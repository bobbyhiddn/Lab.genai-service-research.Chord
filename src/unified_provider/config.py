"""Configuration for unified provider."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any
import os


class ProviderType(Enum):
    """Supported provider types."""
    
    OPENAI = "openai"
    GOOGLE = "google"
    TOGETHER = "together"
    AZURE_OPENAI = "azure_openai"
    ANYSCALE = "anyscale"


@dataclass
class ProviderConfig:
    """
    Configuration for unified provider client.
    
    Attributes:
        provider: The provider type to use
        api_key: API key for authentication
        base_url: Optional custom base URL for API
        default_llm_model: Default model for LLM/chat requests
        default_embedding_model: Default model for embedding requests
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        additional_params: Additional provider-specific parameters
    """
    
    provider: ProviderType
    api_key: str
    base_url: Optional[str] = None
    default_llm_model: Optional[str] = None
    default_embedding_model: Optional[str] = None
    timeout: int = 60
    max_retries: int = 3
    additional_params: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_env(
        cls,
        provider: Optional[ProviderType] = None,
        env_api_key: str = "UNIFIED_API_KEY",
        env_provider: str = "UNIFIED_PROVIDER",
    ) -> "ProviderConfig":
        """
        Create configuration from environment variables.
        
        Args:
            provider: Optional provider type override
            env_api_key: Environment variable name for API key
            env_provider: Environment variable name for provider type
            
        Returns:
            ProviderConfig instance
            
        Raises:
            ValueError: If required environment variables are missing
        """
        # Get API key
        api_key = os.getenv(env_api_key)
        if not api_key:
            raise ValueError(f"Environment variable {env_api_key} not set")
        
        # Get provider type
        if provider is None:
            provider_str = os.getenv(env_provider, "openai")
            try:
                provider = ProviderType(provider_str.lower())
            except ValueError:
                raise ValueError(f"Invalid provider type: {provider_str}")
        
        # Set default models based on provider
        default_llm = os.getenv("UNIFIED_LLM_MODEL")
        default_embedding = os.getenv("UNIFIED_EMBEDDING_MODEL")
        
        if not default_llm:
            default_llm = cls._get_default_llm_model(provider)
        if not default_embedding:
            default_embedding = cls._get_default_embedding_model(provider)
        
        # Get optional settings
        base_url = os.getenv("UNIFIED_BASE_URL")
        timeout = int(os.getenv("UNIFIED_TIMEOUT", "60"))
        max_retries = int(os.getenv("UNIFIED_MAX_RETRIES", "3"))
        
        return cls(
            provider=provider,
            api_key=api_key,
            base_url=base_url,
            default_llm_model=default_llm,
            default_embedding_model=default_embedding,
            timeout=timeout,
            max_retries=max_retries,
        )
    
    @staticmethod
    def _get_default_llm_model(provider: ProviderType) -> str:
        """Get default LLM model for provider."""
        defaults = {
            ProviderType.OPENAI: "gpt-4-turbo-preview",
            ProviderType.GOOGLE: "gemini-pro",
            ProviderType.TOGETHER: "mistralai/Mixtral-8x7B-Instruct-v0.1",
            ProviderType.AZURE_OPENAI: "gpt-4",
            ProviderType.ANYSCALE: "mistralai/Mixtral-8x7B-Instruct-v0.1",
        }
        return defaults.get(provider, "gpt-4-turbo-preview")
    
    @staticmethod
    def _get_default_embedding_model(provider: ProviderType) -> str:
        """Get default embedding model for provider."""
        defaults = {
            ProviderType.OPENAI: "text-embedding-3-small",
            ProviderType.GOOGLE: "text-embedding-004",
            ProviderType.TOGETHER: "togethercomputer/m2-bert-80M-8k-retrieval",
            ProviderType.AZURE_OPENAI: "text-embedding-3-small",
            ProviderType.ANYSCALE: "thenlper/gte-large",
        }
        return defaults.get(provider, "text-embedding-3-small")
    
    def validate(self) -> None:
        """
        Validate configuration.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.api_key:
            raise ValueError("API key is required")
        
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        
        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
