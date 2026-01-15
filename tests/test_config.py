"""Tests for unified provider configuration."""

import os
import pytest
from unittest.mock import patch

from unified_provider.config import ProviderConfig, ProviderType
from unified_provider.exceptions import ConfigurationError


class TestProviderConfig:
    """Test ProviderConfig class."""
    
    def test_create_config(self):
        """Test creating configuration."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
        )
        
        assert config.provider == ProviderType.OPENAI
        assert config.api_key == "test-key"
        assert config.timeout == 60
        assert config.max_retries == 3
    
    def test_config_with_custom_values(self):
        """Test configuration with custom values."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
            base_url="https://custom.api.com",
            default_llm_model="custom-llm",
            default_embedding_model="custom-embed",
            timeout=120,
            max_retries=5,
        )
        
        assert config.base_url == "https://custom.api.com"
        assert config.default_llm_model == "custom-llm"
        assert config.default_embedding_model == "custom-embed"
        assert config.timeout == 120
        assert config.max_retries == 5
    
    def test_validate_success(self):
        """Test validation succeeds with valid config."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
        )
        
        # Should not raise
        config.validate()
    
    def test_validate_missing_api_key(self):
        """Test validation fails with missing API key."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="",
        )
        
        with pytest.raises(ValueError, match="API key is required"):
            config.validate()
    
    def test_validate_invalid_timeout(self):
        """Test validation fails with invalid timeout."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
            timeout=-1,
        )
        
        with pytest.raises(ValueError, match="Timeout must be positive"):
            config.validate()
    
    def test_validate_invalid_max_retries(self):
        """Test validation fails with invalid max retries."""
        config = ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
            max_retries=-1,
        )
        
        with pytest.raises(ValueError, match="Max retries cannot be negative"):
            config.validate()
    
    @patch.dict(os.environ, {
        "UNIFIED_API_KEY": "env-test-key",
        "UNIFIED_PROVIDER": "openai",
    })
    def test_from_env_basic(self):
        """Test creating config from environment variables."""
        config = ProviderConfig.from_env()
        
        assert config.provider == ProviderType.OPENAI
        assert config.api_key == "env-test-key"
    
    @patch.dict(os.environ, {
        "UNIFIED_API_KEY": "env-test-key",
        "UNIFIED_PROVIDER": "google",
        "UNIFIED_LLM_MODEL": "custom-llm",
        "UNIFIED_EMBEDDING_MODEL": "custom-embed",
        "UNIFIED_BASE_URL": "https://custom.api.com",
        "UNIFIED_TIMEOUT": "120",
        "UNIFIED_MAX_RETRIES": "5",
    })
    def test_from_env_with_custom_values(self):
        """Test creating config from environment with custom values."""
        config = ProviderConfig.from_env()
        
        assert config.provider == ProviderType.GOOGLE
        assert config.api_key == "env-test-key"
        assert config.default_llm_model == "custom-llm"
        assert config.default_embedding_model == "custom-embed"
        assert config.base_url == "https://custom.api.com"
        assert config.timeout == 120
        assert config.max_retries == 5
    
    @patch.dict(os.environ, {}, clear=True)
    def test_from_env_missing_api_key(self):
        """Test from_env fails with missing API key."""
        with pytest.raises(ValueError, match="Environment variable UNIFIED_API_KEY not set"):
            ProviderConfig.from_env()
    
    @patch.dict(os.environ, {
        "UNIFIED_API_KEY": "test-key",
        "UNIFIED_PROVIDER": "invalid-provider",
    })
    def test_from_env_invalid_provider(self):
        """Test from_env fails with invalid provider."""
        with pytest.raises(ValueError, match="Invalid provider type"):
            ProviderConfig.from_env()
    
    def test_default_llm_models(self):
        """Test default LLM models for each provider."""
        assert ProviderConfig._get_default_llm_model(ProviderType.OPENAI) == "gpt-4-turbo-preview"
        assert ProviderConfig._get_default_llm_model(ProviderType.GOOGLE) == "gemini-pro"
        assert "Mixtral" in ProviderConfig._get_default_llm_model(ProviderType.TOGETHER)
        assert ProviderConfig._get_default_llm_model(ProviderType.AZURE_OPENAI) == "gpt-4"
    
    def test_default_embedding_models(self):
        """Test default embedding models for each provider."""
        assert "text-embedding" in ProviderConfig._get_default_embedding_model(ProviderType.OPENAI)
        assert "text-embedding" in ProviderConfig._get_default_embedding_model(ProviderType.GOOGLE)
        assert ProviderConfig._get_default_embedding_model(ProviderType.TOGETHER) is not None
        assert "text-embedding" in ProviderConfig._get_default_embedding_model(ProviderType.AZURE_OPENAI)


class TestProviderType:
    """Test ProviderType enum."""
    
    def test_provider_types_exist(self):
        """Test all expected provider types exist."""
        assert ProviderType.OPENAI.value == "openai"
        assert ProviderType.GOOGLE.value == "google"
        assert ProviderType.TOGETHER.value == "together"
        assert ProviderType.AZURE_OPENAI.value == "azure_openai"
        assert ProviderType.ANYSCALE.value == "anyscale"
    
    def test_provider_type_from_string(self):
        """Test creating provider type from string."""
        assert ProviderType("openai") == ProviderType.OPENAI
        assert ProviderType("google") == ProviderType.GOOGLE
        assert ProviderType("together") == ProviderType.TOGETHER
