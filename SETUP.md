# RAG Chatbot Setup Guide

This guide will walk you through setting up the RAG Chatbot project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **MongoDB** - [Download MongoDB](https://www.mongodb.com/try/download/community)
- **Git** - [Download Git](https://git-scm.com/)

## Project Structure

```
rag-chatbot/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration & database
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt    # Python dependencies
│   └── run.py             # Server startup script
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS config
├── .env.example           # Environment variables template
└── README.md              # Project documentation
```

## Step 1: Clone and Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rag-chatbot
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file with your configuration:**
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

   # Security
   SECRET_KEY=your_secret_key_here
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # CORS Configuration
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
   ```

## Step 2: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start MongoDB:**
   ```bash
   # Start MongoDB service (Windows)
   net start MongoDB

   # Start MongoDB service (macOS/Linux)
   sudo systemctl start mongod
   # or
   brew services start mongodb-community
   ```

5. **Run the backend server:**
   ```bash
   python run.py
   ```

   The server will start at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

## Step 3: Frontend Setup

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will open at `http://localhost:3000`

## Step 4: Get Groq API Key

1. **Sign up for Groq:**
   - Visit [Groq Console](https://console.groq.com/)
   - Create an account and verify your email

2. **Generate API Key:**
   - Go to API Keys section
   - Create a new API key
   - Copy the key and update your `.env` file

3. **Choose a model:**
   - Recommended: `llama3-8b-8192` (fast and cost-effective)
   - Alternative: `mixtral-8x7b-32768` (more powerful)

## Step 5: Test the Application

1. **Upload Documents:**
   - Go to `/upload` page
   - Upload a `.txt` file or paste text content
   - Verify documents appear in the list

2. **Start Chatting:**
   - Go to `/chat` page
   - Ask questions about your uploaded documents
   - Verify RAG responses with source citations

3. **Check Dashboard:**
   - Visit the main dashboard
   - Verify statistics and system health

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error:**
   - Ensure MongoDB is running
   - Check connection string in `.env`
   - Verify MongoDB port (default: 27017)

2. **Groq API Error:**
   - Verify API key is correct
   - Check API key permissions
   - Ensure sufficient credits in account

3. **Frontend Build Errors:**
   - Clear `node_modules` and reinstall
   - Check Node.js version compatibility
   - Verify all dependencies are installed

4. **CORS Issues:**
   - Check `ALLOWED_ORIGINS` in `.env`
   - Ensure frontend and backend ports match
   - Restart both servers after config changes

### Performance Tips

1. **Document Processing:**
   - Keep text files under 10MB for optimal performance
   - Use meaningful titles for better organization
   - Consider chunking very long documents manually

2. **Chat Optimization:**
   - Keep chat history reasonable (last 5-10 messages)
   - Use specific questions for better RAG responses
   - Monitor token usage for cost optimization

## Development

### Backend Development

- **API Testing:** Use FastAPI's automatic docs at `/docs`
- **Logs:** Check console output for debugging
- **Hot Reload:** Enabled by default in development mode

### Frontend Development

- **Hot Reload:** React dev server automatically refreshes
- **TypeScript:** Full type safety with defined interfaces
- **Styling:** Tailwind CSS with custom design system

### Database Management

- **MongoDB Compass:** GUI for database inspection
- **Collections:** `documents`, `messages`, `chats`
- **Indexes:** Automatic on `_id` fields

## Deployment

### Backend Deployment

1. **Production Environment:**
   - Set `DEBUG=False` in `.env`
   - Use production MongoDB instance
   - Configure proper CORS origins

2. **Docker Support:**
   - Build image: `docker build -t rag-chatbot .`
   - Run container: `docker run -p 8000:8000 rag-chatbot`

### Frontend Deployment

1. **Build for Production:**
   ```bash
   npm run build
   ```

2. **Deploy to:**
   - Vercel: `vercel --prod`
   - Netlify: `netlify deploy --prod`
   - Static hosting: Upload `build/` folder

## Support

- **Documentation:** Check `/docs` endpoint for API details
- **Issues:** Review console logs and network requests
- **Community:** Check project README for updates

## Next Steps

After successful setup:

1. **Customize:** Modify embedding models and chunk sizes
2. **Scale:** Add more documents and test RAG performance
3. **Enhance:** Implement user authentication and document sharing
4. **Monitor:** Add logging and analytics for production use

Happy coding! 🚀
