import groq
from typing import List, Dict, Any
from ..core.config import get_settings

settings = get_settings()

class GroqService:
    """Service for interacting with Groq LLM API."""
    
    def __init__(self):
        """Initialize the Groq service with API key and model."""
        self.client = groq.Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model
    
    def generate_response(self, query: str, context_chunks: List[str], 
                         chat_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response using Groq LLM with RAG context.
        
        Args:
            query: User's question
            context_chunks: Relevant document chunks for context
            chat_history: Previous conversation history
            
        Returns:
            Generated response from the LLM
        """
        try:
            # Prepare the system prompt
            system_prompt = self._create_system_prompt(context_chunks)
            
            # Prepare messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history if available
            if chat_history:
                for msg in chat_history[-5:]:  # Keep last 5 messages for context
                    messages.append(msg)
            
            # Add the current query
            messages.append({"role": "user", "content": query})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response from Groq: {e}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    
    def _create_system_prompt(self, context_chunks: List[str]) -> str:
        """
        Create a system prompt with RAG context.
        
        Args:
            context_chunks: Relevant document chunks
            
        Returns:
            Formatted system prompt
        """
        if not context_chunks:
            return """You are a helpful AI assistant. Please provide accurate and helpful responses based on your knowledge."""
        
        context_text = "\n\n".join([f"Context {i+1}: {chunk}" for i, chunk in enumerate(context_chunks)])
        
        system_prompt = f"""You are a helpful AI assistant with access to the following context information. 
        Please use this context to provide accurate and relevant answers to user questions.

        Context Information:
        {context_text}

        Instructions:
        1. Base your responses primarily on the provided context
        2. If the context doesn't contain enough information to answer the question, say so
        3. Be concise but comprehensive
        4. If you reference specific parts of the context, mention which context section you're referring to
        5. Always be helpful and professional

        Please provide your response based on the context above."""
        
        return system_prompt
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in a text string.
        This is a rough estimation based on average word length.
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        # Rough estimation: 1 token ≈ 4 characters for English text
        return len(text) // 4
    
    def generate_chat_response(self, query: str, context_chunks: List[str], 
                              chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generate a complete chat response with metadata.
        
        Args:
            query: User's question
            context_chunks: Relevant document chunks
            chat_history: Previous conversation history
            
        Returns:
            Dictionary containing response and metadata
        """
        response = self.generate_response(query, context_chunks, chat_history)
        
        # Estimate tokens used
        input_tokens = self.estimate_tokens(query)
        output_tokens = self.estimate_tokens(response)
        total_tokens = input_tokens + output_tokens
        
        return {
            "response": response,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "context_chunks_used": len(context_chunks)
        }

# Global Groq service instance
groq_service = GroqService()
