"""
User Service

Business logic for user operations.

What you'll learn:
- Service layer pattern
- Database operations with SQLAlchemy
- Async database queries
- Error handling
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get user by email address.
    
    Args:
        db: Database session
        email: User's email
    
    Returns:
        User object if found, None otherwise
    """
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """
    Get user by username.
    
    Args:
        db: Database session
        username: User's username
    
    Returns:
        User object if found, None otherwise
    """
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
    """
    Get user by ID.
    
    Args:
        db: Database session
        user_id: User's UUID
    
    Returns:
        User object if found, None otherwise
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: Database session
        user_data: User creation data
    
    Returns:
        Created user object
    
    Raises:
        IntegrityError: If email or username already exists
    
    Example:
        >>> user_data = UserCreate(
        ...     email="test@example.com",
        ...     username="testuser",
        ...     password="password123"
        ... )
        >>> user = await create_user(db, user_data)
    """
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user object
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_active=True,
        is_superuser=False
    )
    
    # Add to database
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str
) -> Optional[User]:
    """
    Authenticate user with email and password.
    
    Args:
        db: Database session
        email: User's email
        password: Plain text password
    
    Returns:
        User object if authentication successful, None otherwise
    
    Example:
        >>> user = await authenticate_user(db, "test@example.com", "password123")
        >>> if user:
        ...     print("Login successful!")
        ... else:
        ...     print("Invalid credentials")
    """
    # Get user by email
    user = await get_user_by_email(db, email)
    
    if not user:
        return None
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        return None
    
    # Check if user is active
    if not user.is_active:
        return None
    
    return user


async def update_user(
    db: AsyncSession,
    user: User,
    user_data: UserUpdate
) -> User:
    """
    Update user profile.
    
    Args:
        db: Database session
        user: User object to update
        user_data: Update data
    
    Returns:
        Updated user object
    """
    # Update fields if provided
    if user_data.email is not None:
        user.email = user_data.email
    
    if user_data.username is not None:
        user.username = user_data.username
    
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    
    if user_data.password is not None:
        user.hashed_password = get_password_hash(user_data.password)
    
    await db.commit()
    await db.refresh(user)
    
    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    """
    Delete user account.
    
    Args:
        db: Database session
        user: User object to delete
    
    Note:
        This will also delete all user's datasets (cascade delete)
    """
    await db.delete(user)
    await db.commit()


# What's happening here?
# ----------------------
# 1. Service Layer:
#    - Separates business logic from API routes
#    - Reusable functions
#    - Easier to test
#    - Single responsibility
#
# 2. Async Database Operations:
#    - await db.execute(): Run query
#    - await db.commit(): Save changes
#    - await db.refresh(): Reload object from DB
#    - scalar_one_or_none(): Get single result or None
#
# 3. SQLAlchemy Select:
#    - select(User): Select from users table
#    - .where(): Add WHERE clause
#    - .filter(): Alternative to where
#
# 4. Error Handling:
#    - IntegrityError: Unique constraint violation
#    - None return: Not found
#    - Exceptions propagate to route handler
#
# 5. Security:
#    - Password hashed before storage
#    - Password verification uses bcrypt
#    - Check user is_active before auth
#    - Never return plain password
#
# 6. Pattern Benefits:
#    - Routes stay clean
#    - Logic is reusable
#    - Easy to add caching
#    - Easy to add logging
#    - Testable without HTTP
