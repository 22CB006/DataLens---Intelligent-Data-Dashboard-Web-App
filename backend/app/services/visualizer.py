"""
Data Visualizer Service

Generates visualization-ready data for frontend charts.

What you'll learn:
- Data preparation for charts
- Chart type selection
- Data aggregation
- JSON serialization
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


def prepare_bar_chart_data(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    aggregation: str = 'sum',
    limit: int = 20
) -> Dict:
    """
    Prepare data for bar chart.
    
    Args:
        df: pandas DataFrame
        x_column: Column for x-axis (categories)
        y_column: Column for y-axis (values)
        aggregation: 'sum', 'mean', 'count', 'max', 'min'
        limit: Maximum number of bars
    
    Returns:
        Dictionary with labels and values
    
    Example:
        >>> data = prepare_bar_chart_data(df, 'category', 'sales', 'sum')
        >>> print(data['labels'], data['values'])
    """
    if x_column not in df.columns or y_column not in df.columns:
        return {'error': 'Column not found'}
    
    # Group and aggregate
    if aggregation == 'sum':
        grouped = df.groupby(x_column)[y_column].sum()
    elif aggregation == 'mean':
        grouped = df.groupby(x_column)[y_column].mean()
    elif aggregation == 'count':
        grouped = df.groupby(x_column)[y_column].count()
    elif aggregation == 'max':
        grouped = df.groupby(x_column)[y_column].max()
    elif aggregation == 'min':
        grouped = df.groupby(x_column)[y_column].min()
    else:
        return {'error': f'Unknown aggregation: {aggregation}'}
    
    # Sort by value descending and limit
    grouped = grouped.sort_values(ascending=False).head(limit)
    
    return {
        'type': 'bar',
        'labels': grouped.index.tolist(),
        'values': grouped.values.tolist(),
        'aggregation': aggregation,
        'x_column': x_column,
        'y_column': y_column
    }


def prepare_line_chart_data(
    df: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    sort_by_x: bool = True
) -> Dict:
    """
    Prepare data for line chart.
    
    Args:
        df: pandas DataFrame
        x_column: Column for x-axis (usually time/date)
        y_columns: List of columns for y-axis (multiple lines)
        sort_by_x: Sort data by x-axis
    
    Returns:
        Dictionary with x values and multiple y series
    
    Example:
        >>> data = prepare_line_chart_data(df, 'date', ['sales', 'profit'])
    """
    if x_column not in df.columns:
        return {'error': f'Column {x_column} not found'}
    
    for col in y_columns:
        if col not in df.columns:
            return {'error': f'Column {col} not found'}
    
    # Select relevant columns
    plot_df = df[[x_column] + y_columns].dropna()
    
    # Sort by x if requested
    if sort_by_x:
        plot_df = plot_df.sort_values(x_column)
    
    # Prepare data
    result = {
        'type': 'line',
        'x_values': plot_df[x_column].tolist(),
        'series': []
    }
    
    for col in y_columns:
        result['series'].append({
            'name': col,
            'values': plot_df[col].tolist()
        })
    
    return result


def prepare_pie_chart_data(
    df: pd.DataFrame,
    category_column: str,
    value_column: Optional[str] = None,
    top_n: int = 10
) -> Dict:
    """
    Prepare data for pie chart.
    
    Args:
        df: pandas DataFrame
        category_column: Column for pie slices
        value_column: Column for slice sizes (None = count)
        top_n: Show top N categories, group rest as "Other"
    
    Returns:
        Dictionary with labels and values
    
    Example:
        >>> data = prepare_pie_chart_data(df, 'category', 'revenue', top_n=5)
    """
    if category_column not in df.columns:
        return {'error': f'Column {category_column} not found'}
    
    if value_column is None:
        # Count occurrences
        grouped = df[category_column].value_counts()
    else:
        if value_column not in df.columns:
            return {'error': f'Column {value_column} not found'}
        # Sum values
        grouped = df.groupby(category_column)[value_column].sum().sort_values(ascending=False)
    
    # Take top N
    top_categories = grouped.head(top_n)
    
    # Group remaining as "Other"
    if len(grouped) > top_n:
        other_value = grouped.iloc[top_n:].sum()
        labels = top_categories.index.tolist() + ['Other']
        values = top_categories.values.tolist() + [other_value]
    else:
        labels = top_categories.index.tolist()
        values = top_categories.values.tolist()
    
    return {
        'type': 'pie',
        'labels': labels,
        'values': values,
        'category_column': category_column,
        'value_column': value_column or 'count'
    }


def prepare_scatter_plot_data(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    color_column: Optional[str] = None,
    size_column: Optional[str] = None,
    sample_size: Optional[int] = 1000
) -> Dict:
    """
    Prepare data for scatter plot.
    
    Args:
        df: pandas DataFrame
        x_column: Column for x-axis
        y_column: Column for y-axis
        color_column: Column for point colors (optional)
        size_column: Column for point sizes (optional)
        sample_size: Limit points for performance
    
    Returns:
        Dictionary with x, y, and optional color/size data
    
    Example:
        >>> data = prepare_scatter_plot_data(df, 'age', 'income', color_column='gender')
    """
    if x_column not in df.columns or y_column not in df.columns:
        return {'error': 'Column not found'}
    
    # Select columns
    cols = [x_column, y_column]
    if color_column and color_column in df.columns:
        cols.append(color_column)
    if size_column and size_column in df.columns:
        cols.append(size_column)
    
    plot_df = df[cols].dropna()
    
    # Sample if too many points
    if sample_size and len(plot_df) > sample_size:
        plot_df = plot_df.sample(n=sample_size, random_state=42)
    
    result = {
        'type': 'scatter',
        'x_values': plot_df[x_column].tolist(),
        'y_values': plot_df[y_column].tolist(),
        'x_column': x_column,
        'y_column': y_column,
        'point_count': len(plot_df)
    }
    
    if color_column and color_column in plot_df.columns:
        result['colors'] = plot_df[color_column].tolist()
        result['color_column'] = color_column
    
    if size_column and size_column in plot_df.columns:
        result['sizes'] = plot_df[size_column].tolist()
        result['size_column'] = size_column
    
    return result


def prepare_heatmap_data(
    df: pd.DataFrame,
    method: str = 'correlation'
) -> Dict:
    """
    Prepare data for heatmap.
    
    Args:
        df: pandas DataFrame
        method: 'correlation' or 'pivot'
    
    Returns:
        Dictionary with heatmap data
    
    Example:
        >>> data = prepare_heatmap_data(df, method='correlation')
    """
    if method == 'correlation':
        # Correlation heatmap
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty or len(numeric_df.columns) < 2:
            return {'error': 'Need at least 2 numeric columns'}
        
        corr_matrix = numeric_df.corr()
        
        return {
            'type': 'heatmap',
            'method': 'correlation',
            'x_labels': corr_matrix.columns.tolist(),
            'y_labels': corr_matrix.index.tolist(),
            'values': corr_matrix.values.tolist(),
            'min_value': float(corr_matrix.min().min()),
            'max_value': float(corr_matrix.max().max())
        }
    
    else:
        return {'error': f'Unknown method: {method}'}


def prepare_histogram_data(
    df: pd.DataFrame,
    column: str,
    bins: int = 20
) -> Dict:
    """
    Prepare data for histogram.
    
    Args:
        df: pandas DataFrame
        column: Column to plot
        bins: Number of bins
    
    Returns:
        Dictionary with histogram data
    
    Example:
        >>> data = prepare_histogram_data(df, 'age', bins=10)
    """
    if column not in df.columns:
        return {'error': f'Column {column} not found'}
    
    col_data = df[column].dropna()
    
    if not pd.api.types.is_numeric_dtype(col_data):
        return {'error': f'Column {column} is not numeric'}
    
    # Calculate histogram
    counts, bin_edges = np.histogram(col_data, bins=bins)
    
    # Create bin labels
    bin_labels = [f'{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}' for i in range(len(bin_edges)-1)]
    
    return {
        'type': 'histogram',
        'column': column,
        'labels': bin_labels,
        'values': counts.tolist(),
        'bin_edges': bin_edges.tolist(),
        'total_count': int(len(col_data)),
        'mean': float(col_data.mean()),
        'median': float(col_data.median()),
        'std': float(col_data.std())
    }


def suggest_chart_type(df: pd.DataFrame, x_column: str, y_column: Optional[str] = None) -> Dict:
    """
    Suggest appropriate chart type based on data.
    
    Args:
        df: pandas DataFrame
        x_column: First column
        y_column: Second column (optional)
    
    Returns:
        Dictionary with chart suggestion and reasoning
    
    Example:
        >>> suggestion = suggest_chart_type(df, 'date', 'sales')
        >>> print(suggestion['chart_type'])
    
    Logic:
        - Datetime + Numeric → Line chart
        - Categorical + Numeric → Bar chart
        - Numeric + Numeric → Scatter plot
        - Single Categorical → Pie chart
        - Single Numeric → Histogram
    """
    if x_column not in df.columns:
        return {'error': f'Column {x_column} not found'}
    
    x_dtype = df[x_column].dtype
    
    if y_column is None:
        # Single column
        if pd.api.types.is_numeric_dtype(x_dtype):
            return {
                'chart_type': 'histogram',
                'reasoning': 'Single numeric column - distribution analysis',
                'recommended': True
            }
        else:
            return {
                'chart_type': 'pie',
                'reasoning': 'Single categorical column - proportion analysis',
                'recommended': True
            }
    
    else:
        # Two columns
        if y_column not in df.columns:
            return {'error': f'Column {y_column} not found'}
        
        y_dtype = df[y_column].dtype
        
        # Datetime + Numeric → Line chart
        if pd.api.types.is_datetime64_any_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
            return {
                'chart_type': 'line',
                'reasoning': 'Time series data - trend analysis',
                'recommended': True
            }
        
        # Categorical + Numeric → Bar chart
        elif not pd.api.types.is_numeric_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
            return {
                'chart_type': 'bar',
                'reasoning': 'Categorical vs numeric - comparison analysis',
                'recommended': True
            }
        
        # Numeric + Numeric → Scatter plot
        elif pd.api.types.is_numeric_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
            return {
                'chart_type': 'scatter',
                'reasoning': 'Two numeric columns - correlation analysis',
                'recommended': True
            }
        
        else:
            return {
                'chart_type': 'bar',
                'reasoning': 'Default choice for mixed types',
                'recommended': False
            }


# What's happening here?
# ----------------------
# 1. Chart Data Preparation:
#    - Each function returns JSON-ready data
#    - Handles missing values
#    - Optimizes for frontend rendering
#    - Includes metadata
#
# 2. Bar Charts:
#    - Aggregation support (sum, mean, count)
#    - Sorting by value
#    - Limit for readability
#    - Category-value pairs
#
# 3. Line Charts:
#    - Multiple series support
#    - Time series friendly
#    - Sorted by x-axis
#    - Handles dates
#
# 4. Pie Charts:
#    - Top N categories
#    - "Other" grouping
#    - Count or sum values
#    - Percentage-ready
#
# 5. Scatter Plots:
#    - Optional color/size dimensions
#    - Sampling for performance
#    - Correlation visualization
#    - Multi-dimensional data
#
# 6. Heatmaps:
#    - Correlation matrices
#    - Color scale data
#    - Label arrays
#    - 2D data format
#
# 7. Histograms:
#    - Distribution analysis
#    - Configurable bins
#    - Statistical summary
#    - Frequency data
#
# 8. Smart Suggestions:
#    - Analyzes data types
#    - Recommends chart type
#    - Explains reasoning
#    - Helps users choose
#
# Why this approach?
# - Frontend-agnostic (works with any charting library)
# - JSON-serializable
# - Optimized data transfer
# - Flexible and extensible
