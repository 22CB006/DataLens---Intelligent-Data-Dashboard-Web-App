"""
Statistical Analyzer Service

Comprehensive statistical analysis for datasets.

What you'll learn:
- Descriptive statistics
- Correlation analysis
- Outlier detection
- Trend analysis
- Data aggregation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from scipy import stats


def calculate_descriptive_statistics(df: pd.DataFrame, include_distributions: bool = True) -> Dict:
    """
    Calculate comprehensive descriptive statistics.
    
    Args:
        df: pandas DataFrame
        include_distributions: Whether to include histogram/distribution data
    
    Returns:
        Dictionary with statistics for each numeric column and optional distributions
    
    Example:
        >>> stats = calculate_descriptive_statistics(df)
        >>> print(stats['column_name']['mean'])
    
    Statistics Included:
        - count, mean, std, min, max
        - 25th, 50th, 75th percentiles
        - skewness, kurtosis
        - variance, range
        - distributions (histogram data)
    """
    numeric_df = df.select_dtypes(include=['number'])
    
    if numeric_df.empty:
        return {'error': 'No numeric columns found'}
    
    statistics = {}
    distributions = {}
    
    for col in numeric_df.columns:
        col_data = numeric_df[col].dropna()
        
        if len(col_data) == 0:
            continue
        
        statistics[col] = {
            'count': int(col_data.count()),
            'mean': float(col_data.mean()),
            'median': float(col_data.median()),
            'mode': float(col_data.mode()[0]) if not col_data.mode().empty else None,
            'std': float(col_data.std()),
            'variance': float(col_data.var()),
            'min': float(col_data.min()),
            'max': float(col_data.max()),
            'range': float(col_data.max() - col_data.min()),
            'q25': float(col_data.quantile(0.25)),
            'q50': float(col_data.quantile(0.50)),
            'q75': float(col_data.quantile(0.75)),
            'iqr': float(col_data.quantile(0.75) - col_data.quantile(0.25)),
            'skewness': float(col_data.skew()),
            'kurtosis': float(col_data.kurtosis()),
            'missing_count': int(numeric_df[col].isna().sum()),
            'missing_percentage': float((numeric_df[col].isna().sum() / len(numeric_df)) * 100)
        }
        
        # Generate distribution/histogram data
        if include_distributions:
            # Determine optimal number of bins using Sturges' rule
            n_bins = min(int(np.ceil(np.log2(len(col_data)) + 1)), 20)
            
            # Create histogram
            counts, bin_edges = np.histogram(col_data, bins=n_bins)
            
            # Create bin labels (midpoints)
            bin_labels = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges)-1)]
            
            distributions[col] = {
                'labels': [f'{label:.2f}' for label in bin_labels],
                'values': [int(count) for count in counts],
                'bins': n_bins,
                'bin_edges': [float(edge) for edge in bin_edges]
            }
    
    result = {'statistics': statistics}
    if include_distributions:
        result['distributions'] = distributions
    
    return result


def calculate_correlation_matrix(df: pd.DataFrame, method: str = 'pearson') -> Dict:
    """
    Calculate correlation matrix for numeric columns.
    
    Args:
        df: pandas DataFrame
        method: 'pearson', 'spearman', or 'kendall'
    
    Returns:
        Dictionary with correlation matrix and significant pairs
    
    Example:
        >>> corr = calculate_correlation_matrix(df)
        >>> print(corr['matrix'])
    
    Methods:
        - pearson: Linear correlation (-1 to 1)
        - spearman: Rank correlation
        - kendall: Ordinal correlation
    """
    numeric_df = df.select_dtypes(include=['number'])
    
    if numeric_df.empty or len(numeric_df.columns) < 2:
        return {'error': 'Need at least 2 numeric columns'}
    
    # Calculate correlation matrix
    corr_matrix = numeric_df.corr(method=method)
    
    # Convert to dictionary format
    corr_dict = corr_matrix.to_dict()
    
    # Find strong correlations (|r| > 0.7, excluding diagonal)
    strong_correlations = []
    for i, col1 in enumerate(corr_matrix.columns):
        for j, col2 in enumerate(corr_matrix.columns):
            if i < j:  # Only upper triangle
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'column1': col1,
                        'column2': col2,
                        'correlation': float(corr_value),
                        'strength': 'strong positive' if corr_value > 0.7 else 'strong negative'
                    })
    
    return {
        'matrix': corr_dict,
        'columns': corr_matrix.columns.tolist(),
        'method': method,
        'strong_correlations': strong_correlations
    }


def detect_outliers(df: pd.DataFrame, method: str = 'iqr', threshold: float = 1.5) -> Dict:
    """
    Detect outliers in numeric columns.
    
    Args:
        df: pandas DataFrame
        method: 'iqr' or 'zscore'
        threshold: IQR multiplier (default: 1.5) or Z-score threshold (default: 3)
    
    Returns:
        Dictionary with outliers for each column
    
    Example:
        >>> outliers = detect_outliers(df, method='iqr')
        >>> print(outliers['column_name']['count'])
    
    Methods:
        - IQR: Values beyond Q1 - 1.5*IQR or Q3 + 1.5*IQR
        - Z-score: Values with |z| > threshold (default: 3)
    """
    numeric_df = df.select_dtypes(include=['number'])
    
    if numeric_df.empty:
        return {'error': 'No numeric columns found'}
    
    outliers_info = {}
    
    for col in numeric_df.columns:
        col_data = numeric_df[col].dropna()
        
        if len(col_data) == 0:
            continue
        
        if method == 'iqr':
            # IQR method
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
        
        elif method == 'zscore':
            # Z-score method
            z_scores = np.abs(stats.zscore(col_data))
            outliers = col_data[z_scores > threshold]
        
        else:
            continue
        
        outliers_info[col] = {
            'count': int(len(outliers)),
            'percentage': float((len(outliers) / len(col_data)) * 100),
            'values': outliers.tolist()[:100],  # Limit to 100 for response size
            'min_outlier': float(outliers.min()) if len(outliers) > 0 else None,
            'max_outlier': float(outliers.max()) if len(outliers) > 0 else None,
            'method': method,
            'threshold': threshold
        }
        
        if method == 'iqr':
            outliers_info[col]['lower_bound'] = float(lower_bound)
            outliers_info[col]['upper_bound'] = float(upper_bound)
    
    return outliers_info


def analyze_trends(df: pd.DataFrame, date_column: Optional[str] = None, value_column: Optional[str] = None) -> Dict:
    """
    Analyze trends in time series data.
    
    Args:
        df: pandas DataFrame
        date_column: Name of date column (auto-detect if None)
        value_column: Name of value column (auto-detect if None)
    
    Returns:
        Dictionary with trend analysis
    
    Example:
        >>> trends = analyze_trends(df, 'date', 'sales')
        >>> print(trends['direction'])
    
    Analysis:
        - Overall trend (increasing/decreasing/stable)
        - Moving averages (7-day, 30-day)
        - Growth rate
        - Seasonality indicators
    """
    # Auto-detect date column if not provided
    if date_column is None:
        date_cols = df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) == 0:
            # Try to convert string columns to datetime
            for col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_column = col
                    break
                except:
                    continue
        else:
            date_column = date_cols[0]
    
    if date_column is None:
        return {'error': 'No date column found'}
    
    # Auto-detect value column if not provided
    if value_column is None:
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            return {'error': 'No numeric column found'}
        value_column = numeric_cols[0]
    
    # Sort by date
    df_sorted = df[[date_column, value_column]].sort_values(date_column).dropna()
    
    if len(df_sorted) < 2:
        return {'error': 'Not enough data points for trend analysis'}
    
    # Calculate moving averages
    values = df_sorted[value_column]
    ma_7 = values.rolling(window=min(7, len(values))).mean().tolist()
    ma_30 = values.rolling(window=min(30, len(values))).mean().tolist()
    
    # Calculate trend direction using linear regression
    x = np.arange(len(values))
    y = values.values
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Determine trend direction
    if slope > 0.01:
        direction = 'increasing'
    elif slope < -0.01:
        direction = 'decreasing'
    else:
        direction = 'stable'
    
    # Calculate growth rate
    if len(values) > 1:
        first_value = values.iloc[0]
        last_value = values.iloc[-1]
        if first_value != 0:
            growth_rate = ((last_value - first_value) / first_value) * 100
        else:
            growth_rate = 0
    else:
        growth_rate = 0
    
    return {
        'date_column': date_column,
        'value_column': value_column,
        'data_points': len(df_sorted),
        'direction': direction,
        'slope': float(slope),
        'r_squared': float(r_value ** 2),
        'p_value': float(p_value),
        'growth_rate_percentage': float(growth_rate),
        'moving_average_7': [float(x) if not pd.isna(x) else None for x in ma_7],
        'moving_average_30': [float(x) if not pd.isna(x) else None for x in ma_30],
        'start_value': float(values.iloc[0]),
        'end_value': float(values.iloc[-1]),
        'min_value': float(values.min()),
        'max_value': float(values.max()),
        'mean_value': float(values.mean())
    }


def generate_summary_report(df: pd.DataFrame) -> Dict:
    """
    Generate comprehensive summary report.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Dictionary with complete dataset summary
    
    Example:
        >>> report = generate_summary_report(df)
        >>> print(report['overview'])
    """
    return {
        'overview': {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'numeric_columns': len(df.select_dtypes(include=['number']).columns),
            'categorical_columns': len(df.select_dtypes(include=['object', 'category']).columns),
            'datetime_columns': len(df.select_dtypes(include=['datetime64']).columns),
            'missing_cells': int(df.isna().sum().sum()),
            'missing_percentage': float((df.isna().sum().sum() / (len(df) * len(df.columns))) * 100),
            'duplicate_rows': int(df.duplicated().sum()),
            'memory_usage_mb': float(df.memory_usage(deep=True).sum() / (1024 * 1024))
        },
        'statistics': calculate_descriptive_statistics(df),
        'data_quality': {
            'completeness': float(100 - (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100),
            'uniqueness': float((len(df) - df.duplicated().sum()) / len(df) * 100) if len(df) > 0 else 0
        }
    }


# What's happening here?
# ----------------------
# 1. Descriptive Statistics:
#    - Central tendency (mean, median, mode)
#    - Dispersion (std, variance, range)
#    - Distribution shape (skewness, kurtosis)
#    - Quartiles and IQR
#
# 2. Correlation Analysis:
#    - Pearson (linear relationships)
#    - Spearman (monotonic relationships)
#    - Identifies strong correlations
#    - Matrix format for heatmaps
#
# 3. Outlier Detection:
#    - IQR method (robust to extremes)
#    - Z-score method (assumes normal distribution)
#    - Configurable thresholds
#    - Returns outlier values and bounds
#
# 4. Trend Analysis:
#    - Time series analysis
#    - Moving averages (smoothing)
#    - Linear regression (trend direction)
#    - Growth rate calculation
#
# 5. Summary Report:
#    - Complete dataset overview
#    - Data quality metrics
#    - Combines all analyses
#    - Ready for dashboard display
#
# Why scipy.stats?
# - Statistical functions
# - Linear regression
# - Z-score calculation
# - Hypothesis testing
# - Complements pandas
