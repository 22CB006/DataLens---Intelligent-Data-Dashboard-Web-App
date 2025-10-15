"""
Authentication API Routes

This module handles user authentication endpoints.

What you'll learn:
- API route definition with FastAPI
- Request/response handling
- HTTP status codes
- API documentation with docstrings

Endpoints:
- POST /register - Register new user
- POST /login - Login user
- GET /me - Get current user profile
"""

from fastapi import APIRouter, HTTPException, status

# Create router for authentication endpoints
router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user():
    """
    Register a new user.
    
    **Request Body:**
    - email: User's email address
    - password: User's password (min 8 characters)
    - username: Unique username
    
    **Returns:**
    - User object with id, email, username
    
    **Raises:**
    - 400: Email already registered
    - 422: Validation error
    
    **Implementation:** Phase 2 - Database & Authentication
    """
    # TODO: Implement in Phase 2
    return {
        "message": "User registration endpoint",
        "status": "coming_soon",
        "phase": "Phase 2 - Milestone 2.2"
    }


@router.post("/login")
async def login_user():
    """
    Login user and return JWT token.
    
    **Request Body:**
    - email: User's email
    - password: User's password
    
    **Returns:**
    - access_token: JWT token
    - token_type: "bearer"
    
    **Raises:**
    - 401: Invalid credentials
    - 422: Validation error
    
    **Implementation:** Phase 2 - Database & Authentication
    """
    # TODO: Implement in Phase 2
    return {
        "message": "User login endpoint",
        "status": "coming_soon",
        "phase": "Phase 2 - Milestone 2.2"
    }


@router.get("/me")
async def get_current_user_profile():
    """
    Get current authenticated user's profile.
    
    **Headers:**
    - Authorization: Bearer {token}
    
    **Returns:**
    - User profile object
    
    **Raises:**
    - 401: Not authenticated
    - 404: User not found
    
    **Implementation:** Phase 2 - Database & Authentication
    """
    # TODO: Implement in Phase 2
    return {
        "message": "Get user profile endpoint",
        "status": "coming_soon",
        "phase": "Phase 2 - Milestone 2.2"
    }


# What's happening here?
# ----------------------
# 1. We create an APIRouter instance
# 2. We define endpoints using decorators (@router.post, @router.get)
# 3. Each endpoint has:
#    - HTTP method (GET, POST, PUT, DELETE)
#    - Path (e.g., "/register")
#    - Status code (e.g., 201 for created)
#    - Docstring (appears in API docs)
#    - Handler function (async def)
#
# This router will be included in main.py:
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
#
# Final URLs will be:
# - POST /api/v1/auth/register
# - POST /api/v1/auth/login
# - GET /api/v1/auth/me
