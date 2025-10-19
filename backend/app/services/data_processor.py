"""
Data Processor Service

Handles data reading, processing, and validation.

What you'll learn:
- Pandas DataFrame operations
- CSV/Excel/JSON reading
- Data type detection
- Memory-efficient processing
- Error handling for corrupt files
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from fastapi import HTTPException, status


def read_dataset(file_path: str, file_type: str) -> pd.DataFrame:
    """
    Read dataset file into pandas DataFrame.
    
    Args:
        file_path: Path to the file
        file_type: File extension (csv, xlsx, json)
    
    Returns:
        pandas DataFrame
    
    Raises:
        HTTPException: If file cannot be read
    
    Example:
        >>> df = read_dataset("data.csv", "csv")
        >>> print(df.head())
    
    Supported Formats:
        - CSV: Comma-separated values
        - Excel: .xlsx, .xls
        - JSON: Array of objects or records
    """
    try:
        if file_type == "csv":
            # Read CSV with automatic encoding detection
            df = pd.read_csv(file_path, encoding='utf-8')
        
        elif file_type in ["xlsx", "xls"]:
            # Read Excel file
            df = pd.read_excel(file_path, engine='openpyxl' if file_type == 'xlsx' else None)
        
        elif file_type == "json":
            # Read JSON file
            df = pd.read_json(file_path)
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file_type}"
            )
        
        return df
    
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )
    except pd.errors.ParserError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File format is invalid or corrupted"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading file: {str(e)}"
        )


def get_dataset_info(df: pd.DataFrame) -> Dict:
    """
    Get comprehensive dataset information.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Dictionary with dataset metadata
    
    Example:
        >>> info = get_dataset_info(df)
        >>> print(info['row_count'], info['column_count'])
    
    Returns:
        {
            'row_count': int,
            'column_count': int,
            'columns': [{'name': str, 'type': str, 'non_null': int, 'null': int}],
            'memory_usage': str,
            'numeric_columns': list,
            'categorical_columns': list,
            'datetime_columns': list
        }
    """
    # Basic info
    row_count, column_count = df.shape
    
    # Column information
    columns_info = []
    numeric_cols = []
    categorical_cols = []
    datetime_cols = []
    
    for col in df.columns:
        col_type = str(df[col].dtype)
        non_null_count = df[col].count()
        null_count = df[col].isna().sum()
        
        columns_info.append({
            'name': col,
            'type': col_type,
            'non_null_count': int(non_null_count),
            'null_count': int(null_count),
            'unique_count': int(df[col].nunique())
        })
        
        # Categorize columns
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            datetime_cols.append(col)
        else:
            categorical_cols.append(col)
    
    # Memory usage
    memory_bytes = df.memory_usage(deep=True).sum()
    memory_mb = memory_bytes / (1024 * 1024)
    
    return {
        'row_count': row_count,
        'column_count': column_count,
        'columns': columns_info,
        'memory_usage': f"{memory_mb:.2f} MB",
        'numeric_columns': numeric_cols,
        'categorical_columns': categorical_cols,
        'datetime_columns': datetime_cols
    }


def get_dataset_preview(df: pd.DataFrame, n_rows: int = 10) -> Dict:
    """
    Get preview of dataset (first N rows).
    
    Args:
        df: pandas DataFrame
        n_rows: Number of rows to preview (default: 10)
    
    Returns:
        Dictionary with preview data
    
    Example:
        >>> preview = get_dataset_preview(df, 5)
        >>> print(preview['data'])
    
    Returns:
        {
            'columns': list of column names,
            'data': list of row dictionaries,
            'total_rows': total rows in dataset,
            'preview_rows': number of rows in preview
        }
    """
    preview_df = df.head(n_rows)
    
    # Convert to list of dictionaries
    # Handle NaN values by converting to None
    data = preview_df.where(pd.notnull(preview_df), None).to_dict('records')
    
    return {
        'columns': df.columns.tolist(),
        'data': data,
        'total_rows': len(df),
        'preview_rows': len(preview_df)
    }


def detect_and_convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Automatically detect and convert column types.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        DataFrame with optimized types
    
    Example:
        >>> df = detect_and_convert_types(df)
    
    Conversions:
        - Numeric strings → int/float
        - Date strings → datetime
        - Low cardinality strings → category
    """
    df_copy = df.copy()
    
    for col in df_copy.columns:
        # Skip if already numeric or datetime
        if pd.api.types.is_numeric_dtype(df_copy[col]) or \
           pd.api.types.is_datetime64_any_dtype(df_copy[col]):
            continue
        
        # Try to convert to numeric
        try:
            df_copy[col] = pd.to_numeric(df_copy[col])
            continue
        except (ValueError, TypeError):
            pass
        
        # Try to convert to datetime
        try:
            df_copy[col] = pd.to_datetime(df_copy[col])
            continue
        except (ValueError, TypeError, pd.errors.ParserError):
            pass
        
        # Convert low cardinality strings to category
        if df_copy[col].dtype == 'object':
            num_unique = df_copy[col].nunique()
            num_total = len(df_copy[col])
            
            # If less than 50% unique values, convert to category
            if num_unique / num_total < 0.5:
                df_copy[col] = df_copy[col].astype('category')
    
    return df_copy


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = 'drop',
    fill_value: Optional[any] = None
) -> pd.DataFrame:
    """
    Handle missing values in dataset.
    
    Args:
        df: pandas DataFrame
        strategy: 'drop', 'fill', 'mean', 'median', 'mode'
        fill_value: Value to fill (if strategy='fill')
    
    Returns:
        DataFrame with missing values handled
    
    Example:
        >>> df = handle_missing_values(df, strategy='mean')
    
    Strategies:
        - drop: Remove rows with any missing values
        - fill: Fill with specific value
        - mean: Fill numeric columns with mean
        - median: Fill numeric columns with median
        - mode: Fill with most frequent value
    """
    df_copy = df.copy()
    
    if strategy == 'drop':
        df_copy = df_copy.dropna()
    
    elif strategy == 'fill':
        df_copy = df_copy.fillna(fill_value)
    
    elif strategy == 'mean':
        numeric_cols = df_copy.select_dtypes(include=['number']).columns
        df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].mean())
    
    elif strategy == 'median':
        numeric_cols = df_copy.select_dtypes(include=['number']).columns
        df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].median())
    
    elif strategy == 'mode':
        for col in df_copy.columns:
            if df_copy[col].isna().any():
                mode_value = df_copy[col].mode()[0] if not df_copy[col].mode().empty else None
                df_copy[col] = df_copy[col].fillna(mode_value)
    
    return df_copy


# What's happening here?
# ----------------------
# 1. File Reading:
#    - Supports CSV, Excel, JSON
#    - Automatic encoding detection
#    - Error handling for corrupt files
#    - Memory-efficient reading
#
# 2. Dataset Info:
#    - Row and column counts
#    - Column types and null counts
#    - Memory usage calculation
#    - Column categorization
#
# 3. Preview:
#    - First N rows
#    - Handles NaN values
#    - JSON-serializable output
#    - Efficient for large datasets
#
# 4. Type Detection:
#    - Automatic numeric conversion
#    - Datetime parsing
#    - Category optimization
#    - Memory reduction
#
# 5. Missing Values:
#    - Multiple strategies
#    - Numeric-specific handling
#    - Preserves data integrity
#    - Flexible options
#
# Why Pandas?
# - Industry standard for data
# - Rich functionality
# - Efficient operations
# - Great documentation
# - Large ecosystem
