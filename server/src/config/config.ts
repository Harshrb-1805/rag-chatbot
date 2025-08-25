import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

export const config = {
  // Server Configuration
  port: parseInt(process.env.PORT || '8000', 10),
  host: process.env.HOST || '0.0.0.0',
  nodeEnv: process.env.NODE_ENV || 'development',

  // MongoDB Configuration
  mongoUri: process.env.MONGODB_URI || 'mongodb://localhost:27017',
  dbName: process.env.MONGODB_DB_NAME || 'rag_chatbot',

  // Groq API Configuration
  groqApiKey: process.env.GROQ_API_KEY || '',
  groqModel: process.env.GROQ_MODEL || 'llama3-8b-8192',

  // Security Configuration
  secretKey: process.env.SECRET_KEY || 'your_secret_key_here',
  accessTokenExpireMinutes: parseInt(process.env.ACCESS_TOKEN_EXPIRE_MINUTES || '30', 10),

  // CORS Configuration
  allowedOrigins: process.env.ALLOWED_ORIGINS?.split(',') || [
    'http://localhost:3000',
    'http://localhost:3001'
  ],

  // Frontend Configuration
  frontendUrl: process.env.REACT_APP_API_URL || 'http://localhost:3000',

  // Embedding Configuration
  embeddingModel: process.env.EMBEDDING_MODEL || 'universal-sentence-encoder',
  chunkSize: parseInt(process.env.CHUNK_SIZE || '1000', 10),
  chunkOverlap: parseInt(process.env.CHUNK_OVERLAP || '200', 10),

  // Development
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',
};