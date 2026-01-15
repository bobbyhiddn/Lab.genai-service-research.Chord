#!/usr/bin/env python3
"""
Manual test script for the unified provider client.

This script demonstrates the basic functionality of the unified provider
without making actual API calls (unless credentials are provided).
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from unified_provider import (
    UnifiedProviderClient,
    ProviderConfig,
    ProviderType,
    ChatRequest,
    ChatMessage,
    MessageRole,
    EmbeddingRequest,
    ConfigurationError,
)


def test_config_creation():
    """Test configuration creation."""
    print("=" * 60)
    print("Test 1: Configuration Creation")
    print("=" * 60)
    
    # Test basic config
    config = ProviderConfig(
        provider=ProviderType.OPENAI,
        api_key="test-key-123",
        default_llm_model="gpt-4-turbo-preview",
        default_embedding_model="text-embedding-3-small",
    )
    
    print(f"✓ Created config with provider: {config.provider.value}")
    print(f"✓ Default LLM model: {config.default_llm_model}")
    print(f"✓ Default embedding model: {config.default_embedding_model}")
    print(f"✓ Timeout: {config.timeout}s")
    print(f"✓ Max retries: {config.max_retries}")
    
    # Test validation
    try:
        config.validate()
        print("✓ Configuration validation passed")
    except Exception as e:
        print(f"✗ Configuration validation failed: {e}")
        return False
    
    print()
    return True


def test_client_creation():
    """Test client creation with different providers."""
    print("=" * 60)
    print("Test 2: Client Creation")
    print("=" * 60)
    
    # Test OpenAI provider
    config_openai = ProviderConfig(
        provider=ProviderType.OPENAI,
        api_key="test-key",
    )
    
    try:
        client = UnifiedProviderClient(config_openai)
        print("✓ Created client with OpenAI provider")
    except Exception as e:
        print(f"✗ Failed to create OpenAI client: {e}")
        return False
    
    # Test Azure OpenAI provider
    config_azure = ProviderConfig(
        provider=ProviderType.AZURE_OPENAI,
        api_key="test-key",
        base_url="https://test.openai.azure.com",
    )
    
    try:
        client = UnifiedProviderClient(config_azure)
        print("✓ Created client with Azure OpenAI provider")
    except Exception as e:
        print(f"✗ Failed to create Azure client: {e}")
        return False
    
    # Test unsupported provider (should fail)
    config_google = ProviderConfig(
        provider=ProviderType.GOOGLE,
        api_key="test-key",
    )
    
    try:
        client = UnifiedProviderClient(config_google)
        print("✗ Should have failed with unsupported provider")
        return False
    except ConfigurationError as e:
        print(f"✓ Correctly rejected unsupported provider: {e}")
    
    print()
    return True


def test_request_models():
    """Test request model creation."""
    print("=" * 60)
    print("Test 3: Request Models")
    print("=" * 60)
    
    # Test ChatRequest
    chat_request = ChatRequest(
        messages=[
            ChatMessage(role=MessageRole.SYSTEM, content="You are helpful."),
            ChatMessage(role=MessageRole.USER, content="Hello!"),
        ],
        temperature=0.7,
        max_tokens=100,
    )
    
    print(f"✓ Created ChatRequest with {len(chat_request.messages)} messages")
    print(f"  - Temperature: {chat_request.temperature}")
    print(f"  - Max tokens: {chat_request.max_tokens}")
    
    # Convert to dict
    chat_dict = chat_request.to_dict()
    print(f"✓ Converted ChatRequest to dict with {len(chat_dict)} keys")
    
    # Test EmbeddingRequest
    embedding_request = EmbeddingRequest(
        input="Hello world",
        encoding_format="float",
    )
    
    print(f"✓ Created EmbeddingRequest")
    print(f"  - Input: '{embedding_request.input}'")
    print(f"  - Format: {embedding_request.encoding_format}")
    
    # Test multiple inputs
    multi_embedding_request = EmbeddingRequest(
        input=["Text 1", "Text 2", "Text 3"],
    )
    
    print(f"✓ Created EmbeddingRequest with {len(multi_embedding_request.input)} inputs")
    
    print()
    return True


def test_provider_defaults():
    """Test default models for different providers."""
    print("=" * 60)
    print("Test 4: Provider Default Models")
    print("=" * 60)
    
    providers = [
        ProviderType.OPENAI,
        ProviderType.GOOGLE,
        ProviderType.TOGETHER,
        ProviderType.AZURE_OPENAI,
        ProviderType.ANYSCALE,
    ]
    
    for provider in providers:
        llm_model = ProviderConfig._get_default_llm_model(provider)
        embed_model = ProviderConfig._get_default_embedding_model(provider)
        
        print(f"✓ {provider.value.upper()}:")
        print(f"  - Default LLM: {llm_model}")
        print(f"  - Default Embedding: {embed_model}")
    
    print()
    return True


def test_message_serialization():
    """Test message serialization."""
    print("=" * 60)
    print("Test 5: Message Serialization")
    print("=" * 60)
    
    # Create message
    message = ChatMessage(
        role=MessageRole.USER,
        content="Test message",
        name="TestUser",
    )
    
    # Serialize to dict
    msg_dict = message.to_dict()
    print(f"✓ Serialized message to dict: {msg_dict}")
    
    # Deserialize from dict
    restored = ChatMessage.from_dict(msg_dict)
    print(f"✓ Deserialized message from dict")
    print(f"  - Role: {restored.role.value}")
    print(f"  - Content: {restored.content}")
    print(f"  - Name: {restored.name}")
    
    # Verify equality
    if (restored.role == message.role and 
        restored.content == message.content and 
        restored.name == message.name):
        print("✓ Serialization/deserialization preserved all data")
    else:
        print("✗ Data mismatch after serialization")
        return False
    
    print()
    return True


def main():
    """Run all tests."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "UNIFIED PROVIDER MANUAL TEST" + " " * 20 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    tests = [
        test_config_creation,
        test_client_creation,
        test_request_models,
        test_provider_defaults,
        test_message_serialization,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("✓ All tests passed!")
        print()
        print("Note: These tests validate the library structure and API.")
        print("To test actual API calls, set environment variables:")
        print("  export UNIFIED_API_KEY='your-api-key'")
        print("  export UNIFIED_PROVIDER='openai'")
        print("Then see src/unified_provider/examples.py for usage.")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
