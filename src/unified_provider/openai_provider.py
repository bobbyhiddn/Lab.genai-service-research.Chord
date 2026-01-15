"""OpenAI provider implementation."""

from typing import Optional, Any, Dict
import httpx

from .base_provider import BaseProvider
from .config import ProviderConfig
from .models import (
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    MessageRole,
)
from .exceptions import (
    APIError,
    RateLimitError,
    AuthenticationError,
)


class OpenAIProvider(BaseProvider):
    """
    OpenAI provider implementation.
    
    Provides access to OpenAI's chat completion and embedding APIs
    using a single API key.
    """
    
    def __init__(self, config: ProviderConfig):
        """Initialize OpenAI provider."""
        super().__init__(config)
        self.base_url = config.base_url or "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        }
    
    def _handle_error(self, response: httpx.Response) -> None:
        """
        Handle API error responses.
        
        Args:
            response: HTTP response object
            
        Raises:
            AuthenticationError: If authentication failed
            RateLimitError: If rate limit exceeded
            APIError: For other API errors
        """
        try:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", str(error_data))
        except Exception:
            error_message = response.text
        
        if response.status_code == 401:
            raise AuthenticationError(
                f"Authentication failed: {error_message}",
                provider="openai",
            )
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                f"Rate limit exceeded: {error_message}",
                provider="openai",
                retry_after=int(retry_after) if retry_after else None,
            )
        else:
            raise APIError(
                f"API request failed: {error_message}",
                provider="openai",
                status_code=response.status_code,
                response_data=error_data if 'error_data' in locals() else None,
            )
    
    async def chat_completion(self, request: ChatRequest) -> ChatResponse:
        """Generate chat completion using OpenAI API."""
        model = request.model or self.config.default_llm_model
        
        payload = request.to_dict()
        payload["model"] = model
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
            )
            
            if response.status_code != 200:
                self._handle_error(response)
            
            data = response.json()
            
            choice = data["choices"][0]
            message = choice["message"]
            
            return ChatResponse(
                id=data["id"],
                model=data["model"],
                content=message["content"],
                role=MessageRole(message["role"]),
                finish_reason=choice.get("finish_reason"),
                usage=data.get("usage"),
                raw_response=data,
            )
    
    async def create_embedding(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Create embeddings using OpenAI API."""
        model = request.model or self.config.default_embedding_model
        
        payload = request.to_dict()
        payload["model"] = model
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                f"{self.base_url}/embeddings",
                headers=self.headers,
                json=payload,
            )
            
            if response.status_code != 200:
                self._handle_error(response)
            
            data = response.json()
            
            # Extract embeddings from response
            embeddings = [item["embedding"] for item in data["data"]]
            
            return EmbeddingResponse(
                embeddings=embeddings,
                model=data["model"],
                usage=data.get("usage"),
                raw_response=data,
            )
    
    def chat_completion_sync(self, request: ChatRequest) -> ChatResponse:
        """Generate chat completion using OpenAI API (synchronous)."""
        model = request.model or self.config.default_llm_model
        
        payload = request.to_dict()
        payload["model"] = model
        
        with httpx.Client(timeout=self.config.timeout) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
            )
            
            if response.status_code != 200:
                self._handle_error(response)
            
            data = response.json()
            
            choice = data["choices"][0]
            message = choice["message"]
            
            return ChatResponse(
                id=data["id"],
                model=data["model"],
                content=message["content"],
                role=MessageRole(message["role"]),
                finish_reason=choice.get("finish_reason"),
                usage=data.get("usage"),
                raw_response=data,
            )
    
    def create_embedding_sync(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Create embeddings using OpenAI API (synchronous)."""
        model = request.model or self.config.default_embedding_model
        
        payload = request.to_dict()
        payload["model"] = model
        
        with httpx.Client(timeout=self.config.timeout) as client:
            response = client.post(
                f"{self.base_url}/embeddings",
                headers=self.headers,
                json=payload,
            )
            
            if response.status_code != 200:
                self._handle_error(response)
            
            data = response.json()
            
            # Extract embeddings from response
            embeddings = [item["embedding"] for item in data["data"]]
            
            return EmbeddingResponse(
                embeddings=embeddings,
                model=data["model"],
                usage=data.get("usage"),
                raw_response=data,
            )
