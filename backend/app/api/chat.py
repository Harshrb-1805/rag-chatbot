from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..models.chat import ChatRequest, ChatResponse
from ..services.chat_service import get_chat_service
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_documents(chat_request: ChatRequest):
    """
    Chat with uploaded documents using RAG.
    
    Args:
        chat_request: Chat request with user message
        
    Returns:
        Chat response with assistant message and sources
    """
    try:
        response = await get_chat_service().process_chat_request(chat_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions")
async def get_chat_sessions():
    """
    Get all chat sessions.
    
    Returns:
        List of chat sessions with metadata
    """
    try:
        sessions = await get_chat_service().get_chat_sessions()
        return {"sessions": sessions, "total": len(sessions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{chat_id}/history")
async def get_chat_history(chat_id: str, limit: int = 20):
    """
    Get chat history for a specific session.
    
    Args:
        chat_id: Chat session ID
        limit: Maximum number of messages to return
        
    Returns:
        List of messages in the chat session
    """
    try:
        history = await get_chat_service().get_chat_history(chat_id, limit)
        return {"chat_id": chat_id, "messages": history, "total": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{chat_id}")
async def delete_chat_session(chat_id: str):
    """
    Delete a chat session and all its messages.
    
    Args:
        chat_id: Chat session ID
        
    Returns:
        Success message
    """
    try:
        success = await get_chat_service().delete_chat_session(chat_id)
        if not success:
            raise HTTPException(
                status_code=404, 
                detail="Chat session not found"
            )
        return {"message": "Chat session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions/{chat_id}/clear")
async def clear_chat_history(chat_id: str):
    """
    Clear chat history for a session (keep the session).
    
    Args:
        chat_id: Chat session ID
        
    Returns:
        Success message
    """
    try:
        # Delete all messages in the chat
        from ..core.database import db
        messages_collection = db.get_collection("messages")
        
        result = await messages_collection.delete_many({"chat_id": chat_id})
        
        # Reset chat session counters
        chats_collection = db.get_collection("chats")
        await chats_collection.update_one(
            {"_id": chat_id},
            {
                "$set": {
                    "message_count": 0,
                    "total_tokens": 0,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {"message": f"Chat history cleared. {result.deleted_count} messages removed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
