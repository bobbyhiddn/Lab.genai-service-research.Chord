"""Tests for exception classes."""

import pytest
from unified_provider.exceptions import (
    ProviderError,
    ConfigurationError,
    APIError,
    RateLimitError,
    AuthenticationError,
    ModelNotFoundError,
    ValidationError,
)


class TestProviderError:
    """Test ProviderError base class."""
    
    def test_create_provider_error(self):
        """Test creating provider error."""
        error = ProviderError("Test error")
        
        assert str(error) == "Test error"
        assert error.provider is None
    
    def test_create_provider_error_with_provider(self):
        """Test creating provider error with provider name."""
        error = ProviderError("Test error", provider="openai")
        
        assert str(error) == "Test error"
        assert error.provider == "openai"
    
    def test_provider_error_is_exception(self):
        """Test that ProviderError is an Exception."""
        error = ProviderError("Test error")
        
        assert isinstance(error, Exception)


class TestConfigurationError:
    """Test ConfigurationError."""
    
    def test_create_configuration_error(self):
        """Test creating configuration error."""
        error = ConfigurationError("Config error")
        
        assert str(error) == "Config error"
        assert isinstance(error, ProviderError)


class TestAPIError:
    """Test APIError."""
    
    def test_create_api_error(self):
        """Test creating API error."""
        error = APIError("API failed")
        
        assert str(error) == "API failed"
        assert error.status_code is None
        assert error.response_data is None
    
    def test_create_api_error_with_details(self):
        """Test creating API error with details."""
        error = APIError(
            "API failed",
            provider="openai",
            status_code=500,
            response_data={"error": "Internal error"},
        )
        
        assert error.provider == "openai"
        assert error.status_code == 500
        assert error.response_data["error"] == "Internal error"
    
    def test_api_error_is_provider_error(self):
        """Test that APIError is a ProviderError."""
        error = APIError("API failed")
        
        assert isinstance(error, ProviderError)


class TestRateLimitError:
    """Test RateLimitError."""
    
    def test_create_rate_limit_error(self):
        """Test creating rate limit error."""
        error = RateLimitError("Rate limited")
        
        assert str(error) == "Rate limited"
        assert error.status_code == 429
        assert error.retry_after is None
    
    def test_create_rate_limit_error_with_retry(self):
        """Test creating rate limit error with retry_after."""
        error = RateLimitError(
            "Rate limited",
            provider="openai",
            retry_after=60,
        )
        
        assert error.provider == "openai"
        assert error.retry_after == 60
        assert error.status_code == 429
    
    def test_rate_limit_error_is_api_error(self):
        """Test that RateLimitError is an APIError."""
        error = RateLimitError("Rate limited")
        
        assert isinstance(error, APIError)
        assert isinstance(error, ProviderError)


class TestAuthenticationError:
    """Test AuthenticationError."""
    
    def test_create_authentication_error(self):
        """Test creating authentication error."""
        error = AuthenticationError("Auth failed")
        
        assert str(error) == "Auth failed"
        assert error.status_code == 401
    
    def test_create_authentication_error_with_provider(self):
        """Test creating authentication error with provider."""
        error = AuthenticationError("Auth failed", provider="openai")
        
        assert error.provider == "openai"
        assert error.status_code == 401
    
    def test_authentication_error_is_api_error(self):
        """Test that AuthenticationError is an APIError."""
        error = AuthenticationError("Auth failed")
        
        assert isinstance(error, APIError)
        assert isinstance(error, ProviderError)


class TestModelNotFoundError:
    """Test ModelNotFoundError."""
    
    def test_create_model_not_found_error(self):
        """Test creating model not found error."""
        error = ModelNotFoundError("Model not found")
        
        assert str(error) == "Model not found"
        assert isinstance(error, ProviderError)


class TestValidationError:
    """Test ValidationError."""
    
    def test_create_validation_error(self):
        """Test creating validation error."""
        error = ValidationError("Validation failed")
        
        assert str(error) == "Validation failed"
        assert isinstance(error, ProviderError)


class TestExceptionHierarchy:
    """Test exception hierarchy."""
    
    def test_all_inherit_from_provider_error(self):
        """Test that all exceptions inherit from ProviderError."""
        errors = [
            ConfigurationError("test"),
            APIError("test"),
            RateLimitError("test"),
            AuthenticationError("test"),
            ModelNotFoundError("test"),
            ValidationError("test"),
        ]
        
        for error in errors:
            assert isinstance(error, ProviderError)
            assert isinstance(error, Exception)
    
    def test_api_error_hierarchy(self):
        """Test API error hierarchy."""
        rate_limit = RateLimitError("test")
        auth_error = AuthenticationError("test")
        
        assert isinstance(rate_limit, APIError)
        assert isinstance(auth_error, APIError)
        assert isinstance(rate_limit, ProviderError)
        assert isinstance(auth_error, ProviderError)
