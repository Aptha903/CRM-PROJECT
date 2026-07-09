import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

api.getInteractions = (params = {}) => api.get('/interactions/', { params });
api.getInteraction = (id) => api.get(`/interactions/${id}/`);
api.createInteraction = (data) => api.post('/interactions/', data);
api.updateInteraction = (id, data) => api.put(`/interactions/${id}/`, data);
api.deleteInteraction = (id) => api.delete(`/interactions/${id}/`);
api.sendChatMessage = (messages, mode = 'log') => api.post('/interactions/chat', { messages, mode });
api.checkCompliance = (id) => api.post(`/interactions/compliance/${id}/`);

export default api;