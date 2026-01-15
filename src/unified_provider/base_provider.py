"""Base provider interface."""

from abc import ABC, abstractmethod
from typing import Optional

from .models import ChatRequest, ChatResponse, EmbeddingRequest, EmbeddingResponse
from .config import ProviderConfig


class BaseProvider(ABC):
    """
    Abstract base class for provider implementations.
    
    Each provider must implement methods for chat completion and embeddings.
    """
    
    def __init__(self, config: ProviderConfig):
        """
        Initialize provider.
        
        Args:
            config: Provider configuration
        """
        self.config = config
        config.validate()
    
    @abstractmethod
    async def chat_completion(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Generate chat completion.
        
        Args:
            request: Chat completion request
            
        Returns:
            Chat completion response
            
        Raises:
            APIError: If API request fails
            RateLimitError: If rate limit is exceeded
            AuthenticationError: If authentication fails
        """
        pass
    
    @abstractmethod
    async def create_embedding(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Create text embeddings.
        
        Args:
            request: Embedding request
            
        Returns:
            Embedding response
            
        Raises:
            APIError: If API request fails
            RateLimitError: If rate limit is exceeded
            AuthenticationError: If authentication fails
        """
        pass
    
    @abstractmethod
    def chat_completion_sync(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Generate chat completion (synchronous).
        
        Args:
            request: Chat completion request
            
        Returns:
            Chat completion response
            
        Raises:
            APIError: If API request fails
            RateLimitError: If rate limit is exceeded
            AuthenticationError: If authentication fails
        """
        pass
    
    @abstractmethod
    def create_embedding_sync(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Create text embeddings (synchronous).
        
        Args:
            request: Embedding request
            
        Returns:
            Embedding response
            
        Raises:
            APIError: If API request fails
            RateLimitError: If rate limit is exceeded
            AuthenticationError: If authentication fails
        """
        pass
