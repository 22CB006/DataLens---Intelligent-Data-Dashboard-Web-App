# Error Handling & Validation Guide

## ✅ **What Was Implemented**

### **1. Global Exception Handlers**
- ✅ User-friendly error messages for all errors
- ✅ Validation error formatting
- ✅ Database error handling
- ✅ Custom exception classes

### **2. Files Created**
```
backend/app/core/
├── exceptions.py        # Custom exception classes
└── error_handlers.py    # Global error handlers
```

### **3. Error Response Format**

All errors now return:
```json
{
  "detail": "Technical error message",
  "user_message": "User-friendly message for display",
  "errors": [...]  // For validation errors
}
```

---

## 🔧 **Fixes Applied**

### **Fix 1: Delete Dataset**
**Problem:** 404 error when deleting dataset

**Solution:**
- Fixed database delete operation
- Added proper error handling
- Added user-friendly messages

**Test:**
```
DELETE /api/v1/datasets/{dataset_id}
Authorization: Bearer YOUR_TOKEN
```

**Expected:** 204 No Content (success)

---

### **Fix 2: User-Friendly Error Messages**

All endpoints now return helpful messages:

#### **Authentication Errors**
```json
{
  "detail": "Incorrect email or password",
  "user_message": "The email or password you entered is incorrect. Please try again."
}
```

#### **File Upload Errors**
```json
{
  "detail": "Invalid file type",
  "user_message": "Please upload a valid file. Supported formats: csv, xlsx, json"
}
```

#### **Validation Errors**
```json
{
  "detail": "Validation error",
  "user_message": "Invalid email: value is not a valid email address",
  "errors": [
    {
      "field": "email",
      "message": "value is not a valid email address"
    }
  ]
}
```

#### **Permission Errors**
```json
{
  "detail": "Not authorized",
  "user_message": "You don't have permission to access this dataset."
}
```

---

## 📝 **All Custom Exceptions**

### **Authentication**
- `InvalidCredentialsError` - Wrong email/password
- `TokenExpiredError` - Session expired
- `InvalidTokenError` - Invalid token
- `UserNotFoundError` - User doesn't exist
- `UserAlreadyExistsError` - Duplicate email/username
- `InactiveUserError` - Account deactivated

### **Dataset**
- `DatasetNotFoundError` - Dataset doesn't exist
- `DatasetAccessDeniedError` - No permission
- `InvalidFileTypeError` - Wrong file format
- `FileTooLargeError` - File exceeds size limit
- `FileProcessingError` - Can't process file
- `EmptyDatasetError` - File is empty

### **Analysis**
- `InsufficientDataError` - Not enough data
- `InvalidColumnError` - Column doesn't exist
- `NoNumericColumnsError` - No numeric data

### **General**
- `ValidationError` - Input validation failed
- `DatabaseError` - Database operation failed
- `ServerError` - Internal server error

---

## 🎨 **Frontend Integration**

### **Step 1: Create Toast Notification Component**

Create `frontend/src/components/Toast.jsx`:

```jsx
import { useState, useEffect } from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';

export const Toast = ({ message, type = 'info', onClose, duration = 5000 }) => {
  useEffect(() => {
    if (duration) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const icons = {
    success: <CheckCircle className="w-5 h-5 text-green-500" />,
    error: <AlertCircle className="w-5 h-5 text-red-500" />,
    warning: <AlertTriangle className="w-5 h-5 text-yellow-500" />,
    info: <Info className="w-5 h-5 text-blue-500" />
  };

  const bgColors = {
    success: 'bg-green-50 border-green-200',
    error: 'bg-red-50 border-red-200',
    warning: 'bg-yellow-50 border-yellow-200',
    info: 'bg-blue-50 border-blue-200'
  };

  return (
    <div className={`fixed top-4 right-4 z-50 max-w-md p-4 border rounded-lg shadow-lg ${bgColors[type]} animate-slide-in`}>
      <div className="flex items-start gap-3">
        {icons[type]}
        <p className="flex-1 text-sm text-gray-800">{message}</p>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export const ToastContainer = ({ toasts, removeToast }) => {
  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          message={toast.message}
          type={toast.type}
          onClose={() => removeToast(toast.id)}
        />
      ))}
    </div>
  );
};
```

---

### **Step 2: Create Toast Hook**

Create `frontend/src/hooks/useToast.js`:

