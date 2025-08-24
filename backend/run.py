#!/usr/bin/env python3
"""
RAG Chatbot Backend Server
Run this script to start the FastAPI server
"""

import uvicorn
from app.core.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print("Starting RAG Chatbot Backend...")
    print(f"Server will run on http://{settings.api_host}:{settings.api_port}")
    print(f"API Documentation: http://{settings.api_host}:{settings.api_port}/docs")
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info"
    )
