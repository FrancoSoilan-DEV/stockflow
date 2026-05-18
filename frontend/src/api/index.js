import api from './axios'

// ── Auth ──────────────────────────────────────────
export const authApi = {
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
}

// ── Branches ──────────────────────────────────────
export const branchesApi = {
  list: () => api.get('/branches/'),
  get: (id) => api.get(`/branches/${id}`),
  create: (data) => api.post('/branches/', data),
  update: (id, data) => api.patch(`/branches/${id}`, data),
  delete: (id) => api.delete(`/branches/${id}`),
}

// ── Users ─────────────────────────────────────────
export const usersApi = {
  list: () => api.get('/users/'),
  get: (id) => api.get(`/users/${id}`),
  create: (data) => api.post('/users/', data),
  update: (id, data) => api.patch(`/users/${id}`, data),
  delete: (id) => api.delete(`/users/${id}`),
}

// ── Products ──────────────────────────────────────
export const productsApi = {
  list: () => api.get('/products/'),
  get: (id) => api.get(`/products/${id}`),
  create: (data) => api.post('/products/', data),
  update: (id, data) => api.patch(`/products/${id}`, data),
  delete: (id) => api.delete(`/products/${id}`),
}

// ── Stock ─────────────────────────────────────────
export const stockApi = {
  byBranch: (branchId) => api.get(`/stock/branch/${branchId}`),
  byProduct: (productId) => api.get(`/stock/product/${productId}`),
  update: (branchId, productId, data) =>
    api.patch(`/stock/branch/${branchId}/product/${productId}`, data),
}

// ── Sales ─────────────────────────────────────────
export const salesApi = {
  byBranch: (branchId) => api.get(`/sales/branch/${branchId}`),
  get: (id) => api.get(`/sales/${id}`),
  create: (branchId, data) => api.post(`/sales/branch/${branchId}`, data),
}

// ── Stock Requests ────────────────────────────────
export const stockRequestsApi = {
  list: () => api.get('/stock-requests/'),
  byBranch: (branchId) => api.get(`/stock-requests/branch/${branchId}`),
  get: (id) => api.get(`/stock-requests/${id}`),
  create: (data) => api.post('/stock-requests/', data),
  updateStatus: (id, data) => api.patch(`/stock-requests/${id}/status`, data),
}