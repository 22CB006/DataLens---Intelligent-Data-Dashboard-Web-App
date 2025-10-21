/**
 * Dataset Service
 * 
 * Handles all dataset-related API calls
 */

import api from './api';

const datasetService = {
  /**
   * Upload a new dataset
   */
  uploadDataset: async (file, onUploadProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/datasets/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onUploadProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onUploadProgress(percentCompleted);
        }
      },
    });

    return response.data;
  },

  /**
   * Get all datasets for current user
   */
  getDatasets: async () => {
    const response = await api.get('/datasets/');
    return response.data;
  },

  /**
   * Get a specific dataset by ID
   */
  getDataset: async (datasetId) => {
    const response = await api.get(`/datasets/${datasetId}`);
    return response.data;
  },

  /**
   * Get dataset preview (first few rows)
   */
  getDatasetPreview: async (datasetId, rows = 10) => {
    const response = await api.get(`/datasets/${datasetId}/preview`, {
      params: { rows },
    });
    return response.data;
  },

  /**
   * Delete a dataset
   */
  deleteDataset: async (datasetId) => {
    const response = await api.delete(`/datasets/${datasetId}`);
    return response.data;
  },

  /**
   * Get dataset statistics
   */
  getDatasetStats: async (datasetId) => {
    const response = await api.get(`/datasets/${datasetId}/stats`);
    return response.data;
  },

  /**
   * Rename a dataset
   */
  renameDataset: async (datasetId, newFilename) => {
    const response = await api.put(`/datasets/${datasetId}`, {
      filename: newFilename,
    });
    return response.data;
  },
};

export default datasetService;
