/**
 * Upload Data Page
 * 
 * Page for uploading and managing datasets
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/Layout/DashboardLayout';
import FileUpload from '../components/FileUpload';
import FileList from '../components/FileList';
import { useToast } from '../hooks/useToast';
import { ToastContainer } from '../components/Toast';
import datasetService from '../services/datasetService';
import { RefreshCw } from 'lucide-react';

const UploadData = () => {
  const navigate = useNavigate();
  const { toasts, removeToast, showSuccess, showError } = useToast();
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchDatasets = async () => {
    try {
      setRefreshing(true);
      const data = await datasetService.getDatasets();
      
      // Handle different response formats
      if (Array.isArray(data)) {
        setDatasets(data);
      } else if (data && Array.isArray(data.datasets)) {
        setDatasets(data.datasets);
      } else if (data && Array.isArray(data.data)) {
        setDatasets(data.data);
      } else {
        console.error('Unexpected datasets format:', data);
        setDatasets([]);
      }
    } catch (error) {
      console.error('Failed to load datasets:', error);
      showError(error.userMessage || 'Failed to load datasets');
      setDatasets([]);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, []);

  const handleUploadSuccess = (result) => {
    showSuccess(result.message || 'Dataset uploaded successfully!');
    fetchDatasets(); // Refresh the list
  };

  const handleUploadError = (error) => {
    showError(error.userMessage || 'Upload failed. Please try again.');
  };

  const handleDelete = async (datasetId) => {
    try {
      await datasetService.deleteDataset(datasetId);
      showSuccess('Dataset deleted successfully');
      fetchDatasets();
    } catch (error) {
      showError(error.userMessage || 'Failed to delete dataset');
      throw error;
    }
  };

  const handleRename = async (datasetId, newFilename) => {
    try {
      await datasetService.renameDataset(datasetId, newFilename);
      showSuccess('Dataset renamed successfully');
      fetchDatasets();
    } catch (error) {
      showError(error.userMessage || 'Failed to rename dataset');
      throw error;
    }
  };

  return (
    <DashboardLayout>
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-navy-900">Upload Data</h1>
            <p className="text-gray-600 mt-2">
              Upload your datasets to start analyzing with AI-powered insights
            </p>
          </div>
          
          <button
            onClick={fetchDatasets}
            disabled={refreshing}
            className="btn-secondary flex items-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {/* Upload Section */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Upload New Dataset
          </h2>
          <FileUpload
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
          />
        </div>

        {/* Datasets List */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">
              My Datasets
              {datasets.length > 0 && (
                <span className="ml-2 text-sm font-normal text-gray-500">
                  ({datasets.length})
                </span>
              )}
            </h2>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
              <p className="text-gray-600 mt-4">Loading datasets...</p>
            </div>
          ) : (
            <FileList
              datasets={datasets}
              onDelete={handleDelete}
              onRename={handleRename}
              onRefresh={fetchDatasets}
            />
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default UploadData;
