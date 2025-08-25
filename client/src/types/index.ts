// Common TypeScript interfaces for the RAG Chatbot application

export interface Document {
  id: string;
  title: string;
  content: string;
  source: string;
  created_at: string;
  updated_at: string;
  chunk_count: number;
}

export interface DocumentList {
  documents: Document[];
  total: number;
}

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  created_at: string;
  tokens_used?: number;
}

export interface ChatRequest {
  message: string;
  chat_id?: string;
}

export interface ChatResponse {
  message: string;
  chat_id: string;
  sources: string[];
  tokens_used: number;
}

export interface ChatSession {
  id: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  total_tokens: number;
}

export interface Stats {
  total_documents: number;
  total_chunks: number;
  average_chunks_per_document: number;
}

export interface HealthStatus {
  status: string;
  database: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}
