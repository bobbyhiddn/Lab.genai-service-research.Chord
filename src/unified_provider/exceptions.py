"""Exception classes for the unified provider."""


class ProviderError(Exception):
    """Base exception for all provider errors."""
    
    def __init__(self, message: str, provider: str = None):
        """
        Initialize provider error.
        
        Args:
            message: Error message
            provider: Name of the provider where error occurred
        """
        self.provider = provider
        super().__init__(message)


class ConfigurationError(ProviderError):
    """Configuration or initialization error."""
    pass


class APIError(ProviderError):
    """API request failed."""
    
    def __init__(self, message: str, provider: str = None, status_code: int = None, response_data: dict = None):
        """
        Initialize API error.
        
        Args:
            message: Error message
            provider: Name of the provider
            status_code: HTTP status code if available
            response_data: Response data from the API if available
        """
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message, provider)


class RateLimitError(APIError):
    """Rate limit exceeded."""
    
    def __init__(self, message: str, provider: str = None, retry_after: int = None):
        """
        Initialize rate limit error.
        
        Args:
            message: Error message
            provider: Name of the provider
            retry_after: Seconds to wait before retrying
        """
        self.retry_after = retry_after
        super().__init__(message, provider, status_code=429)


class AuthenticationError(APIError):
    """Authentication failed."""
    
    def __init__(self, message: str, provider: str = None):
        """
        Initialize authentication error.
        
        Args:
            message: Error message
            provider: Name of the provider
        """
        super().__init__(message, provider, status_code=401)


class ModelNotFoundError(ProviderError):
    """Requested model not available."""
    pass


class ValidationError(ProviderError):
    """Request validation failed."""
    pass
