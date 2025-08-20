"""
Logging configuration for Mail.tm Console Client
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config import config


def setup_logger(name: str = "pryvon_temp_mail") -> logging.Logger:
    """Setup and configure logger"""
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, config.get('log_level', 'INFO')))
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    file_formatter = logging.Formatter(
        config.get('log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    try:
        log_file = Path(config.get('log_file', '~/.pryvon/pryvon.log')).expanduser()
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not setup file logging: {e}")
    
    return logger


# Global logger instance
logger = setup_logger()
