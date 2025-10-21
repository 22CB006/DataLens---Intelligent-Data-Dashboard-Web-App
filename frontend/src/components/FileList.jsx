/**
 * FileList Component
 * 
 * Display list of uploaded datasets with actions
 */

import { useState } from 'react';
import { File, Trash2, Eye, BarChart3, Calendar, Database, Edit2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import ConfirmModal from './ConfirmModal';

const FileList = ({ datasets, onDelete, onRefresh, onRename }) => {
  const navigate = useNavigate();
  const [deletingId, setDeletingId] = useState(null);
  const [renamingId, setRenamingId] = useState(null);
  const [newName, setNewName] = useState('');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [datasetToDelete, setDatasetToDelete] = useState(null);

  const handleDeleteClick = (dataset) => {
    setDatasetToDelete(dataset);
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = async () => {
    if (!datasetToDelete) return;

    setDeletingId(datasetToDelete.id);
    try {
      await onDelete(datasetToDelete.id);
      if (onRefresh) {
        onRefresh();
      }
    } catch (error) {
      console.error('Delete failed:', error);
    } finally {
      setDeletingId(null);
      setDatasetToDelete(null);
    }
  };

  const handleRenameClick = (dataset) => {
    setRenamingId(dataset.id);
    // Remove file extension for editing
    const nameWithoutExt = dataset.filename.replace(/\.[^/.]+$/, '');
    setNewName(nameWithoutExt);
  };

  const handleRenameSubmit = async (datasetId, originalFilename) => {
    if (!newName.trim()) {
      alert('Please enter a valid name');
      return;
    }

    try {
      // Get file extension from original filename
      const extension = originalFilename.match(/\.[^/.]+$/)?.[0] || '';
      const fullNewName = newName.trim() + extension;
      
      if (onRename) {
        await onRename(datasetId, fullNewName);
      }
      setRenamingId(null);
      setNewName('');
      if (onRefresh) {
        onRefresh();
      }
    } catch (error) {
      console.error('Rename failed:', error);
    }
  };

  const handleRenameCancel = () => {
    setRenamingId(null);
    setNewName('');
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return 'N/A';
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  // Ensure datasets is an array
  const datasetList = Array.isArray(datasets) ? datasets : [];

  if (datasetList.length === 0) {
    return (
      <div className="text-center py-12">
        <Database className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No datasets yet</h3>
        <p className="text-gray-600">Upload your first dataset to get started</p>
      </div>
    );
  }

  return (
    <>
      <ConfirmModal
        isOpen={showDeleteModal}
        onClose={() => {
          setShowDeleteModal(false);
          setDatasetToDelete(null);
        }}
        onConfirm={handleDeleteConfirm}
        title="Delete Dataset"
        message={`Are you sure you want to delete "${datasetToDelete?.filename}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
      />

      <div className="space-y-4">
      {datasetList.map((dataset) => (
        <div
          key={dataset.id}
          className="card hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between">
            {/* Dataset Info */}
            <div className="flex items-start gap-4 flex-1">
              <div className="p-3 bg-primary-100 rounded-lg">
                <File className="w-6 h-6 text-primary-600" />
              </div>
              
              <div className="flex-1 min-w-0">
                {renamingId === dataset.id ? (
                  <div className="flex items-center gap-2 mb-1">
                    <input
                      type="text"
                      value={newName}
                      onChange={(e) => setNewName(e.target.value)}
                      className="flex-1 px-3 py-1 border border-primary-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      autoFocus
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          handleRenameSubmit(dataset.id, dataset.filename);
                        } else if (e.key === 'Escape') {
                          handleRenameCancel();
                        }
                      }}
                    />
                    <button
                      onClick={() => handleRenameSubmit(dataset.id, dataset.filename)}
                      className="px-3 py-1 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm"
                    >
                      Save
                    </button>
                    <button
                      onClick={handleRenameCancel}
                      className="px-3 py-1 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 text-sm"
                    >
                      Cancel
                    </button>
                  </div>
                ) : (
                  <h3 className="text-lg font-semibold text-gray-900 mb-1 truncate">
                    {dataset.original_filename || dataset.filename}
                  </h3>
                )}
                
                <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                  <div className="flex items-center gap-1">
                    <Database className="w-4 h-4" />
                    <span>{dataset.row_count?.toLocaleString() || 0} rows</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <BarChart3 className="w-4 h-4" />
                    <span>{dataset.column_count?.toLocaleString() || 0} columns</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    <span>{formatDate(dataset.created_at)}</span>
                  </div>
                </div>

                {dataset.file_size && (
                  <p className="text-sm text-gray-500 mt-1">
                    Size: {formatFileSize(dataset.file_size)}
                  </p>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-2 ml-4">
              <button
                onClick={() => navigate(`/datasets/${dataset.id}/preview`)}
                className="p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                title="Preview"
              >
                <Eye className="w-5 h-5" />
              </button>
              
              <button
                onClick={() => navigate(`/datasets/${dataset.id}/analysis`)}
                className="p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                title="Analyze"
              >
                <BarChart3 className="w-5 h-5" />
              </button>
              
              <button
                onClick={() => handleRenameClick(dataset)}
                className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                title="Rename"
              >
                <Edit2 className="w-5 h-5" />
              </button>
              
              <button
                onClick={() => handleDeleteClick(dataset)}
                disabled={deletingId === dataset.id}
                className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                title="Delete"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      ))}
      </div>
    </>
  );
};

export default FileList;
