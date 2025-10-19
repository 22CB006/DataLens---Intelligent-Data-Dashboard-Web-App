"""
Data Analysis API Routes

This module handles data analysis and statistics endpoints.

What you'll learn:
- Complex data processing endpoints
- Statistical analysis APIs
- Response formatting
- Error handling

Endpoints:
- GET /{dataset_id}/statistics - Descriptive statistics
- GET /{dataset_id}/correlation - Correlation analysis
- GET /{dataset_id}/outliers - Outlier detection
- GET /{dataset_id}/trends - Trend analysis
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services import dataset_service
from app.services.file_handler import get_file_extension
from app.services.data_processor import read_dataset
from app.services.analyzer import (
    calculate_descriptive_statistics,
    calculate_correlation_matrix,
    detect_outliers as detect_outliers_func,
    analyze_trends as analyze_trends_func,
    generate_summary_report
)
from app.services.visualizer import (
    prepare_bar_chart_data,
    prepare_line_chart_data,
    prepare_pie_chart_data,
    prepare_scatter_plot_data,
    prepare_heatmap_data,
    prepare_histogram_data,
    suggest_chart_type
)

# Create router for analysis endpoints
router = APIRouter()


@router.get("/{dataset_id}/statistics")
async def get_statistics(
    dataset_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get descriptive statistics for dataset.
    
    **Path Parameters:**
    - dataset_id: UUID of the dataset
    
    **Returns:**
    - For each numeric column:
      - count, mean, median, mode
      - std, variance, min, max, range
      - quartiles (25%, 50%, 75%), IQR
      - skewness, kurtosis
      - missing count and percentage
    
    **Raises:**
    - 401: Not authenticated
    - 404: Dataset not found
    - 403: Not authorized
    """
    # Get and verify dataset
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Read and analyze
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    stats = calculate_descriptive_statistics(df)
    
    return stats


