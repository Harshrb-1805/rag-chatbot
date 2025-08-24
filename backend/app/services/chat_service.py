from datetime import datetime
from typing import List, Dict, Any, Optional
from bson import ObjectId
from ..core.database import db
from ..models.chat import ChatRequest, ChatResponse, MessageCreate, MessageInDB
from .document_service import document_service
from .groq_service import groq_service

class ChatService:
    """Service for managing chat sessions and generating RAG responses."""
    
    def __init__(self):
        """Initialize the chat service."""
        self.messages_collection_name = "messages"
        self.chats_collection_name = "chats"
    
    @property
    def messages_collection(self):
        """Get the messages collection lazily."""
        return db.get_collection(self.messages_collection_name)
    
    @property
    def chats_collection(self):
        """Get the chats collection lazily."""
        return db.get_collection(self.chats_collection_name)
    
    async def create_chat_session(self) -> str:
        """
        Create a new chat session.
        
        Returns:
            Chat session ID
        """
        try:
            chat_data = {
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "message_count": 0,
                "total_tokens": 0
            }
            
            result = await self.chats_collection.insert_one(chat_data)
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error creating chat session: {e}")
            raise e
    
    async def add_message(self, chat_id: str, content: str, role: str, 
                         tokens_used: Optional[int] = None) -> str:
        """
        Add a message to a chat session.
        
        Args:
            chat_id: Chat session ID
            content: Message content
            role: Message role (user or assistant)
            tokens_used: Number of tokens used
            
        Returns:
            Message ID
        """
        try:
            message = MessageInDB(
                chat_id=ObjectId(chat_id),
                content=content,
                role=role,
                tokens_used=tokens_used
            )
            
            # Insert message
            doc_dict = message.dict(by_alias=True)
            result = await self.messages_collection.insert_one(doc_dict)
            
            # Update chat session
            await self.chats_collection.update_one(
                {"_id": ObjectId(chat_id)},
                {
                    "$inc": {"message_count": 1, "total_tokens": tokens_used or 0},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error adding message: {e}")
            raise e
    
    async def get_chat_history(self, chat_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get chat history for a session.
        
        Args:
            chat_id: Chat session ID
            limit: Maximum number of messages to return
            
        Returns:
            List of messages with metadata
        """
        try:
            cursor = self.messages_collection.find(
                {"chat_id": ObjectId(chat_id)}
            ).sort("created_at", -1).limit(limit)
            
            messages = await cursor.to_list(length=None)
            messages.reverse()  # Show in chronological order
            
            return [
                {
                    "id": str(msg["_id"]),
                    "content": msg["content"],
                    "role": msg["role"],
                    "created_at": msg["created_at"],
                    "tokens_used": msg.get("tokens_used")
                }
                for msg in messages
            ]
            
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    async def process_chat_request(self, chat_request: ChatRequest) -> ChatResponse:
        """
        Process a chat request and generate RAG response.
        
        Args:
            chat_request: Chat request with user message
            
        Returns:
            Chat response with assistant message
        """
        try:
            # Get or create chat session
            chat_id = chat_request.chat_id
            if not chat_id:
                chat_id = await self.create_chat_session()
            
            # Add user message to chat
            await self.add_message(chat_id, chat_request.message, "user")
            
            # Search for relevant document chunks
            relevant_chunks = await document_service.search_documents(chat_request.message)
            
            # Extract just the text chunks for context
            context_chunks = [chunk["chunk"] for chunk in relevant_chunks]
            
            # Get chat history for context
            chat_history = await self.get_chat_history(chat_id, limit=5)
            
            # Format chat history for Groq
            formatted_history = []
            for msg in chat_history:
                formatted_history.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Generate response using Groq
            groq_response = groq_service.generate_chat_response(
                chat_request.message,
                context_chunks,
                formatted_history
            )
            
            # Add assistant message to chat
            await self.add_message(
                chat_id, 
                groq_response["response"], 
                "assistant",
                groq_response["total_tokens"]
            )
            
            # Prepare sources information
            sources = []
            for chunk in relevant_chunks[:3]:  # Top 3 sources
                sources.append(f"{chunk['document_title']} (similarity: {chunk['similarity']:.3f})")
            
            return ChatResponse(
                message=groq_response["response"],
                chat_id=chat_id,
                sources=sources,
                tokens_used=groq_response["total_tokens"]
            )
            
        except Exception as e:
            print(f"Error processing chat request: {e}")
            # Return error response
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            
            if chat_id:
                await self.add_message(chat_id, error_message, "assistant")
            
            return ChatResponse(
                message=error_message,
                chat_id=chat_id or "error",
                sources=[],
                tokens_used=0
            )
    
    async def get_chat_sessions(self) -> List[Dict[str, Any]]:
        """
        Get all chat sessions.
        
        Returns:
            List of chat sessions with metadata
        """
        try:
            cursor = self.chats_collection.find().sort("updated_at", -1)
            chats = await cursor.to_list(length=None)
            
            return [
                {
                    "id": str(chat["_id"]),
                    "created_at": chat["created_at"],
                    "updated_at": chat["updated_at"],
                    "message_count": chat["message_count"],
                    "total_tokens": chat["total_tokens"]
                }
                for chat in chats
            ]
            
        except Exception as e:
            print(f"Error getting chat sessions: {e}")
            return []
    
    async def delete_chat_session(self, chat_id: str) -> bool:
        """
        Delete a chat session and all its messages.
        
        Args:
            chat_id: Chat session ID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            # Delete all messages in the chat
            await self.messages_collection.delete_many({"chat_id": ObjectId(chat_id)})
            
            # Delete the chat session
            result = await self.chats_collection.delete_one({"_id": ObjectId(chat_id)})
            
            return result.deleted_count > 0
            
        except Exception as e:
            print(f"Error deleting chat session: {e}")
            return False

# Global chat service instance - will be created when needed
chat_service = None

def get_chat_service():
    """Get the chat service instance."""
    global chat_service
    if chat_service is None:
        chat_service = ChatService()
    return chat_service
