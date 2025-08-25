import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Document API endpoints
export const documentAPI = {
  // Upload document file
  uploadFile: async (file: File, title?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    if (title) {
      formData.append('title', title);
    }
    
    const response = await api.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Paste text content
  pasteText: async (title: string, content: string) => {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('content', content);
    
    const response = await api.post('/api/documents/paste', formData);
    return response.data;
  },

  // Get all documents
  getAllDocuments: async () => {
    const response = await api.get('/api/documents/');
    return response.data;
  },

  // Get document by ID
  getDocument: async (id: string) => {
    const response = await api.get(`/api/documents/${id}`);
    return response.data;
  },

  // Delete document
  deleteDocument: async (id: string) => {
    const response = await api.delete(`/api/documents/${id}`);
    return response.data;
  },

  // Get document statistics
  getStats: async () => {
    const response = await api.get('/api/documents/stats/summary');
    return response.data;
  },
};

// Chat API endpoints
export const chatAPI = {
  // Send chat message
  sendMessage: async (message: string, chatId?: string) => {
    const response = await api.post('/api/chat/', {
      message,
      chat_id: chatId,
    });
    return response.data;
  },

  // Get chat sessions
  getChatSessions: async () => {
    const response = await api.get('/api/chat/sessions');
    return response.data;
  },

  // Get chat history
  getChatHistory: async (chatId: string, limit: number = 20) => {
    const response = await api.get(`/api/chat/sessions/${chatId}/history?limit=${limit}`);
    return response.data;
  },

  // Delete chat session
  deleteChatSession: async (chatId: string) => {
    const response = await api.delete(`/api/chat/sessions/${chatId}`);
    return response.data;
  },

  // Clear chat history
  clearChatHistory: async (chatId: string) => {
    const response = await api.post(`/api/chat/sessions/${chatId}/clear`);
    return response.data;
  },
};

// Health check
export const healthAPI = {
  checkHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
