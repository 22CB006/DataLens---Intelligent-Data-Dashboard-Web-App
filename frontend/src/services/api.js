/**
 * API Service
 * 
 * Axios instance with interceptors for authentication and error handling
 */

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
    console.log('🌐 API Request:', config.method.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.config.method.toUpperCase(), response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('❌ API Error:', error.config?.method?.toUpperCase(), error.config?.url, error.response?.status);
    // Extract user-friendly message
    let userMessage = 'Something went wrong. Please try again.';
    
    if (error.response) {
      // Server responded with error
      const { data, headers, status } = error.response;
      
      // Check for user message in headers
      if (headers['x-user-message']) {
        userMessage = headers['x-user-message'];
      }
      // Check for user message in response body
      else if (data.user_message) {
        userMessage = data.user_message;
      }
      // Check for message field
      else if (data.message) {
        userMessage = data.message;
      }
      // Check for detail message
      else if (data.detail) {
        userMessage = data.detail;
      }
      
      // Handle specific status codes
      if (status === 401) {
        userMessage = 'Your session has expired. Please log in again.';
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
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
