"""
Base Model Module

This module contains the base model class with common fields.

What you'll learn:
- SQLAlchemy model inheritance
- Common model fields (id, timestamps)
- UUID primary keys
- Automatic timestamp management
"""

from sqlalchemy import Column, DateTime, func, TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36), storing as stringified hex values.
    This allows tests to run on SQLite while production uses PostgreSQL.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            else:
                return value


class BaseModel(Base):
    """
    Base model class with common fields.
    
    All database models should inherit from this class.
    It provides:
    - UUID primary key
    - created_at timestamp
    - updated_at timestamp (auto-updated)
    """
    
    __abstract__ = True  # This tells SQLAlchemy not to create a table for this class
    
    # Primary key as UUID (more secure than sequential integers)
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    
    # Timestamp when record was created
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # Database sets this automatically
        nullable=False
    )
    
    # Timestamp when record was last updated
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # Automatically updates on record change
        nullable=False
    )
    
    def __repr__(self):
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"


# What's happening here?
# ----------------------
# 1. BaseModel inherits from SQLAlchemy's Base
# 2. __abstract__ = True means no table is created for BaseModel
# 3. All models inheriting from BaseModel get these fields automatically
# 4. UUID is used instead of integer for better security
# 5. Timestamps are managed automatically by the database
#
# Why UUID?
# - More secure (can't guess next ID)
# - Globally unique (useful for distributed systems)
# - No collision risk
#
# Why timestamps?
# - Track when records are created
# - Track when records are modified
# - Useful for auditing and debugging
#
# Example usage:
# class User(BaseModel):
#     __tablename__ = "users"
#     email = Column(String, unique=True)
#     # id, created_at, updated_at are inherited automatically