@router.get("/{dataset_id}/correlation")
async def get_correlation(
    dataset_id: str,
    method: str = Query('pearson', regex='^(pearson|spearman|kendall)$'),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get correlation matrix for numeric columns.
    
    **Path Parameters:**
    - dataset_id: UUID of the dataset
    
    **Query Parameters:**
    - method: pearson, spearman, or kendall (default: pearson)
    
    **Returns:**
    - matrix: Correlation matrix
    - columns: Column names
    - strong_correlations: Pairs with |r| > 0.7
    
    **Raises:**
    - 401: Not authenticated
    - 404: Dataset not found
    - 403: Not authorized
    """
    # Get and verify dataset
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Read and analyze
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    corr = calculate_correlation_matrix(df, method=method)
    
    return corr


@router.get("/{dataset_id}/outliers")
async def detect_outliers(
    dataset_id: str,
    method: str = Query('iqr', regex='^(iqr|zscore)$'),
    threshold: float = Query(1.5, gt=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Detect outliers in numeric columns.
    
    **Path Parameters:**
    - dataset_id: UUID of the dataset
    
    **Query Parameters:**
    - method: iqr or zscore (default: iqr)
    - threshold: 1.5 for IQR, 3 for zscore (default: 1.5)
    
    **Returns:**
    - For each column: count, percentage, values, bounds
    
    **Raises:**
    - 401: Not authenticated
    - 404: Dataset not found
    - 403: Not authorized
    """
    # Get and verify dataset
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Read and analyze
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    outliers = detect_outliers_func(df, method=method, threshold=threshold)
    
    return outliers


@router.get("/{dataset_id}/trends")
async def analyze_trends(
    dataset_id: str,
    date_column: Optional[str] = None,
    value_column: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze trends in time-series data.
    
    **Path Parameters:**
    - dataset_id: UUID of the dataset
    
    **Query Parameters:**
    - date_column: Date column (auto-detect if None)
    - value_column: Value column (auto-detect if None)
    
    **Returns:**
    - direction, slope, growth_rate
    - moving averages (7-day, 30-day)
    - statistical significance
    
    **Raises:**
    - 401: Not authenticated
    - 404: Dataset not found
    - 403: Not authorized
    """
    # Get and verify dataset
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Read and analyze
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    trends = analyze_trends_func(df, date_column=date_column, value_column=value_column)
    
    return trends


@router.get("/{dataset_id}/summary")
async def get_summary(
    dataset_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive summary report.
    
    **Returns:**
    - Overview (rows, columns, types, missing data)
    - Statistics for all numeric columns
    - Data quality metrics
    """
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    summary = generate_summary_report(df)
    
    return summary


@router.post("/{dataset_id}/visualize/bar")
async def create_bar_chart(
    dataset_id: str,
    x_column: str = Query(...),
    y_column: str = Query(...),
    aggregation: str = Query('sum', regex='^(sum|mean|count|max|min)$'),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate bar chart data."""
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    chart_data = prepare_bar_chart_data(df, x_column, y_column, aggregation, limit)
    
    return chart_data


@router.post("/{dataset_id}/visualize/line")
async def create_line_chart(
    dataset_id: str,
    x_column: str = Query(...),
    y_columns: str = Query(...),  # Comma-separated
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate line chart data."""
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    y_cols = [col.strip() for col in y_columns.split(',')]
    chart_data = prepare_line_chart_data(df, x_column, y_cols)
    
    return chart_data


@router.post("/{dataset_id}/visualize/pie")
async def create_pie_chart(
    dataset_id: str,
    category_column: str = Query(...),
    value_column: Optional[str] = None,
    top_n: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate pie chart data."""
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    chart_data = prepare_pie_chart_data(df, category_column, value_column, top_n)
    
    return chart_data


@router.post("/{dataset_id}/visualize/scatter")
async def create_scatter_plot(
    dataset_id: str,
    x_column: str = Query(...),
    y_column: str = Query(...),
    color_column: Optional[str] = None,
    size_column: Optional[str] = None,
    sample_size: int = Query(1000, ge=100, le=10000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate scatter plot data."""
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    chart_data = prepare_scatter_plot_data(df, x_column, y_column, color_column, size_column, sample_size)
    
    return chart_data


@router.get("/{dataset_id}/visualize/heatmap")
async def create_heatmap(
    dataset_id: str,
    method: str = Query('correlation'),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate heatmap data (correlation matrix)."""
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    chart_data = prepare_heatmap_data(df, method=method)
    
    return chart_data


@router.post("/{dataset_id}/visualize/histogram")
async def create_histogram(
    dataset_id: str,
    column: str = Query(...),
    bins: int = Query(20, ge=5, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate histogram data."""
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    chart_data = prepare_histogram_data(df, column, bins)
    
    return chart_data


@router.get("/{dataset_id}/visualize/suggest")
async def suggest_chart(
    dataset_id: str,
    x_column: str = Query(...),
    y_column: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Suggest appropriate chart type based on data types."""
    dataset = await dataset_service.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if str(dataset.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_type = get_file_extension(dataset.filename)
    df = read_dataset(dataset.file_path, file_type)
    suggestion = suggest_chart_type(df, x_column, y_column)
    
    return suggestion


# What's happening here?
# ----------------------
# 1. All endpoints use path parameter {dataset_id}
# 2. Some endpoints accept query parameters for customization
# 3. Each endpoint performs specific statistical analysis
# 4. Results are formatted as JSON for easy consumption
# 5. Comprehensive error handling for edge cases
#
# These endpoints will use:
# - Pandas for data manipulation
# - NumPy for numerical operations
# - SciPy for statistical functions
#
# Example URLs:
# - GET /api/v1/analysis/abc-123/statistics
# - GET /api/v1/analysis/abc-123/correlation?method=pearson
# - GET /api/v1/analysis/abc-123/outliers?method=zscore&threshold=3
# - GET /api/v1/analysis/abc-123/trends?date_column=date&value_column=sales
