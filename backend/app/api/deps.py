"""
API Dependencies Module

This module contains reusable dependencies for API endpoints.

What you'll learn:
- FastAPI dependency injection
- Reusable components
- Database session management
- Authentication dependencies
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.services import user_service

# OAuth2 scheme for token extraction
# This tells FastAPI to look for token in Authorization header
# Format: "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    This dependency:
    1. Extracts JWT token from Authorization header
    2. Validates and decodes the token
    3. Fetches user from database
    4. Returns user object
    
    Args:
        token: JWT token from Authorization header
        db: Database session
    
    Returns:
        User object
    
    Raises:
        HTTPException 401: If token is invalid or user not found
    
    Usage:
        @app.get("/profile")
        async def get_profile(current_user: User = Depends(get_current_user)):
            return current_user
    
    How it works:
        1. FastAPI extracts token from header automatically
        2. decode_access_token() validates and decodes JWT
        3. Extract email from token payload
        4. Fetch user from database
        5. Return user or raise 401 error
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extract email from token
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    # Get user from database
    user = await user_service.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they are a superuser.
    
    Use this dependency for admin-only endpoints.
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        User object if superuser
    
    Raises:
        HTTPException 403: If user is not a superuser
    
    Usage:
        @app.delete("/users/{user_id}")
        async def delete_user(
            user_id: str,
            admin: User = Depends(get_current_active_superuser)
        ):
            # Only superusers can access this
            pass
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


# What are dependencies?
# ---------------------
# Dependencies are reusable functions that:
# 1. Provide common functionality to multiple endpoints
# 2. Are automatically called by FastAPI before the endpoint
# 3. Can be nested (dependencies can have dependencies)
# 4. Make code DRY (Don't Repeat Yourself)
#
# Example flow:
# Request → oauth2_scheme (extract token) → get_current_user (validate) → Endpoint
#
# Benefits:
# - Code reusability
# - Easier testing (can mock dependencies)
# - Cleaner endpoint code
# - Automatic validation
# - Security handled centrally
#
# OAuth2PasswordBearer:
# - Automatically extracts token from header
# - Adds security to OpenAPI docs
# - Shows "Authorize" button in Swagger UI
# - Handles "Bearer" prefix automatically
