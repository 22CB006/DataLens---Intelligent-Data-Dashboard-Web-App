"""
Dataset Model

This module defines the Dataset database model.

What you'll learn:
- Foreign key relationships
- JSONB column type (PostgreSQL specific)
- Enum types for status
- File metadata storage
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class DatasetStatus(str, enum.Enum):
    """
    Enum for dataset processing status.
    
    This ensures only valid status values can be stored.
    """
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


class Dataset(BaseModel):
    """
    Dataset model for storing uploaded file metadata.
    
    Fields:
    - id: UUID primary key (inherited)
    - user_id: Foreign key to User
    - filename: Unique filename in storage
    - original_filename: Original uploaded filename
    - file_type: File extension (csv, xlsx, json)
    - file_size: Size in bytes
    - file_path: Path to stored file
    - row_count: Number of rows in dataset
    - column_count: Number of columns
    - columns_info: JSON with column metadata
    - status: Processing status (uploaded, processing, ready, error)
    - created_at: Timestamp (inherited)
    - updated_at: Timestamp (inherited)
    
    Relationships:
    - owner: Many-to-One relationship with User
    """
    
    __tablename__ = "datasets"
    
    # Foreign key to users table
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),  # Delete datasets when user is deleted
        nullable=False,
        index=True  # Index for faster joins
    )
    
    # File information
    filename = Column(
        String(255),
        unique=True,  # Each file has unique name in storage
        nullable=False
    )
    
    original_filename = Column(
        String(255),
        nullable=False
    )
    
    file_type = Column(
        String(50),
        nullable=False
    )
    
    file_size = Column(
        Integer,
        nullable=False
    )
    
    file_path = Column(
        String(500),
        nullable=False
    )
    
    # Dataset metadata
    row_count = Column(
        Integer,
        nullable=True  # Set after processing
    )
    
    column_count = Column(
        Integer,
        nullable=True
    )
    
    # JSONB column for flexible column metadata
    # Example: {"columns": [{"name": "age", "type": "int64", "null_count": 0}, ...]}
    columns_info = Column(
        JSONB,
        nullable=True
    )
    
    # Processing status
    status = Column(
        SQLEnum(DatasetStatus),
        default=DatasetStatus.UPLOADED,
        nullable=False
    )
    
    # Relationship with user
    owner = relationship(
        "User",
        back_populates="datasets"
    )
    
    def __repr__(self):
        """String representation."""
        return f"<Dataset(filename={self.filename}, status={self.status})>"


# What's happening here?
# ----------------------
# 1. Dataset inherits from BaseModel
# 2. user_id is a foreign key linking to User.id
# 3. ForeignKey with ondelete="CASCADE" means:
#    - When user is deleted, their datasets are deleted too
# 4. JSONB stores flexible JSON data efficiently
# 5. Enum ensures only valid status values
#
# Foreign Keys:
# - Link records between tables
# - user_id references users.id
# - ondelete="CASCADE" handles deletion
# - Index speeds up joins
#
# JSONB vs JSON:
# - JSONB is PostgreSQL-specific
# - Stores JSON in binary format
# - Faster queries and indexing
# - Can query nested JSON fields
#
# Why store columns_info as JSON?
# - Flexible schema (different datasets have different columns)
# - Can store complex metadata
# - Easy to extend without schema changes
#
# Enum Benefits:
# - Type safety (only valid values allowed)
# - Self-documenting code
# - Database constraint
# - Easy to add new statuses
#
# Relationships:
# - Many Datasets belong to One User
# - back_populates creates bidirectional link
# - Can access dataset.owner or user.datasets
