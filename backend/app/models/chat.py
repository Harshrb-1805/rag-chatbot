from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId field for Pydantic models."""
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")
        return field_schema
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.json_schema(core_schema.str_schema())

class MessageBase(BaseModel):
    """Base message model."""
    content: str = Field(..., description="Message content")
    role: str = Field(..., description="Message role (user or assistant)")
    
    class Config:
        json_encoders = {ObjectId: str}

class MessageCreate(MessageBase):
    """Model for creating a new message."""
    pass

class MessageInDB(MessageBase):
    """Model for message stored in database."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    chat_id: PyObjectId = Field(..., description="Chat session ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class MessageResponse(MessageBase):
    """Model for message response."""
    id: str
    created_at: datetime
    tokens_used: Optional[int]

class ChatRequest(BaseModel):
    """Model for chat request."""
    message: str = Field(..., description="User message")
    chat_id: Optional[str] = Field(None, description="Existing chat session ID")

class ChatResponse(BaseModel):
    """Model for chat response."""
    message: str = Field(..., description="Assistant response")
    chat_id: str = Field(..., description="Chat session ID")
    sources: List[str] = Field(default_factory=list, description="Source documents used")
    tokens_used: Optional[int] = Field(None, description="Total tokens used")

class ChatSession(BaseModel):
    """Model for chat session."""
    id: str
    created_at: datetime
    updated_at: datetime
    message_count: int
    total_tokens: int
