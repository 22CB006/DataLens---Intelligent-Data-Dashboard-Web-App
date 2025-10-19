"""
File Handler Service

This module handles file upload, validation, and storage.

What you'll learn:
- File upload with FastAPI
- File type validation
- Async file operations
- Secure file storage
- UUID generation
"""

import os
import uuid
import aiofiles
from pathlib import Path
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException, status

# Allowed file extensions
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json"}

# Maximum file size (50 MB)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB in bytes

# Upload directory
UPLOAD_DIR = Path("uploads")


def ensure_upload_directory():
    """
    Create upload directory if it doesn't exist.
    
    This function is called on startup to ensure
    the upload directory exists.
    """
    UPLOAD_DIR.mkdir(exist_ok=True)
    print(f"📁 Upload directory ready: {UPLOAD_DIR.absolute()}")


def validate_file_extension(filename: str) -> bool:
    """
    Validate file extension.
    
    Args:
        filename: Name of the file
    
    Returns:
        True if extension is allowed, False otherwise
    
    Example:
        >>> validate_file_extension("data.csv")
        True
        >>> validate_file_extension("data.txt")
        False
    """
    file_ext = Path(filename).suffix.lower()
    return file_ext in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate unique filename using UUID.
    
    Args:
        original_filename: Original filename from upload
    
    Returns:
        Unique filename with UUID prefix
    
    Example:
        >>> generate_unique_filename("sales.csv")
        '550e8400-e29b-41d4-a716-446655440000_sales.csv'
    
    Why UUID?
    - Prevents filename collisions
    - Secure (unpredictable)
    - Sortable by creation time
    """
    file_ext = Path(original_filename).suffix.lower()
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{file_ext}"


async def save_upload_file(upload_file: UploadFile) -> Tuple[str, str, int]:
    """
    Save uploaded file to disk.
    
    Args:
        upload_file: FastAPI UploadFile object
    
    Returns:
        Tuple of (unique_filename, file_path, file_size)
    
    Raises:
        HTTPException: If file validation fails
    
    Example:
        >>> file = UploadFile(...)
        >>> filename, path, size = await save_upload_file(file)
    
    Process:
        1. Validate file extension
        2. Generate unique filename
        3. Write file asynchronously
        4. Return file metadata
    """
    # Validate file extension
    if not validate_file_extension(upload_file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique filename
    unique_filename = generate_unique_filename(upload_file.filename)
    file_path = UPLOAD_DIR / unique_filename
    
    # Write file asynchronously
    file_size = 0
    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await upload_file.read(8192):  # Read in 8KB chunks
            file_size += len(chunk)
            
            # Check file size limit
            if file_size > MAX_FILE_SIZE:
                # Delete partial file
                await f.close()
                os.remove(file_path)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.0f} MB"
                )
            
            await f.write(chunk)
    
    return unique_filename, str(file_path), file_size


async def delete_file(file_path: str) -> bool:
    """
    Delete file from disk.
    
    Args:
        file_path: Path to file
    
    Returns:
        True if deleted successfully, False otherwise
    
    Example:
        >>> await delete_file("uploads/file.csv")
        True
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False


def get_file_extension(filename: str) -> str:
    """
    Get file extension without dot.
    
    Args:
        filename: Name of the file
    
    Returns:
        Extension without dot (e.g., 'csv', 'xlsx')
    
    Example:
        >>> get_file_extension("data.csv")
        'csv'
    """
    return Path(filename).suffix.lower().lstrip('.')


# What's happening here?
# ----------------------
# 1. File Validation:
#    - Check extension against whitelist
#    - Check file size during upload
#    - Prevent malicious files
#
# 2. Unique Filenames:
#    - UUID prevents collisions
#    - Original extension preserved
#    - Unpredictable (security)
#
# 3. Async File Operations:
#    - Non-blocking I/O
#    - Chunked reading (memory efficient)
#    - Progress tracking possible
#
# 4. Error Handling:
#    - Invalid extension → 400
#    - File too large → 413
#    - Partial file cleanup
#
# 5. Security:
#    - Whitelist extensions only
#    - Size limits enforced
#    - Unique names prevent overwrites
#    - No path traversal (UUID names)
#
# 6. Storage Strategy:
#    - Local filesystem (simple)
#    - Could be S3/Cloud later
#    - Organized in uploads/ dir
#
# Why aiofiles?
# - Async file I/O
# - Non-blocking operations
# - Better performance under load
# - Integrates with FastAPI async
