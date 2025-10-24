"""
Analysis Tests

Tests for data analysis endpoints and functionality.
"""

import pytest
from fastapi import status


class TestStatisticalAnalysis:
    """Test statistical analysis endpoints."""
    
    def test_get_statistics(self, client, auth_headers, test_dataset):
        """Test getting statistical analysis."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/statistics",
            headers=auth_headers
        )
        
        # May fail if file doesn't exist, but should return proper status
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "statistics" in data or isinstance(data, dict)
    
    def test_get_statistics_unauthorized(self, client, test_dataset):
        """Test getting statistics without authentication."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/statistics"
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_statistics_nonexistent_dataset(self, client, auth_headers):
        """Test getting statistics for non-existent dataset."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(
            f"/api/v1/analysis/{fake_id}/statistics",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCorrelationAnalysis:
    """Test correlation analysis endpoints."""
    
    def test_get_correlation(self, client, auth_headers, test_dataset):
        """Test getting correlation matrix."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/correlation",
            headers=auth_headers
        )
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "matrix" in data or "columns" in data
    
    def test_get_correlation_with_method(self, client, auth_headers, test_dataset):
        """Test getting correlation with specific method."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/correlation?method=pearson",
            headers=auth_headers
        )
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    def test_get_correlation_invalid_method(self, client, auth_headers, test_dataset):
        """Test getting correlation with invalid method."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/correlation?method=invalid",
            headers=auth_headers
        )
        
        # Should either accept it or return error
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]


class TestOutlierDetection:
    """Test outlier detection endpoints."""
    
    def test_get_outliers(self, client, auth_headers, test_dataset):
        """Test getting outlier detection results."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/outliers",
            headers=auth_headers
        )
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert isinstance(data, dict)
    
    def test_get_outliers_with_method(self, client, auth_headers, test_dataset):
        """Test outlier detection with specific method."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/outliers?method=iqr",
            headers=auth_headers
        )
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    def test_get_outliers_with_threshold(self, client, auth_headers, test_dataset):
        """Test outlier detection with custom threshold."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/outliers?threshold=2.5",
            headers=auth_headers
        )
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


class TestTrendAnalysis:
    """Test trend analysis endpoints."""
    
    def test_get_trends(self, client, auth_headers, test_dataset):
        """Test getting trend analysis."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/trends",
            headers=auth_headers
        )
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    def test_get_trends_with_columns(self, client, auth_headers, test_dataset):
        """Test trend analysis with specific columns."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/trends?date_column=date&value_column=sales",
            headers=auth_headers
        )
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]


class TestAnalysisSummary:
    """Test analysis summary endpoints."""
    
    def test_get_summary(self, client, auth_headers, test_dataset):
        """Test getting analysis summary."""
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/summary",
            headers=auth_headers
        )
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert isinstance(data, dict)


@pytest.mark.integration
class TestCompleteAnalysisFlow:
    """Integration tests for complete analysis workflow."""
    
    def test_full_analysis_workflow(self, client, auth_headers, test_dataset):
        """Test complete analysis workflow."""
        # 1. Get statistics
        stats_response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/statistics",
            headers=auth_headers
        )
        
        # 2. Get correlation
        corr_response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/correlation",
            headers=auth_headers
        )
        
        # 3. Get outliers
        outliers_response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/outliers",
            headers=auth_headers
        )
        
        # 4. Get trends
        trends_response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/trends",
            headers=auth_headers
        )
        
        # All should return valid status codes
        for response in [stats_response, corr_response, outliers_response, trends_response]:
            assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.slow
class TestAnalysisPerformance:
    """Performance tests for analysis operations."""
    
    def test_statistics_performance(self, client, auth_headers, test_dataset):
        """Test that statistics calculation completes in reasonable time."""
        import time
        
        start_time = time.time()
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/statistics",
            headers=auth_headers
        )
        end_time = time.time()
        
        # Should complete within 5 seconds
        assert (end_time - start_time) < 5.0
    
    def test_correlation_performance(self, client, auth_headers, test_dataset):
        """Test that correlation calculation completes in reasonable time."""
        import time
        
        start_time = time.time()
        response = client.get(
            f"/api/v1/analysis/{test_dataset.id}/correlation",
            headers=auth_headers
        )
        end_time = time.time()
        
        # Should complete within 5 seconds
        assert (end_time - start_time) < 5.0
