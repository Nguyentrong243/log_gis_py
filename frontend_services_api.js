// React: API Service
import axios from 'axios';
import { useAuthStore } from '../stores/authStore';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token || localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (data) => apiClient.post('/auth/register', data),
  login: (data) => apiClient.post('/auth/login', data),
  verifyToken: () => apiClient.get('/auth/verify'),
  logout: () => apiClient.post('/auth/logout')
};

// Shipment APIs
export const shipmentAPI = {
  getAll: (params) => apiClient.get('/shipments', { params }),
  getById: (id) => apiClient.get(`/shipments/${id}`),
  getTracking: (id) => apiClient.get(`/shipments/${id}/tracking`),
  create: (data) => apiClient.post('/shipments', data),
  update: (id, data) => apiClient.put(`/shipments/${id}`, data),
  delete: (id) => apiClient.delete(`/shipments/${id}`),
  getByWarehouse: (warehouseId, params) =>
    apiClient.get(`/shipments/warehouse/${warehouseId}`, { params })
};

// Waypoint APIs
export const waypointAPI = {
  getById: (id) => apiClient.get(`/waypoints/${id}`),
  markArrived: (id) => apiClient.post(`/waypoints/${id}/arrive`),
  confirm: (id, data) => apiClient.post(`/waypoints/${id}/confirm`, data),
  markDeparted: (id) => apiClient.post(`/waypoints/${id}/depart`),
  getCheckpointLogs: (id) => apiClient.get(`/waypoints/${id}/logs`)
};

// Warehouse APIs
export const warehouseAPI = {
  getAll: () => apiClient.get('/warehouses'),
  getById: (id) => apiClient.get(`/warehouses/${id}`),
  getStats: (id) => apiClient.get(`/warehouses/${id}/stats`),
  getIncoming: (id) => apiClient.get(`/warehouses/${id}/incoming`),
  create: (data) => apiClient.post('/warehouses', data),
  update: (id, data) => apiClient.put(`/warehouses/${id}`, data),
  delete: (id) => apiClient.delete(`/warehouses/${id}`)
};

// Admin APIs
export const adminAPI = {
  getDashboard: () => apiClient.get('/admin/dashboard'),
  getDelayReport: (params) => apiClient.get('/admin/reports/delays', { params }),
  getPerformanceReport: (params) =>
    apiClient.get('/admin/reports/performance', { params }),
  exportReport: (type) =>
    apiClient.get(`/admin/reports/export?type=${type}`, { responseType: 'blob' }),
  getUsers: () => apiClient.get('/admin/users'),
  createUser: (data) => apiClient.post('/admin/users', data),
  updateUser: (id, data) => apiClient.put(`/admin/users/${id}`, data),
  deleteUser: (id) => apiClient.delete(`/admin/users/${id}`)
};

// Public Tracking APIs (no auth required)
export const trackingAPI = {
  getPublic: (referenceCode) =>
    axios.get(`${API_URL}/tracking/shipment/${referenceCode}`),
  getTimeline: (id) =>
    axios.get(`${API_URL}/tracking/shipment/${id}/timeline`),
  getMapData: (id) => axios.get(`${API_URL}/tracking/shipment/${id}/map-data`)
};

export default apiClient;
