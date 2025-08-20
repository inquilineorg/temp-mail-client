"""
Caching system for Mail.tm Console Client
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional
from config import config
from logger import logger


class Cache:
    """Simple file-based cache with TTL support"""
    
    def __init__(self, cache_file: str = None):
        self.cache_file = Path(cache_file or config.get('cache_file', '~/.pryvon/cache.json')).expanduser()
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.load_cache()
    
    def load_cache(self):
        """Load cache from file"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
                # Clean expired entries
                self._cleanup()
        except Exception as e:
            logger.warning(f"Could not load cache: {e}")
            self.cache = {}
    
    def save_cache(self):
        """Save cache to file"""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save cache: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache if not expired"""
        if not config.get('cache_enabled', True):
            return default
        
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry.get('expires', 0):
                return entry.get('value')
            else:
                # Remove expired entry
                del self.cache[key]
                self.save_cache()
        
        return default
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Set value in cache with TTL"""
        if not config.get('cache_enabled', True):
            return
        
        ttl = ttl or config.get('cache_ttl', 300)
        self.cache[key] = {
            'value': value,
            'expires': time.time() + ttl,
            'created': time.time()
        }
        self.save_cache()
    
    def delete(self, key: str):
        """Delete key from cache"""
        if key in self.cache:
            del self.cache[key]
            self.save_cache()
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.save_cache()
    
    def _cleanup(self):
        """Remove expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self.cache.items()
            if current_time >= entry.get('expires', 0)
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self.save_cache()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_time = time.time()
        active_entries = sum(
            1 for entry in self.cache.values()
            if current_time < entry.get('expires', 0)
        )
        
        return {
            'total_entries': len(self.cache),
            'active_entries': active_entries,
            'expired_entries': len(self.cache) - active_entries,
            'cache_size_mb': self.cache_file.stat().st_size / (1024 * 1024) if self.cache_file.exists() else 0
        }


# Global cache instance
cache = Cache()
