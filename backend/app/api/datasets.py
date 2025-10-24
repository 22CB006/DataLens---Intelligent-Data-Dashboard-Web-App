"""
Dataset API Routes

This module handles dataset management endpoints.

What you'll learn:
- File upload handling
- Multipart form data
- File validation
- Dataset CRUD operations
- Data processing integration
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.dataset import (
    DatasetUploadResponse,
    DatasetResponse,
    DatasetListResponse,
    DatasetPreview,
    DatasetInfo
)
from app.services import dataset_service
from app.services.file_handler import save_upload_file, delete_file, get_file_extension
from app.services.data_processor import (
    read_dataset,
    get_dataset_info,
    get_dataset_preview
)

# Create router for dataset endpoints
router = APIRouter()


@router.post("/upload", response_model=DatasetUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a new dataset file.
    
    **Request:**
    - file: CSV, Excel, or JSON file (multipart/form-data)
    - Max size: 50MB
    - Allowed types: .csv, .xlsx, .xls, .json
    
    **Returns:**
    - Dataset object with metadata
    - Includes row/column counts after processing
    
    **Raises:**
    - 400: Invalid file type
    - 401: Not authenticated
    - 413: File too large (>50MB)
    
    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/datasets/upload" \\
      -H "Authorization: Bearer <token>" \\
      -F "file=@data.csv"
    ```
    """
    # Save file
    unique_filename, file_path, file_size = await save_upload_file(file)
    
    # Get file extension
    file_type = get_file_extension(unique_filename)
    
    try:
        # Read and process file
        df = read_dataset(file_path, file_type)
        row_count, column_count = df.shape
        
        # Create dataset record
        dataset = await dataset_service.create_dataset(
            db=db,
            user_id=str(current_user.id),
            filename=unique_filename,
            original_filename=file.filename,
            file_type=file_type,
            file_path=file_path,
            file_size=file_size,
            row_count=row_count,
            column_count=column_count
        )
        
        # Return response with success message
        return DatasetUploadResponse(
            id=dataset.id,
            filename=unique_filename,
            original_filename=file.filename,
            file_size=file_size,
            file_type=file_type,
            row_count=row_count,
            column_count=column_count,
            created_at=dataset.created_at,
            message="Dataset uploaded successfully! You can now analyze your data."
        )
    
    except Exception as e:
        # Clean up file if processing fails
        await delete_file(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/", response_model=DatasetListResponse)
async def list_datasets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all datasets for current user.
    
    **Query Parameters:**
    - skip: Number of records to skip (default: 0)
    - limit: Max records to return (default: 100, max: 100)
    
    **Returns:**
    - datasets: Array of dataset objects
    - total: Total count
    - skip: Current offset
    - limit: Current limit
    
    **Raises:**
    - 401: Not authenticated
    
    **Example:**
    ```
    GET /api/v1/datasets/?skip=0&limit=10
    Authorization: Bearer <token>
    ```
    """
    # Get datasets
    datasets = await dataset_service.get_user_datasets(
        db=db,
        user_id=str(current_user.id),
        skip=skip,
        limit=limit
    )
    
    # Get total count
    total = await dataset_service.count_user_datasets(
        db=db,
        user_id=str(current_user.id)
    )
    
    return DatasetListResponse(
        datasets=datasets,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dataset details by ID.
    
    **Path Parameters:**
    - dataset_id: Dataset UUID
    
    **Returns:**
    - Dataset object with full metadata
    
    **Raises:**
    - 401: Not authenticated
    - 403: Not authorized (not owner)
    - 404: Dataset not found
    
    **Example:**
    ```
    GET /api/v1/datasets/550e8400-e29b-41d4-a716-446655440000
    Authorization: Bearer <token>
    ```
    """
    # Get dataset
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    # Check ownership
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this dataset"
        )
    
    return dataset


