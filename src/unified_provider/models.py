"""Data models for requests and responses."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Literal, Union
from enum import Enum


class MessageRole(Enum):
    """Message role in a conversation."""
    
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


@dataclass
class ChatMessage:
    """
    A message in a chat conversation.
    
    Attributes:
        role: The role of the message sender
        content: The content of the message
        name: Optional name of the sender
        function_call: Optional function call data
    """
    
    role: MessageRole
    content: str
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        result = {
            "role": self.role.value,
            "content": self.content,
        }
        if self.name:
            result["name"] = self.name
        if self.function_call:
            result["function_call"] = self.function_call
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatMessage":
        """Create from dictionary."""
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            name=data.get("name"),
            function_call=data.get("function_call"),
        )


@dataclass
class ChatRequest:
    """
    Request for chat completion.
    
    Attributes:
        messages: List of messages in the conversation
        model: Model to use for completion
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        frequency_penalty: Frequency penalty (-2.0 to 2.0)
        presence_penalty: Presence penalty (-2.0 to 2.0)
        stop: Optional stop sequences
        stream: Whether to stream the response
        additional_params: Additional provider-specific parameters
    """
    
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[List[str]] = None
    stream: bool = False
    additional_params: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        result = {
            "messages": [msg.to_dict() for msg in self.messages],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "stream": self.stream,
        }
        
        if self.model:
            result["model"] = self.model
        if self.max_tokens:
            result["max_tokens"] = self.max_tokens
        if self.stop:
            result["stop"] = self.stop
        
        # Add any additional parameters
        result.update(self.additional_params)
        
        return result


@dataclass
class ChatResponse:
    """
    Response from chat completion.
    
    Attributes:
        id: Unique identifier for the response
        model: Model used for completion
        content: The generated content
        role: Role of the response (typically 'assistant')
        finish_reason: Reason for completion (e.g., 'stop', 'length')
        usage: Token usage information
        raw_response: Raw response data from provider
    """
    
    id: str
    model: str
    content: str
    role: MessageRole = MessageRole.ASSISTANT
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingRequest:
    """
    Request for text embedding.
    
    Attributes:
        input: Text or list of texts to embed
        model: Model to use for embedding
        encoding_format: Format for the embedding (float or base64)
        dimensions: Optional dimension override for models that support it
        additional_params: Additional provider-specific parameters
    """
    
    input: Union[List[str], str]
    model: Optional[str] = None
    encoding_format: Literal["float", "base64"] = "float"
    dimensions: Optional[int] = None
    additional_params: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        result = {
            "input": self.input,
            "encoding_format": self.encoding_format,
        }
        
        if self.model:
            result["model"] = self.model
        if self.dimensions:
            result["dimensions"] = self.dimensions
        
        # Add any additional parameters
        result.update(self.additional_params)
        
        return result


@dataclass
class EmbeddingResponse:
    """
    Response from embedding request.
    
    Attributes:
        embeddings: List of embedding vectors
        model: Model used for embedding
        usage: Token usage information
        raw_response: Raw response data from provider
    """
    
    embeddings: List[List[float]]
    model: str
    usage: Optional[Dict[str, int]] = None
    raw_response: Optional[Dict[str, Any]] = None
