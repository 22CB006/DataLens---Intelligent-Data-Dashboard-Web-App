"""
User Model

This module defines the User database model.

What you'll learn:
- SQLAlchemy model definition
- Column types and constraints
- Relationships between models
- Indexes for query optimization
"""

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class User(BaseModel):
    """
    User model for authentication and user management.
    
    Fields:
    - id: UUID primary key (inherited from BaseModel)
    - email: Unique email address
    - username: Unique username
    - hashed_password: Bcrypt hashed password
    - full_name: Optional full name
    - is_active: Whether user account is active
    - is_superuser: Whether user has admin privileges
    - created_at: Timestamp (inherited)
    - updated_at: Timestamp (inherited)
    
    Relationships:
    - datasets: One-to-Many relationship with Dataset model
    """
    
    __tablename__ = "users"
    
    # Email address (unique, required)
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True  # Index for faster lookups
    )
    
    # Username (unique, required)
    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    
    # Hashed password (never store plain passwords!)
    hashed_password = Column(
        String(255),
        nullable=False
    )
    
    # Full name (optional)
    full_name = Column(
        String(255),
        nullable=True
    )
    
    # Account status flags
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )
    
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False
    )
    
    # Relationship with datasets
    # This creates a virtual field 'datasets' that returns all datasets for this user
    # cascade="all, delete-orphan" means when user is deleted, their datasets are too
    datasets = relationship(
        "Dataset",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        """String representation."""
        return f"<User(email={self.email}, username={self.username})>"


# What's happening here?
# ----------------------
# 1. User inherits from BaseModel (gets id, timestamps)
# 2. __tablename__ specifies the database table name
# 3. Each Column represents a database column
# 4. unique=True ensures no duplicates
# 5. index=True creates database index for faster queries
# 6. relationship() creates a link to Dataset model
#
# Column Types:
# - String(255): Variable-length string, max 255 chars
# - Boolean: True/False value
# - UUID: Universally unique identifier (from BaseModel)
# - DateTime: Date and time (from BaseModel)
#
# Why index email and username?
# - These fields are frequently used in WHERE clauses
# - Indexes make lookups much faster
# - Trade-off: Slightly slower writes, much faster reads
#
# Security Note:
# - NEVER store plain passwords
# - Always hash passwords with bcrypt
# - hashed_password stores the bcrypt hash
#
# Relationships:
# - One User can have Many Datasets
# - back_populates creates bidirectional relationship
# - cascade ensures related records are deleted together
