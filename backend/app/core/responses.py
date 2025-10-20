"""
Success Response Helpers

This module provides helper functions to create consistent success responses
with user-friendly messages for frontend toast notifications.
"""

from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "Operation completed successfully",
    status_code: int = 200
) -> JSONResponse:
    """
    Create a success response with user-friendly message.
    
    Args:
        data: Response data
        message: User-friendly success message
        status_code: HTTP status code
    
    Returns:
        JSONResponse with data and success message
    """
    response_content = {
        "success": True,
        "message": message,
    }
    
    if data is not None:
        response_content["data"] = data
    
    return JSONResponse(
        status_code=status_code,
        content=response_content
    )


# Success message templates
class SuccessMessages:
    """User-friendly success messages for all operations."""
    
    # Authentication
    LOGIN_SUCCESS = "Welcome back! You've successfully logged in."
    REGISTER_SUCCESS = "Account created successfully! You can now log in."
    LOGOUT_SUCCESS = "You've been logged out successfully."
    
    # User Management
    PROFILE_UPDATED = "Your profile has been updated successfully."
    PROFILE_RETRIEVED = "Profile loaded successfully."
    USER_DELETED = "User account has been deleted successfully."
    PASSWORD_CHANGED = "Your password has been changed successfully."
    
    # Dataset Management
    DATASET_UPLOADED = "Dataset uploaded successfully! You can now analyze your data."
    DATASET_DELETED = "Dataset deleted successfully."
    DATASET_UPDATED = "Dataset updated successfully."
    DATASETS_RETRIEVED = "Datasets loaded successfully."
    DATASET_PREVIEW_LOADED = "Dataset preview loaded successfully."
    
    # Analysis
    STATISTICS_GENERATED = "Statistics calculated successfully."
    CORRELATION_GENERATED = "Correlation analysis completed successfully."
    OUTLIERS_DETECTED = "Outlier detection completed successfully."
    TRENDS_ANALYZED = "Trend analysis completed successfully."
    SUMMARY_GENERATED = "Summary report generated successfully."
    
    # Visualization
    CHART_GENERATED = "Chart data generated successfully."
    BAR_CHART_GENERATED = "Bar chart data ready for visualization."
    LINE_CHART_GENERATED = "Line chart data ready for visualization."
    PIE_CHART_GENERATED = "Pie chart data ready for visualization."
    SCATTER_PLOT_GENERATED = "Scatter plot data ready for visualization."
    HEATMAP_GENERATED = "Heatmap data ready for visualization."
    HISTOGRAM_GENERATED = "Histogram data ready for visualization."
    
    # General
    OPERATION_SUCCESS = "Operation completed successfully."
    DATA_SAVED = "Data saved successfully."
    DATA_LOADED = "Data loaded successfully."
