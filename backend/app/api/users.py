"""
User Management API Routes

This module handles user CRUD operations.

What you'll learn:
- CRUD operations (Create, Read, Update, Delete)
- Protected routes with authentication
- Admin-only endpoints
- Query parameters for filtering
- Pagination

Endpoints:
- GET /users - List all users (admin only)
- GET /users/{user_id} - Get user by ID
- PUT /users/me - Update current user profile
- DELETE /users/me - Delete current user account
- DELETE /users/{user_id} - Delete user (admin only)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services import user_service
from app.api.deps import get_current_user, get_current_active_superuser
from app.models.user import User

# Create router for user management endpoints
router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    List all users (Admin only).
    
    **Query Parameters:**
    - skip: Number of records to skip (default: 0)
    - limit: Maximum records to return (default: 100, max: 100)
    
    **Returns:**
    - List of user objects
    
    **Raises:**
    - 401: Not authenticated
    - 403: Not a superuser
    
    **Example:**
    ```
    GET /api/v1/users?skip=0&limit=10
    Authorization: Bearer <admin_token>
    ```
    
    **Note:**
    This endpoint requires superuser privileges.
    """
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return users


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's profile.
    
    **Headers:**
    - Authorization: Bearer {access_token}
    
    **Returns:**
    - Current user profile
    
    **Raises:**
    - 401: Not authenticated
    
    **Example:**
    ```
    GET /api/v1/users/me
    Authorization: Bearer <token>
    ```
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user's profile.
    
    **Request Body:**
    - email: New email (optional)
    - username: New username (optional)
    - full_name: New full name (optional)
    - password: New password (optional, min 8 characters)
    
    **Returns:**
    - Updated user profile
    
    **Raises:**
    - 400: Email or username already taken
    - 401: Not authenticated
    - 422: Validation error
    
    **Example:**
    ```json
    {
      "full_name": "Updated Name",
      "password": "newpassword123"
    }
    ```
    
    **Note:**
    - All fields are optional
    - Password will be hashed automatically
    - Email and username must be unique
    """
    # Check if email is being updated and already exists
    if user_update.email and user_update.email != current_user.email:
        existing_user = await user_service.get_user_by_email(db, user_update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if username is being updated and already exists
    if user_update.username and user_update.username != current_user.username:
        existing_user = await user_service.get_user_by_username(db, user_update.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Update user
    updated_user = await user_service.update_user(db, current_user, user_update)
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete current user's account.
    
    **Headers:**
    - Authorization: Bearer {access_token}
    
    **Returns:**
    - 204 No Content (success)
    
    **Raises:**
    - 401: Not authenticated
    
    **Example:**
    ```
    DELETE /api/v1/users/me
    Authorization: Bearer <token>
    ```
    
    **Warning:**
    - This action is irreversible
    - All user data will be deleted
    - All user's datasets will be deleted (cascade)
    """
    await user_service.delete_user(db, current_user)
    return None


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID.
    
    **Path Parameters:**
    - user_id: User's UUID
    
    **Returns:**
    - User profile
    
    **Raises:**
    - 401: Not authenticated
    - 403: Not authorized (can only view own profile unless superuser)
    - 404: User not found
    
    **Example:**
    ```
    GET /api/v1/users/06323b0d-cfa7-4701-97d5-be286fe12149
    Authorization: Bearer <token>
    ```
    
    **Note:**
    - Regular users can only view their own profile
    - Superusers can view any user profile
    """
    # Check if user is trying to access their own profile or is superuser
    if str(current_user.id) != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Delete user by ID (Admin only).
    
    **Path Parameters:**
    - user_id: User's UUID
    
    **Returns:**
    - 204 No Content (success)
    
    **Raises:**
    - 401: Not authenticated
    - 403: Not a superuser
    - 404: User not found
    
    **Example:**
    ```
    DELETE /api/v1/users/06323b0d-cfa7-4701-97d5-be286fe12149
    Authorization: Bearer <admin_token>
    ```
    
    **Warning:**
    - This action is irreversible
    - All user data will be deleted
    - Requires superuser privileges
    """
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await user_service.delete_user(db, user)
    return None


# What's happening here?
# ----------------------
# 1. CRUD Operations:
#    - Create: Already in auth.py (register)
#    - Read: GET /users, GET /users/me, GET /users/{id}
#    - Update: PUT /users/me
#    - Delete: DELETE /users/me, DELETE /users/{id}
#
# 2. Authorization Levels:
#    - Public: None (all require auth)
#    - User: /me endpoints (own profile)
#    - Admin: /users list, delete by ID
#
# 3. Query Parameters:
#    - skip: Pagination offset
#    - limit: Max results (capped at 100)
#    - Query() provides validation and docs
#
# 4. Path Parameters:
#    - {user_id}: UUID from URL
#    - Automatically validated by FastAPI
#
# 5. Security:
#    - All endpoints require authentication
#    - Some require superuser (admin)
#    - Users can only modify their own data
#    - Admins can modify any user
#
# 6. Response Codes:
#    - 200: Success (GET, PUT)
#    - 204: Success, no content (DELETE)
#    - 400: Bad request (duplicate email/username)
#    - 401: Unauthorized (not authenticated)
#    - 403: Forbidden (not authorized)
#    - 404: Not found
#
# 7. Validation:
#    - Email uniqueness checked before update
#    - Username uniqueness checked before update
#    - Password hashed automatically in service
#
# 8. Cascade Delete:
#    - Deleting user deletes all their datasets
#    - Handled by database foreign key constraint
#    - ondelete="CASCADE" in Dataset model
