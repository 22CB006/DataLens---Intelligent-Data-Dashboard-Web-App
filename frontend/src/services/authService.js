/**
 * Authentication Service
 * 
 * Handles all authentication-related API calls
 */

import api from './api';

const authService = {
  /**
   * Register a new user
   */
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  /**
   * Login user and store token
   */
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    const { access_token, user, message } = response.data;
    
    // Store token and user info
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { user, message };
  },

  /**
   * Logout user
   */
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  /**
   * Get current user from localStorage
   */
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },

  /**
   * Get user profile from API
   */
  getProfile: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

export default authService;
