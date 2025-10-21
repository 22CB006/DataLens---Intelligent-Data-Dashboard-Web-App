/**
 * Analysis Service
 * 
 * Handles all analysis-related API calls
 */

import api from './api';

const analysisService = {
  /**
   * Run statistical analysis on a dataset
   */
  runAnalysis: async (datasetId) => {
    const response = await api.get(`/analysis/${datasetId}/statistics`);
    return response.data;
  },

  /**
   * Get analysis results for a dataset (statistics)
   */
  getAnalysis: async (datasetId) => {
    const response = await api.get(`/analysis/${datasetId}/statistics`);
    return response.data;
  },

  /**
   * Get correlation matrix
   */
  getCorrelation: async (datasetId) => {
    const response = await api.get(`/analysis/${datasetId}/correlation`);
    return response.data;
  },

  /**
   * Detect outliers in dataset
   */
  detectOutliers: async (datasetId) => {
    const response = await api.get(`/analysis/${datasetId}/outliers`);
    return response.data;
  },

  /**
   * Get outliers (alias for detectOutliers)
   */
  getOutliers: async (datasetId) => {
    const response = await api.get(`/analysis/${datasetId}/outliers`);
    return response.data;
  },

  /**
   * Get trend analysis
   */
  getTrends: async (datasetId, column) => {
    const response = await api.get(`/analysis/${datasetId}/trends`, {
      params: { column },
    });
    return response.data;
  },

  /**
   * Export analysis results
   */
  exportAnalysis: async (datasetId, format = 'pdf') => {
    const response = await api.get(`/analysis/${datasetId}/export`, {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },
};

export default analysisService;
