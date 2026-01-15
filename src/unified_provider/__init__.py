"""
Unified API Provider for LLM and Embedding Models.

This package provides a unified interface for accessing both LLM (chat/completion)
and embedding APIs through a single provider and API key, eliminating the need
for separate OpenRouter and OpenAI/Gemini configurations.
"""

from .client import UnifiedProviderClient
from .config import ProviderConfig, ProviderType
from .exceptions import (
    ProviderError,
    ConfigurationError,
    APIError,
    RateLimitError,
    AuthenticationError,
)
from .models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
)

__all__ = [
    "UnifiedProviderClient",
    "ProviderConfig",
    "ProviderType",
    "ProviderError",
    "ConfigurationError",
    "APIError",
    "RateLimitError",
    "AuthenticationError",
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "EmbeddingRequest",
    "EmbeddingResponse",
]

__version__ = "0.1.0"
