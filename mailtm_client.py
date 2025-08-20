import requests
import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import config
from logger import logger
from cache import cache
from exceptions import *


@dataclass
class MailAccount:
    """Represents a mail.tm account"""
    id: str
    address: str
    quota: int
    used: int
    is_disabled: bool
    is_deleted: bool
    created_at: str
    updated_at: str


@dataclass
class MailMessage:
    """Represents an email message"""
    id: str
    from_address: str
    to_address: str
    subject: str
    intro: str
    seen: bool
    is_deleted: bool
    has_attachments: bool
    size: int
    download_url: str
    created_at: str
    updated_at: str


class MailTMClient:
    """Enhanced client for interacting with mail.tm API"""
    
    def __init__(self):
        self.session = self._create_session()
        self.token = None
        self.current_account = None
        self.last_request_time = 0
        self.request_count = 0
        
    def _create_session(self) -> requests.Session:
        """Create a session with retry logic and proper configuration"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=config.get('max_retries', 3),
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            'User-Agent': 'MailTM-Console-Client/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        return session
    
    def _rate_limit_check(self):
        """Basic rate limiting to be respectful to the API"""
        current_time = time.time()
        if current_time - self.last_request_time < 0.1:  # 100ms between requests
            time.sleep(0.1)
        self.last_request_time = current_time
        self.request_count += 1
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request to the mail.tm API with enhanced error handling"""
        url = f"{config.get('api_base_url', 'https://api.mail.tm')}{endpoint}"
        
        # Rate limiting
        self._rate_limit_check()
        
        # Add authentication if available
        if self.token:
            kwargs.setdefault('headers', {})['Authorization'] = f"Bearer {self.token}"
        
        # Set timeout
        kwargs.setdefault('timeout', config.get('api_timeout', 30))
        
        try:
            logger.debug(f"Making {method} request to {endpoint}")
            response = self.session.request(method, url, **kwargs)
            
            # Handle different HTTP status codes
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed. Please login again.")
            elif response.status_code == 403:
                raise AuthenticationError("Access denied. Check your permissions.")
            elif response.status_code == 404:
                raise AccountNotFoundError("Resource not found.")
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded. Please wait before trying again.")
            elif response.status_code >= 500:
                raise NetworkError(f"Server error: {response.status_code}")
            elif response.status_code >= 400:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', 'Unknown error')
                    raise APIError(f"API Error: {error_msg}", response.status_code, error_data)
                except (json.JSONDecodeError, KeyError):
                    raise APIError(f"API Error ({response.status_code}): {response.text}", response.status_code)
            
            return response
            
        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out. Please check your connection.")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Connection failed. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {str(e)}")
    
    def get_domains(self, use_cache: bool = True) -> List[Dict]:
        """Get available domains for account creation with caching"""
        cache_key = "domains"
        
        if use_cache:
            cached_domains = cache.get(cache_key)
            if cached_domains:
                logger.debug("Using cached domains")
                return cached_domains
        
        try:
            response = self._make_request('GET', '/domains')
            domains = response.json()['hydra:member']
            
            # Cache the result
            if use_cache:
                cache.set(cache_key, domains, ttl=3600)  # Cache for 1 hour
            
            logger.info(f"Retrieved {len(domains)} domains")
            return domains
            
        except Exception as e:
            logger.error(f"Failed to get domains: {e}")
            raise
    
    def create_account(self, address: str, password: str) -> MailAccount:
        """Create a new mail.tm account with validation"""
        # Validate input
        if not address or '@' not in address:
            raise ValidationError("Invalid email address format")
        if not password or len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long")
        
        try:
            data = {
                "address": address,
                "password": password
            }
            
            logger.info(f"Creating account: {address}")
            response = self._make_request('POST', '/accounts', json=data)
            account_data = response.json()
            
            account = MailAccount(
                id=account_data['id'],
                address=account_data['address'],
                quota=account_data['quota'],
                used=account_data['used'],
                is_disabled=account_data['isDisabled'],
                is_deleted=account_data['isDeleted'],
                created_at=account_data['createdAt'],
                updated_at=account_data['updatedAt']
            )
            
            logger.info(f"Account created successfully: {account.address}")
            
            # Clear domain cache since we might have used one
            cache.delete("domains")
            
            return account
            
        except Exception as e:
            logger.error(f"Failed to create account: {e}")
            if "already exists" in str(e).lower():
                raise AccountCreationError(f"Account {address} already exists")
            raise
    
    def login(self, address: str, password: str) -> Tuple[MailAccount, str]:
        """Login to an existing account with enhanced error handling"""
        try:
            data = {
                "address": address,
                "password": password
            }
            
            logger.info(f"Logging in: {address}")
            response = self._make_request('POST', '/token', json=data)
            token_data = response.json()
            
            self.token = token_data['token']
            
            # Get account info
            account_response = self._make_request('GET', '/me')
            account_data = account_response.json()
            
            account = MailAccount(
                id=account_data['id'],
                address=account_data['address'],
                quota=account_data['quota'],
                used=account_data['used'],
                is_disabled=account_data['isDisabled'],
                is_deleted=account_data['isDeleted'],
                created_at=account_data['createdAt'],
                updated_at=account_data['updatedAt']
            )
            
            self.current_account = account
            logger.info(f"Login successful: {account.address}")
            
            return account, self.token
            
        except Exception as e:
            logger.error(f"Login failed for {address}: {e}")
            if "invalid" in str(e).lower() or "credentials" in str(e).lower():
                raise InvalidCredentialsError("Invalid email or password")
            raise
    
    def delete_account(self) -> bool:
        """Delete the current account with confirmation"""
        if not self.current_account:
            raise AuthenticationError("No account logged in")
        
        try:
            logger.warning(f"Deleting account: {self.current_account.address}")
            response = self._make_request('DELETE', f'/accounts/{self.current_account.id}')
            
            if response.status_code == 204:
                logger.info(f"Account {self.current_account.address} deleted successfully")
                return True
            else:
                raise APIError(f"Failed to delete account: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to delete account: {e}")
            raise
    
    def get_messages(self, page: int = 1, limit: int = None, use_cache: bool = True) -> List[MailMessage]:
        """Get messages from the current account's mailbox with caching"""
        if not self.current_account:
            raise AuthenticationError("No account logged in")
        
        limit = limit or config.get('max_messages_display', 100)
        cache_key = f"messages_{self.current_account.id}_{page}_{limit}"
        
        if use_cache:
            cached_messages = cache.get(cache_key)
            if cached_messages:
                logger.debug("Using cached messages")
                return cached_messages
        
        try:
            params = {
                'page': page,
                'limit': limit
            }
            
            response = self._make_request('GET', '/messages', params=params)
            messages_data = response.json()['hydra:member']
            
            messages = []
            for msg_data in messages_data:
                message = MailMessage(
                    id=msg_data['id'],
                    from_address=msg_data['from']['address'],
                    to_address=msg_data['to'][0]['address'] if msg_data['to'] else '',
                    subject=msg_data['subject'],
                    intro=msg_data['intro'],
                    seen=msg_data['seen'],
                    is_deleted=msg_data['isDeleted'],
                    has_attachments=msg_data['hasAttachments'],
                    size=msg_data['size'],
                    download_url=msg_data['downloadUrl'],
                    created_at=msg_data['createdAt'],
                    updated_at=msg_data['updatedAt']
                )
                messages.append(message)
            
            # Cache the result
            if use_cache:
                cache.set(cache_key, messages, ttl=300)  # Cache for 5 minutes
            
            logger.debug(f"Retrieved {len(messages)} messages")
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get messages: {e}")
            raise
    
    def get_message(self, message_id: str, use_cache: bool = True) -> Dict:
        """Get full message content by ID with caching"""
        if not self.current_account:
            raise AuthenticationError("No account logged in")
        
        cache_key = f"message_{message_id}"
        
        if use_cache:
            cached_message = cache.get(cache_key)
            if cached_message:
                logger.debug("Using cached message")
                return cached_message
        
        try:
            response = self._make_request('GET', f'/messages/{message_id}')
            message_data = response.json()
            
            # Cache the result
            if use_cache:
                cache.set(cache_key, message_data, ttl=1800)  # Cache for 30 minutes
            
            return message_data
            
        except Exception as e:
            logger.error(f"Failed to get message {message_id}: {e}")
            raise
    
    def mark_message_seen(self, message_id: str) -> bool:
        """Mark a message as seen"""
        if not self.current_account:
            raise AuthenticationError("No account logged in")
        
        try:
            data = {"seen": True}
            response = self._make_request('PATCH', f'/messages/{message_id}', json=data)
            
            if response.status_code == 200:
                logger.debug(f"Message {message_id} marked as seen")
                
                # Clear message cache
                cache.delete(f"message_{message_id}")
                cache.delete(f"messages_{self.current_account.id}_1_50")  # Clear first page cache
                
                return True
            else:
                raise APIError(f"Failed to mark message as seen: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to mark message as seen: {e}")
            raise
    
    def delete_message(self, message_id: str) -> bool:
        """Delete a message"""
        if not self.current_account:
            raise AuthenticationError("No account logged in")
        
        try:
            response = self._make_request('DELETE', f'/messages/{message_id}')
            
            if response.status_code == 204:
                logger.debug(f"Message {message_id} deleted")
                
                # Clear caches
                cache.delete(f"message_{message_id}")
                cache.delete(f"messages_{self.current_account.id}_1_50")
                
                return True
            else:
                raise APIError(f"Failed to delete message: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")
            raise
    
    def refresh_mailbox(self) -> List[MailMessage]:
        """Refresh mailbox and get latest messages"""
        # Clear message cache to force fresh data
        if self.current_account:
            cache.delete(f"messages_{self.current_account.id}_1_50")
        
        return self.get_messages(use_cache=False)
    
    def get_account_stats(self) -> Dict[str, Any]:
        """Get account statistics"""
        if not self.current_account:
            raise AuthenticationError("No account logged in")
        
        return {
            'address': self.current_account.address,
            'quota_used': self.current_account.used,
            'quota_total': self.current_account.quota,
            'quota_percentage': round((self.current_account.used / self.current_account.quota) * 100, 2),
            'created_at': self.current_account.created_at,
            'last_updated': self.current_account.updated_at,
            'request_count': self.request_count
        }
    
    def logout(self):
        """Logout and clear session"""
        if self.current_account:
            logger.info(f"Logging out: {self.current_account.address}")
        
        self.token = None
        self.current_account = None
        self.session.close()
        
        # Clear sensitive caches
        if self.current_account:
            cache.delete(f"messages_{self.current_account.id}_1_50")
    
    def is_logged_in(self) -> bool:
        """Check if currently logged in"""
        return self.token is not None and self.current_account is not None
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return cache.get_stats()
    
    def clear_cache(self):
        """Clear all cached data"""
        cache.clear()
        logger.info("Cache cleared")