@router.put("/{dataset_id}", response_model=DatasetResponse)
async def update_dataset(
    dataset_id: str,
    update_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update dataset metadata (e.g., rename).
    
    **Path Parameters:**
    - dataset_id: Dataset UUID
    
    **Request Body:**
    - filename: New filename (optional)
    
    **Returns:**
    - Updated dataset object
    
    **Raises:**
    - 401: Not authenticated
    - 403: Not authorized (not owner)
    - 404: Dataset not found
    """
    # Get dataset
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    # Check ownership
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this dataset"
        )
    
    # Update filename if provided
    if 'filename' in update_data:
        new_filename = update_data['filename']
        # Validate filename is not empty
        if not new_filename or not new_filename.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Filename cannot be empty"
            )
        dataset.filename = new_filename
        # Handle both async and sync sessions
        from sqlalchemy.ext.asyncio import AsyncSession
        if isinstance(db, AsyncSession) or hasattr(db, 'is_async'):
            await db.commit()
            await db.refresh(dataset)
        else:
            db.commit()
            db.refresh(dataset)
    
    return dataset


@router.delete("/{dataset_id}", status_code=status.HTTP_200_OK)
async def delete_dataset(
    dataset_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete dataset and associated file.
    
    **Path Parameters:**
    - dataset_id: Dataset UUID
    
    **Returns:**
    - 204 No Content (success)
    
    **Raises:**
    - 401: Not authenticated
    - 403: Not authorized (not owner)
    - 404: Dataset not found
    
    **Example:**
    ```
    DELETE /api/v1/datasets/550e8400-e29b-41d4-a716-446655440000
    Authorization: Bearer <token>
    ```
    """
    # Get dataset
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found",
            headers={"X-User-Message": "The dataset could not be found. It may have already been deleted or you may not have access to it."}
        )
    
    # Check ownership
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this dataset",
            headers={"X-User-Message": "You don't have permission to delete this dataset."}
        )
    
    try:
        # Delete file
        await delete_file(dataset.file_path)
        
        # Delete database record
        await dataset_service.delete_dataset(db, dataset)
        
        # Return success message
        return {
            "success": True,
            "message": "Dataset deleted successfully.",
            "dataset_id": str(dataset_id)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting dataset: {str(e)}",
            headers={"X-User-Message": "Failed to delete the dataset. Please try again."}
        )


@router.get("/{dataset_id}/preview", response_model=DatasetPreview)
async def preview_dataset(
    dataset_id: str,
    rows: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get preview of dataset (first N rows).
    
    **Path Parameters:**
    - dataset_id: Dataset UUID
    
    **Query Parameters:**
    - rows: Number of rows to preview (default: 10, max: 100)
    
    **Returns:**
    - columns: List of column names
    - data: Array of row objects
    - total_rows: Total rows in dataset
    - preview_rows: Number of rows in preview
    
    **Raises:**
    - 401: Not authenticated
    - 403: Not authorized
    - 404: Dataset not found
    
    **Example:**
    ```
    GET /api/v1/datasets/550e8400.../preview?rows=20
    Authorization: Bearer <token>
    ```
    """
    # Get dataset
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    # Check ownership
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this dataset"
        )
    
    # Read dataset
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    
    # Get preview
    preview = get_dataset_preview(df, n_rows=rows)
    
    return DatasetPreview(**preview)


@router.get("/{dataset_id}/info", response_model=DatasetInfo)
async def get_dataset_info_endpoint(
    dataset_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed dataset information.
    
    **Path Parameters:**
    - dataset_id: Dataset UUID
    
    **Returns:**
    - Comprehensive dataset metadata
    - Column information (types, null counts)
    - Memory usage
    - Data quality metrics
    
    **Raises:**
    - 401: Not authenticated
    - 403: Not authorized
    - 404: Dataset not found
    
    **Example:**
    ```
    GET /api/v1/datasets/550e8400.../info
    Authorization: Bearer <token>
    ```
    """
    # Get dataset
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    # Check ownership
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this dataset"
        )
    
    # Read dataset
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    
    # Get info
    info = get_dataset_info(df)
    
    return DatasetInfo(
        filename=dataset.filename,
        file_size=dataset.file_size,
        row_count=info['row_count'],
        column_count=info['column_count'],
        columns=info['columns'],
        memory_usage=info['memory_usage'],
        created_at=dataset.created_at
    )


# What's happening here?
# ----------------------
# 1. File Upload:
#    - UploadFile handles multipart/form-data
#    - save_upload_file validates and stores
#    - read_dataset processes immediately
#    - Metadata saved to database
#    - Cleanup on error
#
# 2. List Datasets:
#    - Pagination with skip/limit
#    - User-specific filtering
#    - Total count for UI pagination
#    - Ordered by creation date
#
# 3. Get Dataset:
#    - Single dataset details
#    - Ownership verification
#    - Full metadata
#
# 4. Delete Dataset:
#    - File deletion from disk
#    - Database record removal
#    - Authorization check
#    - Atomic operation
#
# 5. Preview:
#    - First N rows
#    - JSON-serializable
#    - Configurable row count
#    - Fast for large files
#
# 6. Info:
#    - Detailed metadata
#    - Column types
#    - Null counts
#    - Memory usage
#
# Security:
# - All endpoints require authentication
# - Ownership verified for each operation
# - File validation on upload
# - Size limits enforced
# - Secure file storage
# - 404: Not Found
#
# Example URLs:
# - POST /api/v1/datasets/upload
# - GET /api/v1/datasets/?skip=0&limit=10
# - GET /api/v1/datasets/abc-123-def
# - GET /api/v1/datasets/abc-123-def/preview?rows=50
