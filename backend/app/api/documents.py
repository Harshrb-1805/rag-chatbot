from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
import aiofiles
import os
from ..models.document import DocumentCreate, DocumentResponse, DocumentList
from ..services.document_service import get_document_service
from ..core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(None)
):
    """
    Upload a text document file and generate embeddings.
    
    Args:
        file: Text file to upload
        title: Optional custom title for the document
        
    Returns:
        Created document with metadata
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.txt'):
            raise HTTPException(
                status_code=400, 
                detail="Only .txt files are supported"
            )
        
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Use filename as title if not provided
        if not title:
            title = os.path.splitext(file.filename)[0]
        
        # Create document
        document_data = DocumentCreate(
            title=title,
            content=text_content,
            source=f"File upload: {file.filename}"
        )
        
        document = await get_document_service().create_document(document_data)
        return document
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/paste", response_model=DocumentResponse)
async def paste_text(
    title: str = Form(...),
    content: str = Form(...)
):
    """
    Create a document from pasted text and generate embeddings.
    
    Args:
        title: Document title
        content: Text content
        
    Returns:
        Created document with metadata
    """
    try:
        if not content.strip():
            raise HTTPException(
                status_code=400, 
                detail="Content cannot be empty"
            )
        
        document_data = DocumentCreate(
            title=title,
            content=content.strip(),
            source="Text paste"
        )
        
        document = await get_document_service().create_document(document_data)
        return document
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=DocumentList)
async def get_documents():
    """
    Get all uploaded documents.
    
    Returns:
        List of documents with metadata
    """
    try:
        documents = await get_document_service().get_all_documents()
        return DocumentList(
            documents=documents,
            total=len(documents)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """
    Get a specific document by ID.
    
    Args:
        document_id: Document ID
        
    Returns:
        Document with metadata
    """
    try:
        document = await get_document_service().get_document(document_id)
        if not document:
            raise HTTPException(
                status_code=404, 
                detail="Document not found"
            )
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document by ID.
    
    Args:
        document_id: Document ID
        
    Returns:
        Success message
    """
    try:
        success = await get_document_service().delete_document(document_id)
        if not success:
            raise HTTPException(
                status_code=404, 
                detail="Document not found"
            )
        return {"message": "Document deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_document_stats():
    """
    Get document statistics summary.
    
    Returns:
        Document statistics
    """
    try:
        stats = await get_document_service().get_document_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
