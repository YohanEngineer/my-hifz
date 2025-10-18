"""
Configuration and logging setup for My Hifz Planner API.
"""

import logging
import sys
from pathlib import Path


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("myhifz")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger


class Settings:
    """Application settings and configuration."""

    # API Configuration
    API_TITLE = "My Hifz Planner API"
    API_DESCRIPTION = "API for Quran memorization planning and page data"
    API_VERSION = "1.0.0"

    # CORS Configuration
    CORS_ORIGINS = [
        "http://localhost:5500",  # Local development (Live Server)
        "http://127.0.0.1:5500",  # Local development (Live Server)
        "https://yohanengineer.github.io",  # GitHub Pages production
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

    # Data Configuration
    QURAN_JSON_PATH = Path("quran.json")
    TOTAL_PAGES = 604
    TOTAL_SURAHS = 114
    TOTAL_JUZ = 30

    # Logging Configuration
    LOG_LEVEL = "INFO"


settings = Settings()
logger = setup_logging(settings.LOG_LEVEL)
