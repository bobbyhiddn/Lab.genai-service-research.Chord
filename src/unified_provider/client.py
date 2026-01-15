"""Unified provider client."""

from typing import Optional

from .base_provider import BaseProvider
from .config import ProviderConfig, ProviderType
from .models import ChatRequest, ChatResponse, EmbeddingRequest, EmbeddingResponse
from .openai_provider import OpenAIProvider
from .exceptions import ConfigurationError


class UnifiedProviderClient:
    """
    Unified client for accessing LLM and embedding APIs.
    
    This client provides a single interface for both chat completion
    and embedding requests, abstracting away the specific provider
    implementation.
    
    Example:
        >>> from unified_provider import UnifiedProviderClient, ProviderConfig, ProviderType
        >>> 
        >>> # Create config
        >>> config = ProviderConfig(
        ...     provider=ProviderType.OPENAI,
        ...     api_key="your-api-key",
        ... )
        >>> 
        >>> # Initialize client
        >>> client = UnifiedProviderClient(config)
        >>> 
        >>> # Chat completion
        >>> from unified_provider import ChatRequest, ChatMessage, MessageRole
        >>> request = ChatRequest(
        ...     messages=[ChatMessage(role=MessageRole.USER, content="Hello!")],
        ... )
        >>> response = client.chat_completion_sync(request)
        >>> print(response.content)
        >>> 
        >>> # Embeddings
        >>> from unified_provider import EmbeddingRequest
        >>> request = EmbeddingRequest(input="Hello world")
        >>> response = client.create_embedding_sync(request)
        >>> print(len(response.embeddings[0]))
    """
    
    def __init__(self, config: ProviderConfig):
        """
        Initialize unified provider client.
        
        Args:
            config: Provider configuration
            
        Raises:
            ConfigurationError: If configuration is invalid or provider not supported
        """
        self.config = config
        self._provider = self._create_provider(config)
    
    def _create_provider(self, config: ProviderConfig) -> BaseProvider:
        """
        Create provider instance based on configuration.
        
        Args:
            config: Provider configuration
            
        Returns:
            Provider instance
            
        Raises:
            ConfigurationError: If provider type not supported
        """
        if config.provider == ProviderType.OPENAI:
            return OpenAIProvider(config)
        elif config.provider == ProviderType.AZURE_OPENAI:
            # Azure OpenAI uses the same API structure as OpenAI
            # but with different base URL
            return OpenAIProvider(config)
        elif config.provider == ProviderType.GOOGLE:
            raise ConfigurationError(
                "Google AI provider not yet implemented. "
                "Please use OpenAI provider or contribute a Google implementation.",
                provider="google",
            )
        elif config.provider == ProviderType.TOGETHER:
            raise ConfigurationError(
                "Together AI provider not yet implemented. "
                "Please use OpenAI provider or contribute a Together implementation.",
                provider="together",
            )
        elif config.provider == ProviderType.ANYSCALE:
            raise ConfigurationError(
                "Anyscale provider not yet implemented. "
                "Please use OpenAI provider or contribute an Anyscale implementation.",
                provider="anyscale",
            )
        else:
            raise ConfigurationError(
                f"Unsupported provider type: {config.provider}",
                provider=config.provider.value,
            )
    
    async def chat_completion(self, request: ChatRequest) -> ChatResponse:
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
        return await self._provider.chat_completion(request)
    
    async def create_embedding(self, request: EmbeddingRequest) -> EmbeddingResponse:
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
        return await self._provider.create_embedding(request)
    
    def chat_completion_sync(self, request: ChatRequest) -> ChatResponse:
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
        return self._provider.chat_completion_sync(request)
    
    def create_embedding_sync(self, request: EmbeddingRequest) -> EmbeddingResponse:
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
        return self._provider.create_embedding_sync(request)
    
    @classmethod
    def from_env(cls) -> "UnifiedProviderClient":
        """
        Create client from environment variables.
        
        Environment variables:
            UNIFIED_API_KEY: API key for the provider
            UNIFIED_PROVIDER: Provider type (default: openai)
            UNIFIED_LLM_MODEL: Default LLM model (optional)
            UNIFIED_EMBEDDING_MODEL: Default embedding model (optional)
            UNIFIED_BASE_URL: Custom base URL (optional)
            UNIFIED_TIMEOUT: Request timeout in seconds (default: 60)
            UNIFIED_MAX_RETRIES: Maximum retry attempts (default: 3)
        
        Returns:
            UnifiedProviderClient instance
            
        Raises:
            ValueError: If required environment variables are missing
            ConfigurationError: If configuration is invalid
        """
        config = ProviderConfig.from_env()
        return cls(config)
