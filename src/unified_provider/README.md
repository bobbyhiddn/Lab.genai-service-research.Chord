# Unified Provider Client

A unified Python client for accessing both LLM (chat completion) and embedding APIs through a single provider and API key.

## Overview

This library solves the problem of managing multiple API keys for LLM and embedding services by providing a unified interface that works with providers offering both capabilities under a single API key.

### Problem Statement

Previously, projects using both LLM and embedding models required:
- **OpenRouter** for LLM access (model garden)
- **OpenAI or Gemini** for embedding models

OpenRouter doesn't serve embedding models, forcing a multi-key setup with increased complexity and management overhead.

### Solution

The Unified Provider Client provides:
- Single API key for both LLM and embedding access
- Consistent interface across different providers
- Easy configuration via environment variables or code
- Support for both synchronous and asynchronous operations
- Comprehensive error handling

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Basic Usage with OpenAI

```python
from unified_provider import (
    UnifiedProviderClient,
    ProviderConfig,
    ProviderType,
    ChatRequest,
    ChatMessage,
    MessageRole,
    EmbeddingRequest,
)

# Create configuration
config = ProviderConfig(
    provider=ProviderType.OPENAI,
    api_key="your-openai-api-key",
)

# Initialize client
client = UnifiedProviderClient(config)

# Chat completion
chat_request = ChatRequest(
    messages=[
        ChatMessage(role=MessageRole.USER, content="What is the capital of France?"),
    ],
)
response = client.chat_completion_sync(chat_request)
print(response.content)

# Embeddings
embedding_request = EmbeddingRequest(
    input="Hello world",
)
embedding_response = client.create_embedding_sync(embedding_request)
print(f"Embedding dimension: {len(embedding_response.embeddings[0])}")
```

### Using Environment Variables

```python
# Set environment variables:
# export UNIFIED_API_KEY="your-api-key"
# export UNIFIED_PROVIDER="openai"
# export UNIFIED_LLM_MODEL="gpt-4-turbo-preview"
# export UNIFIED_EMBEDDING_MODEL="text-embedding-3-small"

from unified_provider import UnifiedProviderClient

# Load from environment
client = UnifiedProviderClient.from_env()

# Use the client
response = client.chat_completion_sync(chat_request)
```

### Asynchronous Usage

```python
import asyncio
from unified_provider import UnifiedProviderClient, ChatRequest, ChatMessage, MessageRole

async def main():
    client = UnifiedProviderClient.from_env()
    
    request = ChatRequest(
        messages=[ChatMessage(role=MessageRole.USER, content="Hello!")],
    )
    
    response = await client.chat_completion(request)
    print(response.content)

asyncio.run(main())
```

## Configuration

### ProviderConfig Options

```python
from unified_provider import ProviderConfig, ProviderType

config = ProviderConfig(
    provider=ProviderType.OPENAI,           # Provider type
    api_key="your-api-key",                 # API key (required)
    base_url="https://api.openai.com/v1",  # Custom base URL (optional)
    default_llm_model="gpt-4-turbo-preview",# Default LLM model
    default_embedding_model="text-embedding-3-small",  # Default embedding model
    timeout=60,                             # Request timeout in seconds
    max_retries=3,                          # Maximum retry attempts
    additional_params={},                   # Provider-specific parameters
)
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `UNIFIED_API_KEY` | API key for the provider | Required |
| `UNIFIED_PROVIDER` | Provider type (openai, google, together, etc.) | `openai` |
| `UNIFIED_LLM_MODEL` | Default LLM model | Provider-specific |
| `UNIFIED_EMBEDDING_MODEL` | Default embedding model | Provider-specific |
| `UNIFIED_BASE_URL` | Custom API base URL | Provider-specific |
| `UNIFIED_TIMEOUT` | Request timeout in seconds | `60` |
| `UNIFIED_MAX_RETRIES` | Maximum retry attempts | `3` |

## Supported Providers

### OpenAI ✅ (Implemented)

**Status**: Fully implemented and recommended

**Models**:
- LLM: GPT-4, GPT-4 Turbo, GPT-3.5 Turbo
- Embeddings: text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002

**Configuration**:
```python
config = ProviderConfig(
    provider=ProviderType.OPENAI,
    api_key="sk-...",
    default_llm_model="gpt-4-turbo-preview",
    default_embedding_model="text-embedding-3-small",
)
```

### Azure OpenAI ✅ (Implemented)

**Status**: Uses same implementation as OpenAI with custom base URL

**Configuration**:
```python
config = ProviderConfig(
    provider=ProviderType.AZURE_OPENAI,
    api_key="your-azure-key",
    base_url="https://your-resource.openai.azure.com/openai/deployments/your-deployment",
    default_llm_model="gpt-4",
    default_embedding_model="text-embedding-ada-002",
)
```

### Google AI (Gemini) 🚧 (Planned)

**Status**: Not yet implemented

To contribute: See [Contributing](#contributing) section.

### Together AI 🚧 (Planned)

**Status**: Not yet implemented

To contribute: See [Contributing](#contributing) section.

### Anyscale 🚧 (Planned)

**Status**: Not yet implemented

To contribute: See [Contributing](#contributing) section.

## API Reference

### UnifiedProviderClient

Main client class for interacting with providers.

#### Methods

##### `__init__(config: ProviderConfig)`
Initialize client with configuration.

##### `chat_completion_sync(request: ChatRequest) -> ChatResponse`
Generate chat completion (synchronous).

##### `chat_completion(request: ChatRequest) -> ChatResponse` (async)
Generate chat completion (asynchronous).

##### `create_embedding_sync(request: EmbeddingRequest) -> EmbeddingResponse`
Create text embeddings (synchronous).

##### `create_embedding(request: EmbeddingRequest) -> EmbeddingResponse` (async)
Create text embeddings (asynchronous).

##### `from_env() -> UnifiedProviderClient` (classmethod)
Create client from environment variables.

### ChatRequest

Request for chat completion.

**Fields**:
- `messages: List[ChatMessage]` - List of messages in conversation
- `model: Optional[str]` - Model to use (defaults to config)
- `temperature: float` - Sampling temperature (0-2)
- `max_tokens: Optional[int]` - Maximum tokens to generate
- `top_p: float` - Nucleus sampling parameter
- `frequency_penalty: float` - Frequency penalty (-2.0 to 2.0)
- `presence_penalty: float` - Presence penalty (-2.0 to 2.0)
- `stop: Optional[List[str]]` - Stop sequences
- `stream: bool` - Whether to stream response
- `additional_params: Dict[str, Any]` - Provider-specific parameters

### ChatResponse

Response from chat completion.

**Fields**:
- `id: str` - Unique response identifier
- `model: str` - Model used
- `content: str` - Generated content
- `role: MessageRole` - Response role (typically 'assistant')
- `finish_reason: Optional[str]` - Completion reason
- `usage: Optional[Dict[str, int]]` - Token usage information
- `raw_response: Optional[Dict[str, Any]]` - Raw provider response

### EmbeddingRequest

Request for text embeddings.

**Fields**:
- `input: List[str] | str` - Text(s) to embed
- `model: Optional[str]` - Model to use (defaults to config)
- `encoding_format: Literal["float", "base64"]` - Embedding format
- `dimensions: Optional[int]` - Dimension override (if supported)
- `additional_params: Dict[str, Any]` - Provider-specific parameters

### EmbeddingResponse

Response from embedding request.

**Fields**:
- `embeddings: List[List[float]]` - Embedding vectors
- `model: str` - Model used
- `usage: Optional[Dict[str, int]]` - Token usage information
- `raw_response: Optional[Dict[str, Any]]` - Raw provider response

## Error Handling

The library provides comprehensive error handling:

```python
from unified_provider import (
    ProviderError,
    ConfigurationError,
    APIError,
    RateLimitError,
    AuthenticationError,
)

