"""Example usage of the unified provider client."""

import asyncio
from unified_provider import (
    UnifiedProviderClient,
    ProviderConfig,
    ProviderType,
    ChatRequest,
    ChatMessage,
    MessageRole,
    EmbeddingRequest,
)


def example_sync_usage():
    """Example of synchronous usage."""
    # Create configuration
    config = ProviderConfig(
        provider=ProviderType.OPENAI,
        api_key="your-api-key-here",
        default_llm_model="gpt-4-turbo-preview",
        default_embedding_model="text-embedding-3-small",
    )
    
    # Or load from environment variables
    # config = ProviderConfig.from_env()
    
    # Initialize client
    client = UnifiedProviderClient(config)
    
    # Chat completion example
    print("=== Chat Completion ===")
    chat_request = ChatRequest(
        messages=[
            ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
            ChatMessage(role=MessageRole.USER, content="What is the capital of France?"),
        ],
        temperature=0.7,
        max_tokens=100,
    )
    
    chat_response = client.chat_completion_sync(chat_request)
    print(f"Response: {chat_response.content}")
    print(f"Model: {chat_response.model}")
    print(f"Usage: {chat_response.usage}")
    
    # Embedding example
    print("\n=== Embeddings ===")
    embedding_request = EmbeddingRequest(
        input=["Hello world", "How are you?"],
    )
    
    embedding_response = client.create_embedding_sync(embedding_request)
    print(f"Number of embeddings: {len(embedding_response.embeddings)}")
    print(f"Embedding dimension: {len(embedding_response.embeddings[0])}")
    print(f"Model: {embedding_response.model}")
    print(f"Usage: {embedding_response.usage}")


async def example_async_usage():
    """Example of asynchronous usage."""
    # Load configuration from environment
    client = UnifiedProviderClient.from_env()
    
    # Async chat completion
    print("=== Async Chat Completion ===")
    chat_request = ChatRequest(
        messages=[
            ChatMessage(role=MessageRole.USER, content="Tell me a short joke."),
        ],
        temperature=0.9,
    )
    
    chat_response = await client.chat_completion(chat_request)
    print(f"Response: {chat_response.content}")
    
    # Async embeddings
    print("\n=== Async Embeddings ===")
    embedding_request = EmbeddingRequest(
        input="The quick brown fox jumps over the lazy dog.",
    )
    
    embedding_response = await client.create_embedding(embedding_request)
    print(f"Embedding dimension: {len(embedding_response.embeddings[0])}")


def example_error_handling():
    """Example of error handling."""
    from unified_provider import (
        APIError,
        RateLimitError,
        AuthenticationError,
    )
    
    config = ProviderConfig(
        provider=ProviderType.OPENAI,
        api_key="invalid-key",
    )
    
    client = UnifiedProviderClient(config)
    
    try:
        request = ChatRequest(
            messages=[ChatMessage(role=MessageRole.USER, content="Hello")],
        )
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


if __name__ == "__main__":
    # Run sync example
    print("Running synchronous example...")
    # example_sync_usage()
    
    # Run async example
    print("\nRunning asynchronous example...")
    # asyncio.run(example_async_usage())
    
    # Run error handling example
    print("\nRunning error handling example...")
    # example_error_handling()
    
    print("\nExamples are commented out to prevent actual API calls.")
    print("Uncomment the examples above and set your API key to run them.")
