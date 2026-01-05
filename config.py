"""
FastAPI Backend Configuration Module

This module contains environment configuration settings for the FastAPI backend server.
Configuration can be managed through environment variables.
"""

import os
from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings and configuration.
    
    Settings are read from environment variables with the prefix specified.
    """
    
    # Application Settings
    app_name: str = os.getenv("APP_NAME", "Password Manager API")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Server Settings
    host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    port: int = int(os.getenv("SERVER_PORT", "8000"))
    
    # API Settings
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
    allowed_origins: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Database Settings
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./test.db"
    )
    database_echo: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    
    # JWT Settings
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    refresh_token_expire_days: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
    )
    
    # Password Settings
    password_min_length: int = int(os.getenv("PASSWORD_MIN_LENGTH", "8"))
    password_require_uppercase: bool = (
        os.getenv("PASSWORD_REQUIRE_UPPERCASE", "True").lower() == "true"
    )
    password_require_numbers: bool = (
        os.getenv("PASSWORD_REQUIRE_NUMBERS", "True").lower() == "true"
    )
    password_require_special_chars: bool = (
        os.getenv("PASSWORD_REQUIRE_SPECIAL_CHARS", "True").lower() == "true"
    )
    
    # Email Settings
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: Optional[str] = os.getenv("SMTP_USERNAME")
    smtp_password: Optional[str] = os.getenv("SMTP_PASSWORD")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "noreply@passwordmanager.com")
    
    # Logging Settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: Optional[str] = os.getenv("LOG_FILE")
    
    # Security Settings
    cors_enabled: bool = os.getenv("CORS_ENABLED", "True").lower() == "true"
    https_only: bool = os.getenv("HTTPS_ONLY", "False").lower() == "true"
    
    # Rate Limiting
    rate_limit_enabled: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_period_seconds: int = int(os.getenv("RATE_LIMIT_PERIOD_SECONDS", "60"))
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False
    
    def is_production(self) -> bool:
        """Check if the application is running in production mode."""
        return not self.debug
    
    def get_database_url(self) -> str:
        """Get the database URL."""
        return self.database_url


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Cached settings object
    """
    return Settings()


# Convenience function to get settings
def load_config() -> Settings:
    """
    Load configuration settings.
    
    Returns:
        Settings: Configuration settings object
    """
    return get_settings()


# Export settings instance
settings = get_settings()
