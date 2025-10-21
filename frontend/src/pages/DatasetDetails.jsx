/**
 * Dataset Details Page
 * 
 * Preview and details of a specific dataset
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/Layout/DashboardLayout';
import { useToast } from '../hooks/useToast';
import { ToastContainer } from '../components/Toast';
import ConfirmModal from '../components/ConfirmModal';
import datasetService from '../services/datasetService';
import { 
  ArrowLeft, 
  BarChart3, 
  Download, 
  Trash2,
  Database,
  Calendar,
  FileText
} from 'lucide-react';

const DatasetDetails = () => {
  const { datasetId } = useParams();
  const navigate = useNavigate();
  const { toasts, removeToast, showSuccess, showError } = useToast();
  
  const [dataset, setDataset] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  useEffect(() => {
    loadDataset();
  }, [datasetId]);

  const loadDataset = async () => {
    try {
      setLoading(true);
      const [datasetData, previewData] = await Promise.all([
        datasetService.getDataset(datasetId),
        datasetService.getDatasetPreview(datasetId, 20),
      ]);
      setDataset(datasetData);
      setPreview(previewData);
    } catch (error) {
      showError(error.userMessage || 'Failed to load dataset');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = () => {
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = async () => {
    try {
      await datasetService.deleteDataset(datasetId);
      showSuccess('Dataset deleted successfully');
      navigate('/upload');
    } catch (error) {
      showError(error.userMessage || 'Failed to delete dataset');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mb-4"></div>
            <p className="text-gray-600">Loading dataset...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (!dataset) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <p className="text-gray-600">Dataset not found</p>
          <button onClick={() => navigate('/upload')} className="btn-primary mt-4">
            Go to Upload
          </button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      
      <ConfirmModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={handleDeleteConfirm}
        title="Delete Dataset"
        message={`Are you sure you want to delete "${dataset?.filename}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
      />
      
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/upload')}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div>
              <h1 className="text-3xl font-bold text-navy-900">{dataset.original_filename || dataset.filename}</h1>
              <p className="text-gray-600 mt-1">
                Uploaded {formatDate(dataset.created_at)}
              </p>
            </div>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={() => navigate(`/datasets/${datasetId}/analysis`)}
              className="btn-primary flex items-center gap-2"
            >
              <BarChart3 className="w-4 h-4" />
              Analyze
            </button>
            <button
              onClick={handleDeleteClick}
              className="btn-secondary text-red-600 hover:bg-red-50 flex items-center gap-2"
            >
              <Trash2 className="w-4 h-4" />
              Delete
            </button>
          </div>
        </div>

        {/* Dataset Info */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="card">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-blue-100 rounded-lg">
                <Database className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Rows</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dataset.row_count?.toLocaleString() || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-green-100 rounded-lg">
                <FileText className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Columns</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dataset.column_count?.toLocaleString() || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-purple-100 rounded-lg">
                <Download className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">File Size</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dataset.file_size 
                    ? `${(dataset.file_size / 1024 / 1024).toFixed(2)} MB`
                    : 'N/A'
                  }
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-orange-100 rounded-lg">
                <Calendar className="w-6 h-6 text-orange-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Status</p>
                <p className="text-2xl font-bold text-green-600">
                  Active
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Data Preview */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Data Preview
          </h2>
          {preview && preview.data && preview.data.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    {preview.columns.map((col) => (
                      <th
                        key={col}
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {preview.data.map((row, idx) => (
                    <tr key={idx}>
                      {preview.columns.map((col) => (
                        <td
                          key={col}
                          className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                        >
                          {row[col] !== null && row[col] !== undefined
                            ? String(row[col])
                            : 'N/A'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">
              No preview data available
            </p>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default DatasetDetails;
