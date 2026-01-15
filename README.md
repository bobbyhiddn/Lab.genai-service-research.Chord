# Unified API Provider Research

> Research and implementation of a unified API provider for both LLM and embedding models, eliminating the need for separate OpenRouter and OpenAI/Gemini API keys.

## Overview

This project provides a unified client library for accessing both Large Language Model (LLM) chat completion and text embedding APIs through a single provider and API key. The implementation addresses the challenge of managing multiple API keys by consolidating to providers that offer both services.

## Quick Start

```python
from unified_provider import UnifiedProviderClient, ChatRequest, ChatMessage, MessageRole

# Create client from environment variables
client = UnifiedProviderClient.from_env()

# Chat completion
response = client.chat_completion_sync(
    ChatRequest(messages=[ChatMessage(role=MessageRole.USER, content="Hello!")])
)
print(response.content)
```

See [src/unified_provider/README.md](./src/unified_provider/README.md) for detailed documentation.

## Structure

```
├── init/         # Bootstrap and setup
├── plans/        # Phase implementation plans
├── docs/         # Architecture and documentation
├── src/          # Source code
└── tests/        # Test files
```

## Phases

This is a **Chord** project with multiple implementation phases:

1. **Phase 1: Foundation** - Core setup and structure
2. **Phase 2: Core** - Main implementation
3. **Phase 3: Integration** - Connect components

See `/plans` for detailed phase documentation.

## Development

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies (for testing)
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=unified_provider tests/

# Run manual validation
python manual_test.py
```

### Usage Examples

See [src/unified_provider/examples.py](./src/unified_provider/examples.py) for comprehensive usage examples.

### Environment Variables

```bash
export UNIFIED_API_KEY="your-api-key"
export UNIFIED_PROVIDER="openai"  # openai, azure_openai, google, together, anyscale
export UNIFIED_LLM_MODEL="gpt-4-turbo-preview"
export UNIFIED_EMBEDDING_MODEL="text-embedding-3-small"
```

## Architecture

See [docs/architecture.md](./docs/architecture.md) for system design.

## License

This project was created by LEGATO.

---
*Created by LEGATO | [Legato.Conduct](https://github.com/Legato/Legato.Conduct)*
