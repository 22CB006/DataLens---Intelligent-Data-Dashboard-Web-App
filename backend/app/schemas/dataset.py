"""
Dataset Schemas

Pydantic models for dataset request/response validation.

What you'll learn:
- File upload schemas
- Dataset metadata schemas
- Response models
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import uuid


class DatasetUploadResponse(BaseModel):
    """
    Schema for dataset upload response.
    
    Returned after successful file upload.
    """
    id: uuid.UUID
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    created_at: datetime
    message: str = "Dataset uploaded successfully! You can now analyze your data."
    
    model_config = ConfigDict(from_attributes=True)


class DatasetResponse(BaseModel):
    """
    Schema for dataset response.
    
    Full dataset information including user.
    """
    id: uuid.UUID
    user_id: uuid.UUID
    filename: str
    file_path: str
    file_size: int
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DatasetListResponse(BaseModel):
    """
    Schema for dataset list response with pagination.
    """
    datasets: list[DatasetResponse]
    total: int
    skip: int
    limit: int
    message: str = "Datasets loaded successfully."


class DatasetPreview(BaseModel):
    """
    Schema for dataset preview.
    
    Returns first few rows of data.
    """
    columns: list[str]
    data: list[dict]
    message: str = "Dataset preview loaded successfully."
    total_rows: int
    preview_rows: int


class DatasetInfo(BaseModel):
    """
    Schema for dataset information.
    
    Returns metadata about the dataset.
    """
    filename: str
    file_size: int
    row_count: int
    column_count: int
    columns: list[dict]  # [{name, type, non_null_count}]
    memory_usage: str
    created_at: datetime


# What's happening here?
# ----------------------
# 1. Upload Response:
#    - Returns immediately after upload
#    - Includes file metadata
#    - Row/column counts may be None (processed later)
#
# 2. Dataset Response:
#    - Full dataset information
#    - Includes user relationship
#    - Used for GET endpoints
#
# 3. List Response:
#    - Pagination support
#    - Total count for UI
#    - Array of datasets
#
# 4. Preview:
#    - First N rows
#    - Column names
#    - Total row count
#
# 5. Info:
#    - Detailed metadata
#    - Column information
#    - Memory usage
#    - Data types
