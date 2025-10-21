/**
 * FileUpload Component
 * 
 * Drag-and-drop file upload with progress tracking
 */

import { useState, useRef } from 'react';
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react';

const FileUpload = ({ onUploadSuccess, onUploadError }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState('idle'); // idle, uploading, success, error
  const [errorMessage, setErrorMessage] = useState('');
  const fileInputRef = useRef(null);

  const allowedTypes = [
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  ];

  const allowedExtensions = ['.csv', '.xls', '.xlsx'];

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleFileSelection(files[0]);
    }
  };

  const handleFileInputChange = (e) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelection(files[0]);
    }
  };

  const handleFileSelection = (file) => {
    // Validate file type
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
      setErrorMessage('Please upload a CSV or Excel file (.csv, .xls, .xlsx)');
      setUploadStatus('error');
      return;
    }

    // Validate file size (max 50MB)
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (file.size > maxSize) {
      setErrorMessage('File size must be less than 50MB');
      setUploadStatus('error');
      return;
    }

    setSelectedFile(file);
    setUploadStatus('idle');
    setErrorMessage('');
    setUploadProgress(0);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploadStatus('uploading');
    setUploadProgress(0);

    try {
      // Import datasetService dynamically to avoid circular dependencies
      const { default: datasetService } = await import('../services/datasetService');
      
      const result = await datasetService.uploadDataset(
        selectedFile,
        (progress) => setUploadProgress(progress)
      );

      setUploadStatus('success');
      setUploadProgress(100);
      
      if (onUploadSuccess) {
        onUploadSuccess(result);
      }

      // Reset after 2 seconds
      setTimeout(() => {
        resetUpload();
      }, 2000);
    } catch (error) {
      setUploadStatus('error');
      setErrorMessage(error.userMessage || 'Upload failed. Please try again.');
      
      if (onUploadError) {
        onUploadError(error);
      }
    }
  };

  const resetUpload = () => {
    setSelectedFile(null);
    setUploadProgress(0);
    setUploadStatus('idle');
    setErrorMessage('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="w-full">
      {/* Drop Zone */}
      <div
        className={`
          relative border-2 border-dashed rounded-lg p-8 text-center transition-all
          ${isDragging ? 'border-primary-500 bg-primary-50' : 'border-gray-300 bg-white'}
          ${uploadStatus === 'success' ? 'border-green-500 bg-green-50' : ''}
          ${uploadStatus === 'error' ? 'border-red-500 bg-red-50' : ''}
        `}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xls,.xlsx"
          onChange={handleFileInputChange}
          className="hidden"
        />

        {uploadStatus === 'idle' && !selectedFile && (
          <div className="space-y-4">
            <div className="flex justify-center">
              <Upload className="w-12 h-12 text-gray-400" />
            </div>
            <div>
              <p className="text-lg font-medium text-gray-700">
                Drop your file here, or{' '}
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="text-primary-500 hover:text-primary-600 font-semibold"
                >
                  browse
                </button>
              </p>
              <p className="text-sm text-gray-500 mt-2">
                Supports: CSV, Excel (.csv, .xls, .xlsx) • Max size: 50MB
              </p>
            </div>
          </div>
        )}

        {selectedFile && uploadStatus === 'idle' && (
          <div className="space-y-4">
            <div className="flex items-center justify-center gap-3">
              <File className="w-8 h-8 text-primary-500" />
              <div className="text-left">
                <p className="font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-sm text-gray-500">{formatFileSize(selectedFile.size)}</p>
              </div>
              <button
                onClick={resetUpload}
                className="ml-4 p-1 hover:bg-gray-100 rounded"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>
            <button
              onClick={handleUpload}
              className="btn-primary"
            >
              Upload Dataset
            </button>
          </div>
        )}

        {uploadStatus === 'uploading' && (
          <div className="space-y-4">
            <div className="flex items-center justify-center gap-3">
              <File className="w-8 h-8 text-primary-500" />
              <div className="text-left">
                <p className="font-medium text-gray-900">{selectedFile?.name}</p>
                <p className="text-sm text-gray-500">Uploading... {uploadProgress}%</p>
              </div>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}

        {uploadStatus === 'success' && (
          <div className="space-y-4">
            <div className="flex justify-center">
              <CheckCircle className="w-12 h-12 text-green-500" />
            </div>
            <div>
              <p className="text-lg font-medium text-green-700">
                Upload Successful!
              </p>
              <p className="text-sm text-gray-600 mt-1">
                Your dataset has been uploaded and is ready for analysis.
              </p>
            </div>
          </div>
        )}

        {uploadStatus === 'error' && (
          <div className="space-y-4">
            <div className="flex justify-center">
              <AlertCircle className="w-12 h-12 text-red-500" />
            </div>
            <div>
              <p className="text-lg font-medium text-red-700">Upload Failed</p>
              <p className="text-sm text-red-600 mt-1">{errorMessage}</p>
            </div>
            <button
              onClick={resetUpload}
              className="btn-secondary"
            >
              Try Again
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
