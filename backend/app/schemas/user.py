"""
User Schemas

Pydantic models for request/response validation.

What you'll learn:
- Pydantic models for data validation
- Request/response schemas
- Field validation
- Email validation
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
import uuid


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """
    Schema for user registration.
    
    Used when creating a new user account.
    Includes password field.
    """
    password: str = Field(..., min_length=8, max_length=100)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "securepassword123"
            }
        }
    )


class UserUpdate(BaseModel):
    """
    Schema for updating user profile.
    
    All fields are optional.
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """
    Schema for user response.
    
    Returned after registration, login, or profile fetch.
    Never includes password!
    """
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """
    Schema for user login.
    
    Can login with either email or username.
    """
    email: EmailStr
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }
    )


class Token(BaseModel):
    """
    Schema for JWT token response.
    
    Returned after successful login.
    """
    access_token: str
    token_type: str = "bearer"
    message: str
    user: dict
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "message": "Welcome back! You've successfully logged in.",
                "user": {
                    "email": "user@example.com",
                    "username": "johndoe",
                    "full_name": "John Doe"
                }
            }
        }
    )


class TokenData(BaseModel):
    """
    Schema for decoded token data.
    
    Used internally to validate token payload.
    """
    email: Optional[str] = None


# What's happening here?
# ----------------------
# 1. Pydantic Models:
#    - Automatic validation of input data
#    - Type checking
#    - Serialization/deserialization
#    - Auto-generated API docs
#
# 2. Schema Types:
#    - UserCreate: For registration (includes password)
#    - UserResponse: For API responses (no password!)
#    - UserUpdate: For profile updates (all optional)
#    - UserLogin: For authentication
#    - Token: For JWT token response
#
# 3. Field Validation:
#    - EmailStr: Validates email format
#    - Field(): Sets constraints (min/max length)
#    - Optional: Field can be None
#
# 4. Security:
#    - Password never included in UserResponse
#    - Separate schemas for input/output
#    - Validation prevents invalid data
#
# 5. Benefits:
#    - Type safety
#    - Automatic validation
#    - Clear API contracts
#    - Self-documenting
#    - IDE autocomplete
#
# Example Usage:
# user_data = UserCreate(
#     email="test@example.com",
#     username="testuser",
#     password="password123"
# )
# # Pydantic validates automatically
# # Raises error if invalid
