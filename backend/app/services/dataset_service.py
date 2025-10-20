"""
Dataset Service

Business logic for dataset operations.

What you'll learn:
- Dataset CRUD operations
- File metadata management
- User-dataset relationships
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.models.dataset import Dataset
from app.models.user import User


async def create_dataset(
    db: AsyncSession,
    user_id: str,
    filename: str,
    original_filename: str,
    file_type: str,
    file_path: str,
    file_size: int,
    row_count: Optional[int] = None,
    column_count: Optional[int] = None
) -> Dataset:
    """
    Create a new dataset record.
    
    Args:
        db: Database session
        user_id: Owner's user ID
        filename: Unique filename (UUID-based)
        original_filename: Original uploaded filename
        file_type: File extension (csv, xlsx, json)
        file_path: Path to stored file
        file_size: File size in bytes
        row_count: Number of rows (optional)
        column_count: Number of columns (optional)
    
    Returns:
        Created dataset object
    """
    dataset = Dataset(
        user_id=user_id,
        filename=filename,
        original_filename=original_filename,
        file_type=file_type,
        file_path=file_path,
        file_size=file_size,
        row_count=row_count,
        column_count=column_count
    )
    
    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)
    
    return dataset


async def get_dataset_by_id(
    db: AsyncSession,
    dataset_id: str
) -> Optional[Dataset]:
    """
    Get dataset by ID.
    
    Args:
        db: Database session
        dataset_id: Dataset UUID
    
    Returns:
        Dataset object if found, None otherwise
    """
    result = await db.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    return result.scalar_one_or_none()


async def get_user_datasets(
    db: AsyncSession,
    user_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[Dataset]:
    """
    Get all datasets for a user.
    
    Args:
        db: Database session
        user_id: User's UUID
        skip: Number of records to skip
        limit: Maximum records to return
    
    Returns:
        List of dataset objects
    """
    result = await db.execute(
        select(Dataset)
        .where(Dataset.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Dataset.created_at.desc())
    )
    return result.scalars().all()


async def count_user_datasets(
    db: AsyncSession,
    user_id: str
) -> int:
    """
    Count total datasets for a user.
    
    Args:
        db: Database session
        user_id: User's UUID
    
    Returns:
        Total count of datasets
    """
    result = await db.execute(
        select(Dataset).where(Dataset.user_id == user_id)
    )
    return len(result.scalars().all())


async def update_dataset_metadata(
    db: AsyncSession,
    dataset: Dataset,
    row_count: int,
    column_count: int
) -> Dataset:
    """
    Update dataset metadata after processing.
    
    Args:
        db: Database session
        dataset: Dataset object
        row_count: Number of rows
        column_count: Number of columns
    
    Returns:
        Updated dataset object
    """
    dataset.row_count = row_count
    dataset.column_count = column_count
    
    await db.commit()
    await db.refresh(dataset)
    
    return dataset


async def delete_dataset(
    db: AsyncSession,
    dataset: Dataset
) -> None:
    """
    Delete dataset record.
    
    Args:
        db: Database session
        dataset: Dataset object to delete
    
    Note:
        File deletion is handled separately in the route
    """
    # Delete from database
    await db.delete(dataset)
    await db.commit()


# What's happening here?
# ----------------------
# 1. Create Dataset:
#    - Stores file metadata in database
#    - Links to user (foreign key)
#    - Row/column counts optional (processed later)
#
# 2. Get Dataset:
#    - By ID for single dataset
#    - By user for list
#    - Ordered by creation date (newest first)
#
# 3. Pagination:
#    - skip/limit for large lists
#    - Count for total pages
#    - Efficient database queries
#
# 4. Update Metadata:
#    - After file processing
#    - Updates row/column counts
#    - Separate from file upload
#
# 5. Delete:
#    - Removes database record
#    - File deletion handled in route
#    - Cascade deletes handled by DB
#
# 6. User Ownership:
#    - Each dataset belongs to one user
#    - Users can only see their datasets
#    - Foreign key ensures referential integrity
