from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId
from ..core.database import db
from ..models.document import DocumentCreate, DocumentInDB, DocumentResponse
from .embedding_service import embedding_service

class DocumentService:
    """Service for managing documents and their embeddings."""
    
    def __init__(self):
        """Initialize the document service."""
        self.collection_name = "documents"
    
    @property
    def collection(self):
        """Get the collection lazily."""
        return db.get_collection(self.collection_name)
    
    async def create_document(self, document_data: DocumentCreate) -> DocumentResponse:
        """
        Create a new document with embeddings.
        
        Args:
            document_data: Document data to create
            
        Returns:
            Created document response
        """
        try:
            # Process text and generate embeddings
            chunks, embeddings = embedding_service.process_text(document_data.content)
            
            # Create document in database
            document = DocumentInDB(
                title=document_data.title,
                content=document_data.content,
                source=document_data.source,
                chunks=chunks,
                embeddings=embeddings
            )
            
            # Convert to dict and insert
            doc_dict = document.dict(by_alias=True)
            result = await self.collection.insert_one(doc_dict)
            
            # Get the created document
            created_doc = await self.collection.find_one({"_id": result.inserted_id})
            
            return self._format_document_response(created_doc)
            
        except Exception as e:
            print(f"Error creating document: {e}")
            raise e
    
    async def get_document(self, document_id: str) -> Optional[DocumentResponse]:
        """
        Get a document by ID.
        
        Args:
            document_id: Document ID
            
        Returns:
            Document response or None
        """
        try:
            doc = await self.collection.find_one({"_id": ObjectId(document_id)})
            if doc:
                return self._format_document_response(doc)
            return None
        except Exception as e:
            print(f"Error getting document: {e}")
            return None
    
    async def get_all_documents(self) -> List[DocumentResponse]:
        """
        Get all documents.
        
        Returns:
            List of document responses
        """
        try:
            cursor = self.collection.find().sort("created_at", -1)
            documents = await cursor.to_list(length=None)
            return [self._format_document_response(doc) for doc in documents]
        except Exception as e:
            print(f"Error getting all documents: {e}")
            return []
    
    async def delete_document(self, document_id: str) -> bool:
        """
        Delete a document by ID.
        
        Args:
            document_id: Document ID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            result = await self.collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    async def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search documents using semantic similarity.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant document chunks with metadata
        """
        try:
            # Get all documents and their embeddings
            all_docs = await self.collection.find({}).to_list(length=None)
            
            if not all_docs:
                return []
            
            # Collect all chunks and embeddings
            all_chunks = []
            all_embeddings = []
            chunk_metadata = []
            
            for doc in all_docs:
                if doc.get("chunks") and doc.get("embeddings"):
                    for i, (chunk, embedding) in enumerate(zip(doc["chunks"], doc["embeddings"])):
                        all_chunks.append(chunk)
                        all_embeddings.append(embedding)
                        chunk_metadata.append({
                            "document_id": str(doc["_id"]),
                            "document_title": doc["title"],
                            "chunk_index": i,
                            "source": doc["source"]
                        })
            
            # Find similar chunks
            similar_chunks = embedding_service.find_similar_chunks(
                query, all_embeddings, all_chunks, top_k
            )
            
            # Format results with metadata
            results = []
            for chunk, similarity in similar_chunks:
                chunk_index = all_chunks.index(chunk)
                metadata = chunk_metadata[chunk_index]
                results.append({
                    "chunk": chunk,
                    "similarity": similarity,
                    "document_id": metadata["document_id"],
                    "document_title": metadata["document_title"],
                    "source": metadata["source"]
                })
            
            return results
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    async def get_document_stats(self) -> Dict[str, Any]:
        """
        Get document statistics.
        
        Returns:
            Dictionary with document statistics
        """
        try:
            total_documents = await self.collection.count_documents({})
            total_chunks = await self.collection.aggregate([
                {"$group": {"_id": None, "total": {"$sum": {"$size": "$chunks"}}}}
            ]).to_list(length=1)
            
            total_chunks_count = total_chunks[0]["total"] if total_chunks else 0
            
            return {
                "total_documents": total_documents,
                "total_chunks": total_chunks_count,
                "average_chunks_per_document": total_chunks_count / total_documents if total_documents > 0 else 0
            }
        except Exception as e:
            print(f"Error getting document stats: {e}")
            return {"total_documents": 0, "total_chunks": 0, "average_chunks_per_document": 0}
    
    def _format_document_response(self, doc: Dict[str, Any]) -> DocumentResponse:
        """
        Format database document to response model.
        
        Args:
            doc: Database document
            
        Returns:
            Formatted document response
        """
        return DocumentResponse(
            id=str(doc["_id"]),
            title=doc["title"],
            content=doc["content"],
            source=doc["source"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
            chunk_count=len(doc.get("chunks", []))
        )

# Global document service instance - will be created when needed
document_service = None

def get_document_service():
    """Get the document service instance."""
    global document_service
    if document_service is None:
        document_service = DocumentService()
    return document_service