try:
    response = client.chat_completion_sync(request)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    print(f"Provider: {e.provider}")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    print(f"Retry after: {e.retry_after} seconds")
except APIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Response: {e.response_data}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except ProviderError as e:
    print(f"Provider error: {e}")
```

### Exception Hierarchy

- `ProviderError` - Base exception
  - `ConfigurationError` - Configuration or initialization error
  - `APIError` - API request failed
    - `RateLimitError` - Rate limit exceeded
    - `AuthenticationError` - Authentication failed
  - `ModelNotFoundError` - Requested model not available
  - `ValidationError` - Request validation failed

## Examples

See [`examples.py`](./examples.py) for comprehensive examples including:
- Synchronous usage
- Asynchronous usage
- Error handling
- Configuration options

## Migration Guide

### From Dual OpenRouter/OpenAI Setup

**Before**:
```python
# LLM with OpenRouter
openrouter_client = OpenRouterClient(api_key="openrouter-key")
llm_response = openrouter_client.chat(...)

# Embeddings with OpenAI
openai_client = OpenAI(api_key="openai-key")
embedding = openai_client.embeddings.create(...)
```

**After**:
```python
# Both with single client
from unified_provider import UnifiedProviderClient

client = UnifiedProviderClient.from_env()
llm_response = client.chat_completion_sync(...)
embedding = client.create_embedding_sync(...)
```

## Best Practices

1. **Use Environment Variables**: Store API keys in environment variables, never in code
2. **Error Handling**: Always handle provider-specific errors
3. **Async for Production**: Use async methods for better performance in production
4. **Model Selection**: Explicitly specify models for reproducibility
5. **Token Management**: Monitor usage through response objects
6. **Rate Limiting**: Implement exponential backoff for rate limit errors

## Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=unified_provider tests/
```

## Contributing

Contributions are welcome! To add support for additional providers:

1. Create a new provider class inheriting from `BaseProvider`
2. Implement required methods: `chat_completion`, `create_embedding`, and sync variants
3. Add provider to `ProviderType` enum
4. Update `UnifiedProviderClient._create_provider()` factory method
5. Add tests for the new provider
6. Update documentation

See `openai_provider.py` as a reference implementation.

## Architecture

The library follows these design principles:
- **Provider Pattern**: Abstract provider interface with concrete implementations
- **Factory Pattern**: Client creates appropriate provider based on configuration
- **Dependency Inversion**: High-level client doesn't depend on specific providers
- **Single Responsibility**: Each component has one clear purpose
- **Open/Closed**: Open for extension (new providers), closed for modification

## License

This project was created by LEGATO.

## Support

For issues or questions:
1. Check the documentation above
2. Review [examples.py](./examples.py)
3. See [unified-provider-research.md](../../docs/unified-provider-research.md) for provider comparison
4. Open an issue on GitHub

---

*Unified Provider Client - Simplifying LLM and embedding access*
