"""
Custom exceptions for Mail.tm Console Client
"""


class MailTMError(Exception):
    """Base exception for Mail.tm client errors"""
    pass


class AuthenticationError(MailTMError):
    """Authentication failed"""
    pass


class AccountNotFoundError(MailTMError):
    """Account not found"""
    pass


class InvalidCredentialsError(MailTMError):
    """Invalid credentials provided"""
    pass


class AccountCreationError(MailTMError):
    """Failed to create account"""
    pass


class APIError(MailTMError):
    """API request failed"""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class NetworkError(MailTMError):
    """Network/connection error"""
    pass


class RateLimitError(MailTMError):
    """Rate limit exceeded"""
    pass


class ValidationError(MailTMError):
    """Input validation error"""
    pass


class CacheError(MailTMError):
    """Cache operation failed"""
    pass


class ConfigurationError(MailTMError):
    """Configuration error"""
    pass
