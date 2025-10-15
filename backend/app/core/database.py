"""
Database Connection Module

This module handles database connection and session management.

What you'll learn:
- SQLAlchemy async engine setup
- Database session management
- Connection pooling
- Database URL configuration
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Convert PostgreSQL URL to async version
# postgresql://... -> postgresql+asyncpg://...
DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Create async engine
# echo=True will log all SQL statements (useful for debugging)
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL in debug mode
    future=True,
    pool_pre_ping=True,  # Verify connections before using
)

# Create async session factory
# This will be used to create database sessions
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autocommit=False,
    autoflush=False,
)

# Base class for all database models
Base = declarative_base()


# Dependency to get database session
async def get_db() -> AsyncSession:
    """
    Database session dependency.
    
    This function is used as a FastAPI dependency to provide
    a database session to route handlers.
    
    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(User))
            return result.scalars().all()
    
    The session is automatically closed after the request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# What's happening here?
# ----------------------
# 1. We create an async database engine (connection pool)
# 2. We create a session factory (creates new sessions)
# 3. We define a Base class (all models inherit from this)
# 4. We create a dependency function (provides sessions to routes)
#
# Why async?
# - Better performance for I/O operations
# - Can handle multiple requests concurrently
# - Non-blocking database queries
#
# Connection Pooling:
# - Engine maintains a pool of connections
# - Reuses connections instead of creating new ones
# - More efficient than creating connection per request
