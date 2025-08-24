# RAG Chatbot Project

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload documents, generate embeddings, and chat with the uploaded content using Groq's LLM API.

## Features

- **Document Upload Interface**: Upload TXT files or paste text directly
- **Text Embedding**: Generate and store embeddings in MongoDB vector database
- **Chat Interface**: Interactive chat with uploaded documents using RAG
- **Modern UI**: React-based frontend with responsive design
- **FastAPI Backend**: High-performance Python backend
- **MongoDB Integration**: Document and vector storage
- **Groq LLM**: Advanced language model for responses

## Project Structure

```
rag-chatbot/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
├── .env.example            # Environment variables template
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB instance
- Groq API key

### Backend Setup
1. Navigate to the backend directory
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your configuration
6. Run the server: `uvicorn app.main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=rag_chatbot

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
```

## API Endpoints

- `POST /api/documents/upload` - Upload and embed documents
- `POST /api/documents/paste` - Embed pasted text
- `POST /api/chat` - Chat with the uploaded documents
- `GET /api/documents` - List uploaded documents

## Usage

1. **Upload Documents**: Use the upload interface to add TXT files or paste text
2. **Generate Embeddings**: The system automatically generates embeddings and stores them
3. **Start Chatting**: Use the chat interface to ask questions about your documents
4. **RAG Responses**: Get contextual answers based on your uploaded content

## Technologies Used

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **Database**: MongoDB with vector search
- **LLM**: Groq API
- **Embeddings**: Sentence Transformers
- **Vector Search**: FAISS (Facebook AI Similarity Search)

## License

MIT License - see LICENSE file for details
