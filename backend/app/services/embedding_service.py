import re
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from ..core.config import get_settings

settings = get_settings()

class EmbeddingService:
    """Service for generating text embeddings."""
    
    def __init__(self):
        """Initialize the embedding service with the specified model."""
        self.model = SentenceTransformer(settings.embedding_model)
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks for better embedding generation.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Split into sentences first
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    # Start new chunk with overlap
                    overlap_start = max(0, len(current_chunk) - self.chunk_overlap)
                    current_chunk = current_chunk[overlap_start:] + " " + sentence
                else:
                    # If single sentence is too long, split it
                    if len(sentence) > self.chunk_size:
                        words = sentence.split()
                        temp_chunk = ""
                        for word in words:
                            if len(temp_chunk) + len(word) + 1 <= self.chunk_size:
                                temp_chunk += " " + word if temp_chunk else word
                            else:
                                if temp_chunk:
                                    chunks.append(temp_chunk.strip())
                                temp_chunk = word
                        current_chunk = temp_chunk
                    else:
                        current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def generate_embeddings(self, chunks: List[str]) -> List[List[float]]:
        """
        Generate embeddings for text chunks.
        
        Args:
            chunks: List of text chunks
            
        Returns:
            List of embedding vectors
        """
        if not chunks:
            return []
        
        try:
            embeddings = self.model.encode(chunks, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []
    
    def process_text(self, text: str) -> Tuple[List[str], List[List[float]]]:
        """
        Process text by chunking and generating embeddings.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (chunks, embeddings)
        """
        chunks = self.chunk_text(text)
        embeddings = self.generate_embeddings(chunks)
        return chunks, embeddings
    
    def find_similar_chunks(self, query: str, all_embeddings: List[List[float]], 
                           all_chunks: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find most similar chunks for a given query.
        
        Args:
            query: Search query
            all_embeddings: List of all document embeddings
            all_chunks: List of all document chunks
            top_k: Number of top results to return
            
        Returns:
            List of (chunk, similarity_score) tuples
        """
        if not all_embeddings or not all_chunks:
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query], convert_to_tensor=False)
            
            # Calculate similarities
            similarities = []
            for i, doc_embedding in enumerate(all_embeddings):
                # Calculate cosine similarity
                similarity = self._cosine_similarity(query_embedding[0], doc_embedding)
                similarities.append((all_chunks[i], similarity))
            
            # Sort by similarity and return top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
            
        except Exception as e:
            print(f"Error finding similar chunks: {e}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np
        
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

# Global embedding service instance
embedding_service = EmbeddingService()
