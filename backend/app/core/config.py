"""
Application Configuration Module

This module handles all application settings using Pydantic Settings.
Environment variables are loaded from .env file.

What you'll learn:
- Pydantic Settings for configuration management
- Environment variable handling
- Type-safe configuration
- Default values and validation
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Pydantic automatically:
    - Loads values from .env file
    - Validates types
    - Provides default values
    - Raises errors for missing required fields
    """
    
    # Application Info
    APP_NAME: str = "DataLens"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database Configuration
    DATABASE_URL: str
    # Example: postgresql://user:password@localhost:5432/datalens
    
    # Security Configuration
    SECRET_KEY: str
    # IMPORTANT: Change this in production! Use: openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # CORS Configuration
    # List of allowed origins (frontend URLs)
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 52428800  # 50MB in bytes
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_FILE_TYPES: List[str] = [".csv", ".xlsx", ".xls", ".json"]
    
    class Config:
        """
        Pydantic configuration class.
        
        env_file: Path to .env file
        case_sensitive: Whether env var names are case-sensitive
        """
        env_file = ".env"
        case_sensitive = True


# Create a single instance of settings
# This will be imported throughout the application
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


# What's happening here?
# ----------------------
# 1. Settings class inherits from BaseSettings (Pydantic)
# 2. Each field has a type annotation (str, int, bool, List)
# 3. Pydantic automatically loads values from .env file
# 4. If a required field is missing, it raises an error
# 5. We create one instance (settings) to use everywhere
#
# Example usage in other files:
# from app.core.config import settings
# print(settings.DATABASE_URL)
# print(settings.SECRET_KEY)