```javascript
import { useState, useCallback } from 'react';

export const useToast = () => {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = 'info') => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, message, type }]);
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const showSuccess = useCallback((message) => addToast(message, 'success'), [addToast]);
  const showError = useCallback((message) => addToast(message, 'error'), [addToast]);
  const showWarning = useCallback((message) => addToast(message, 'warning'), [addToast]);
  const showInfo = useCallback((message) => addToast(message, 'info'), [addToast]);

  return {
    toasts,
    removeToast,
    showSuccess,
    showError,
    showWarning,
    showInfo
  };
};
```

---

### **Step 3: Create API Service with Error Handling**

Create `frontend/src/services/api.js`:

```javascript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Extract user-friendly message
    let userMessage = 'Something went wrong. Please try again.';
    
    if (error.response) {
      // Server responded with error
      const { data, headers } = error.response;
      
      // Check for user message in headers
      if (headers['x-user-message']) {
        userMessage = headers['x-user-message'];
      }
      // Check for user message in response body
      else if (data.user_message) {
        userMessage = data.user_message;
      }
      // Check for detail message
      else if (data.detail) {
        userMessage = data.detail;
      }
      
      // Handle specific status codes
      if (error.response.status === 401) {
        userMessage = 'Your session has expired. Please log in again.';
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      }
    } else if (error.request) {
      // Request made but no response
      userMessage = 'Cannot connect to server. Please check your internet connection.';
    }
    
    // Attach user message to error
    error.userMessage = userMessage;
    return Promise.reject(error);
  }
);

export default api;
```

---

### **Step 4: Use in Components**

Example usage in a component:

```jsx
import { useState } from 'react';
import api from '../services/api';
import { useToast } from '../hooks/useToast';
import { ToastContainer } from '../components/Toast';

function DatasetList() {
  const [datasets, setDatasets] = useState([]);
  const { toasts, removeToast, showSuccess, showError } = useToast();

  const deleteDataset = async (id) => {
    try {
      await api.delete(`/datasets/${id}`);
      showSuccess('Dataset deleted successfully!');
      // Refresh list
      fetchDatasets();
    } catch (error) {
      showError(error.userMessage);
    }
  };

  const fetchDatasets = async () => {
    try {
      const response = await api.get('/datasets/');
      setDatasets(response.data.datasets);
    } catch (error) {
      showError(error.userMessage);
    }
  };

  return (
    <div>
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      {/* Your component UI */}
    </div>
  );
}
```

---

## 🧪 **Testing Error Messages**

### **Test 1: Invalid Login**
```bash
POST /api/v1/auth/login
{
  "email": "wrong@example.com",
  "password": "wrongpass"
}
```

**Expected:**
```json
{
  "detail": "Incorrect email or password",
  "user_message": "The email or password you entered is incorrect. Please try again."
}
```

### **Test 2: Duplicate Email**
```bash
POST /api/v1/auth/register
{
  "email": "existing@example.com",  // Already exists
  "username": "newuser",
  "password": "password123"
}
```

**Expected:**
```json
{
  "detail": "Database integrity error",
  "user_message": "An account with this email already exists."
}
```

### **Test 3: Delete Non-existent Dataset**
```bash
DELETE /api/v1/datasets/invalid-id
```

**Expected:**
```json
{
  "detail": "Dataset not found",
  "user_message": "The dataset you're trying to delete could not be found. It may have already been deleted."
}
```

### **Test 4: Validation Error**
```bash
POST /api/v1/auth/register
{
  "email": "not-an-email",  // Invalid format
  "username": "test",
  "password": "pass"
}
```

**Expected:**
```json
{
  "detail": "Validation error",
  "user_message": "Invalid email: value is not a valid email address",
  "errors": [
    {
      "field": "email",
      "message": "value is not a valid email address"
    }
  ]
}
```

---

## 📋 **Commands to Apply Fixes**

```bash
# 1. Restart backend server
cd backend
uvicorn app.main:app --reload

# 2. Test delete endpoint
# Use Postman to delete a dataset

# 3. Check error messages
# Try various error scenarios
```

---

## ✅ **Benefits**

1. **User-Friendly** - Clear, actionable error messages
2. **Consistent** - Same format across all endpoints
3. **Informative** - Tells users what went wrong and how to fix it
4. **Professional** - Production-ready error handling
5. **Frontend-Ready** - Easy to display in toast notifications

---

## 🎉 **Summary**

- ✅ Fixed delete dataset endpoint
- ✅ Added global error handlers
- ✅ Created custom exception classes
- ✅ User-friendly error messages for all errors
- ✅ Frontend toast notification system
- ✅ API service with error handling
- ✅ Consistent error format

**All APIs now have proper validation and user-friendly error messages!** 🚀
