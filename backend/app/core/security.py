"""
Security Module

This module handles password hashing and JWT token operations.

What you'll learn:
- Password hashing with bcrypt
- JWT token creation and validation
- Security best practices
- Token expiration handling
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing context
# bcrypt is a secure hashing algorithm designed for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The password entered by user
        hashed_password: The stored hashed password
    
    Returns:
        True if password matches, False otherwise
    
    Example:
        >>> hashed = get_password_hash("mypassword")
        >>> verify_password("mypassword", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password string
    
    Example:
        >>> hash1 = get_password_hash("mypassword")
        >>> hash2 = get_password_hash("mypassword")
        >>> hash1 != hash2  # Each hash is unique (salt)
        True
    
    Security Notes:
        - Never store plain passwords
        - Bcrypt automatically adds salt
        - Each hash is unique even for same password
        - Computationally expensive (prevents brute force)
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary of data to encode in token (usually user_id, email)
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    
    Example:
        >>> token = create_access_token({"sub": "user@example.com"})
        >>> # Token looks like: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    
    JWT Structure:
        - Header: Algorithm and token type
        - Payload: User data and expiration
        - Signature: Ensures token hasn't been tampered with
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Add expiration to payload
    to_encode.update({"exp": expire})
    
    # Encode JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload if valid, None if invalid
    
    Example:
        >>> token = create_access_token({"sub": "user@example.com"})
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        'user@example.com'
    
    Validation:
        - Checks signature (token not tampered)
        - Checks expiration (token not expired)
        - Checks algorithm matches
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


# What's happening here?
# ----------------------
# 1. Password Hashing (bcrypt):
#    - Plain password → Hash (one-way, can't reverse)
#    - Each hash includes random salt
#    - Verification compares hashes, not passwords
#    - Slow by design (prevents brute force)
#
# 2. JWT Tokens:
#    - Stateless authentication (no session storage)
#    - Contains user info + expiration
#    - Signed with secret key (can't be forged)
#    - Client stores token, sends with each request
#
# 3. Security Benefits:
#    - Passwords never stored in plain text
#    - Tokens expire automatically
#    - Tokens can't be modified without detection
#    - No database lookup needed for auth
#
# 4. Token Flow:
#    Login → Create Token → Return to Client
#    Client → Send Token in Header → Verify Token → Allow Access
#
# Why JWT?
# - Scalable (no server-side session storage)
# - Works across multiple servers
# - Can include custom claims
# - Industry standard
#
# Why bcrypt?
# - Designed specifically for passwords
# - Adaptive (can increase cost over time)
# - Includes salt automatically
# - Resistant to rainbow table attacks
