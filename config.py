"""
Configuration management for Mail.tm Console Client
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class AppConfig:
    """Application configuration"""
    # API Configuration
    api_base_url: str = "https://api.mail.tm"
    api_timeout: int = 30
    max_retries: int = 3
    
    # UI Configuration
    refresh_interval: int = 30  # seconds
    max_messages_display: int = 100
    auto_refresh: bool = True
    
    # Security Configuration
    save_credentials: bool = False
    credentials_file: str = "~/.pryvon/credentials.json"
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "~/.pryvon/pryvon.log"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cache Configuration
    cache_enabled: bool = True
    cache_ttl: int = 300  # 5 minutes
    cache_file: str = "~/.pryvon/cache.json"


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_file: str = "~/.pryvon/config.json"):
        self.config_file = Path(config_file).expanduser()
        self.config = AppConfig()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    for key, value in config_data.items():
                        if hasattr(self.config, key):
                            setattr(self.config, key, value)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return getattr(self.config, key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        if hasattr(self.config, key):
            setattr(self.config, key, value)
            self.save_config()
    
    def update(self, **kwargs):
        """Update multiple configuration values"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self.save_config()


# Global configuration instance
config = ConfigManager()
