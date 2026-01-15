"""Tests for unified provider client."""

import pytest
from unittest.mock import Mock, patch, AsyncMock

from unified_provider.client import UnifiedProviderClient
from unified_provider.config import ProviderConfig, ProviderType
from unified_provider.models import (
    ChatRequest,
    ChatMessage,
    MessageRole,
    EmbeddingRequest,
)
from unified_provider.exceptions import ConfigurationError


class TestUnifiedProviderClient:
    """Test UnifiedProviderClient class."""
    
    def test_create_client_openai(self):
        """Test creating client with OpenAI provider."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
        )
        
        client = UnifiedProviderClient(config)
        
        assert client.config == config
        assert client._provider is not None
    
    def test_create_client_azure_openai(self):
        """Test creating client with Azure OpenAI provider."""
        config = ProviderConfig(
            provider=ProviderType.AZURE_OPENAI,
            api_key="test-key",
            base_url="https://test.openai.azure.com",
        )
        
        client = UnifiedProviderClient(config)
        
        assert client.config == config
        assert client._provider is not None
    
    def test_create_client_unsupported_provider(self):
        """Test creating client with unsupported provider raises error."""
        config = ProviderConfig(
            provider=ProviderType.GOOGLE,
            api_key="test-key",
        )
        
        with pytest.raises(ConfigurationError, match="not yet implemented"):
            UnifiedProviderClient(config)
    
    def test_chat_completion_sync_delegates_to_provider(self):
        """Test that chat_completion_sync delegates to provider."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
        )
        
        client = UnifiedProviderClient(config)
        
        # Mock the provider
        mock_response = Mock()
        client._provider.chat_completion_sync = Mock(return_value=mock_response)
        
        request = ChatRequest(
            messages=[ChatMessage(role=MessageRole.USER, content="Hello")],
        )
        
        response = client.chat_completion_sync(request)
        
        assert response == mock_response
        client._provider.chat_completion_sync.assert_called_once_with(request)
    
    def test_create_embedding_sync_delegates_to_provider(self):
        """Test that create_embedding_sync delegates to provider."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
        )
        
        client = UnifiedProviderClient(config)
        
        # Mock the provider
        mock_response = Mock()
        client._provider.create_embedding_sync = Mock(return_value=mock_response)
        
        request = EmbeddingRequest(input="Hello world")
        
        response = client.create_embedding_sync(request)
        
        assert response == mock_response
        client._provider.create_embedding_sync.assert_called_once_with(request)
    
    @pytest.mark.asyncio
    async def test_chat_completion_async_delegates_to_provider(self):
        """Test that chat_completion delegates to provider."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
        )
        
        client = UnifiedProviderClient(config)
        
        # Mock the provider
        mock_response = Mock()
        client._provider.chat_completion = AsyncMock(return_value=mock_response)
        
        request = ChatRequest(
            messages=[ChatMessage(role=MessageRole.USER, content="Hello")],
        )
        
        response = await client.chat_completion(request)
        
        assert response == mock_response
        client._provider.chat_completion.assert_called_once_with(request)
    
    @pytest.mark.asyncio
    async def test_create_embedding_async_delegates_to_provider(self):
        """Test that create_embedding delegates to provider."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
        )
        
        client = UnifiedProviderClient(config)
        
        # Mock the provider
        mock_response = Mock()
        client._provider.create_embedding = AsyncMock(return_value=mock_response)
        
        request = EmbeddingRequest(input="Hello world")
        
        response = await client.create_embedding(request)
        
        assert response == mock_response
        client._provider.create_embedding.assert_called_once_with(request)
    
    @patch('unified_provider.client.ProviderConfig.from_env')
    def test_from_env(self, mock_from_env):
        """Test creating client from environment."""
        mock_config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
        )
        mock_from_env.return_value = mock_config
        
        client = UnifiedProviderClient.from_env()
        
        assert client.config == mock_config
        mock_from_env.assert_called_once()
