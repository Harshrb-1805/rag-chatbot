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

class DocumentBase(BaseModel):
    """Base document model."""
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    source: str = Field(..., description="Document source (file or pasted)")
    
    class Config:
        json_encoders = {ObjectId: str}

class DocumentCreate(DocumentBase):
    """Model for creating a new document."""
    pass

class DocumentInDB(DocumentBase):
    """Model for document stored in database."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    chunks: List[str] = Field(default_factory=list, description="Text chunks for embedding")
    embeddings: List[List[float]] = Field(default_factory=list, description="Vector embeddings")
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class DocumentResponse(DocumentBase):
    """Model for document response."""
    id: str
    created_at: datetime
    updated_at: datetime
    chunk_count: int
    
    class Config:
        json_encoders = {ObjectId: str}

class DocumentList(BaseModel):
    """Model for list of documents."""
    documents: List[DocumentResponse]
    total: int
