"""
Authentication API Routes

This module handles user authentication endpoints.

What you'll learn:
- API route definition with FastAPI
- Request/response handling
- HTTP status codes
- API documentation with docstrings
- JWT authentication

Endpoints:
- POST /register - Register new user
- POST /login - Login user
- GET /me - Get current user profile
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services import user_service
from app.api.deps import get_current_user
from app.models.user import User

# Create router for authentication endpoints
router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    
    **Request Body:**
    - email: User's email address (must be valid email)
    - username: Unique username (3-50 characters)
    - password: User's password (min 8 characters)
    - full_name: Optional full name
    
    **Returns:**
    - User object with id, email, username, timestamps
    
    **Raises:**
    - 400: Email or username already registered
    - 422: Validation error (invalid email, short password, etc.)
    
    **Example:**
    ```json
    {
      "email": "user@example.com",
      "username": "johndoe",
      "password": "securepass123",
      "full_name": "John Doe"
    }
    ```
    """
    # Check if email already exists
    existing_user = await user_service.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = await user_service.get_user_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    try:
        user = await user_service.create_user(db, user_data)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )


@router.post("/login", response_model=Token)
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login user and return JWT access token.
    
    **Request Body:**
    - email: User's email
    - password: User's password
    
    **Returns:**
    - access_token: JWT token (use in Authorization header)
    - token_type: "bearer"
    
    **Raises:**
    - 401: Invalid email or password
    - 422: Validation error
    
    **Example:**
    ```json
    {
      "email": "user@example.com",
      "password": "securepass123"
    }
    ```
    
    **Usage:**
    After login, include token in requests:
    ```
    Authorization: Bearer <access_token>
    ```
    """
    # Authenticate user
    user = await user_service.authenticate_user(
        db,
        login_data.email,
        login_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's profile.
    
    **Headers:**
    - Authorization: Bearer {access_token}
    
    **Returns:**
    - User profile object (id, email, username, etc.)
    
    **Raises:**
    - 401: Not authenticated or invalid token
    - 403: User account is inactive
    
    **Example:**
    ```
    GET /api/v1/auth/me
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    ```
    
    **Note:**
    This endpoint requires authentication. You must include a valid
    JWT token in the Authorization header.
    """
    return current_user


# What's happening here?
# ----------------------
# 1. Register Endpoint:
#    - Validates input with Pydantic (UserCreate)
#    - Checks if email/username exists
#    - Hashes password (in service layer)
#    - Creates user in database
#    - Returns user object (no password!)
#
# 2. Login Endpoint:
#    - Validates credentials
#    - Authenticates user (checks password hash)
#    - Creates JWT token with user email
#    - Returns token to client
#
# 3. Get Profile Endpoint:
#    - Requires authentication (Depends(get_current_user))
#    - Token extracted and validated automatically
#    - Returns current user object
#
# 4. Security Flow:
#    Register → Hash Password → Store in DB
#    Login → Verify Password → Create Token → Return Token
#    Protected Route → Verify Token → Get User → Execute
#
# 5. Error Handling:
#    - 400: Bad Request (duplicate email/username)
#    - 401: Unauthorized (invalid credentials/token)
#    - 403: Forbidden (inactive user)
#    - 422: Validation Error (invalid input)
#
# 6. Response Models:
#    - response_model=UserResponse: Validates output
#    - Excludes sensitive fields (password)
#    - Auto-generates API docs
#    - Type safety
