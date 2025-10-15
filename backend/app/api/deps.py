"""
API Dependencies Module

This module contains reusable dependencies for API endpoints.

What you'll learn:
- FastAPI dependency injection
- Reusable components
- Database session management
- Authentication dependencies (to be added)
"""

from typing import Generator
# from sqlalchemy.orm import Session
# from app.core.database import SessionLocal


# Database dependency (will be implemented in Phase 2)
# def get_db() -> Generator:
#     """
#     Database session dependency.
#     
#     Yields a database session and ensures it's closed after use.
#     
#     Usage:
#         @app.get("/users")
#         async def get_users(db: Session = Depends(get_db)):
#             return db.query(User).all()
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# Authentication dependency (will be implemented in Phase 2)
# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ) -> User:
#     """
#     Get current authenticated user from JWT token.
#     
#     This dependency:
#     1. Extracts JWT token from Authorization header
#     2. Validates and decodes the token
#     3. Fetches user from database
#     4. Returns user object
#     
#     Raises:
#         HTTPException: If token is invalid or user not found
#     
#     Usage:
#         @app.get("/profile")
#         async def get_profile(current_user: User = Depends(get_current_user)):
#             return current_user
#     """
#     # Implementation will be added in Phase 2
#     pass


# What are dependencies?
# ---------------------
# Dependencies are reusable functions that:
# 1. Provide common functionality to multiple endpoints
# 2. Are automatically called by FastAPI before the endpoint
# 3. Can be nested (dependencies can have dependencies)
# 4. Make code DRY (Don't Repeat Yourself)
#
# Example flow:
# Request → Dependency (get_db) → Dependency (get_current_user) → Endpoint
#
# Benefits:
# - Code reusability
# - Easier testing (can mock dependencies)
# - Cleaner endpoint code
# - Automatic validation
