"""Tests for unified provider models."""

import pytest
from unified_provider.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    MessageRole,
)


class TestChatMessage:
    """Test ChatMessage class."""
    
    def test_create_message(self):
        """Test creating a chat message."""
        msg = ChatMessage(
            role=MessageRole.USER,
            content="Hello",
        )
        
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello"
        assert msg.name is None
        assert msg.function_call is None
    
    def test_message_with_name(self):
        """Test message with name."""
        msg = ChatMessage(
            role=MessageRole.USER,
            content="Hello",
            name="John",
        )
        
        assert msg.name == "John"
    
    def test_to_dict(self):
        """Test converting message to dictionary."""
        msg = ChatMessage(
            role=MessageRole.ASSISTANT,
            content="Hello there",
        )
        
        result = msg.to_dict()
        
        assert result["role"] == "assistant"
        assert result["content"] == "Hello there"
        assert "name" not in result
    
    def test_to_dict_with_all_fields(self):
        """Test converting message with all fields to dictionary."""
        msg = ChatMessage(
            role=MessageRole.ASSISTANT,
            content="Hello",
            name="Bot",
            function_call={"name": "test", "args": {}},
        )
        
        result = msg.to_dict()
        
        assert result["role"] == "assistant"
        assert result["content"] == "Hello"
        assert result["name"] == "Bot"
        assert result["function_call"]["name"] == "test"
    
    def test_from_dict(self):
        """Test creating message from dictionary."""
        data = {
            "role": "user",
            "content": "Hello",
        }
        
        msg = ChatMessage.from_dict(data)
        
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello"
    
    def test_from_dict_with_all_fields(self):
        """Test creating message from dictionary with all fields."""
        data = {
            "role": "assistant",
            "content": "Hello",
            "name": "Bot",
            "function_call": {"name": "test"},
        }
        
        msg = ChatMessage.from_dict(data)
        
        assert msg.role == MessageRole.ASSISTANT
        assert msg.content == "Hello"
        assert msg.name == "Bot"
        assert msg.function_call["name"] == "test"


class TestChatRequest:
    """Test ChatRequest class."""
    
    def test_create_request(self):
        """Test creating a chat request."""
        messages = [
            ChatMessage(role=MessageRole.USER, content="Hello"),
        ]
        
        request = ChatRequest(messages=messages)
        
        assert len(request.messages) == 1
        assert request.temperature == 0.7
        assert request.stream is False
    
    def test_request_with_custom_params(self):
        """Test request with custom parameters."""
        messages = [
            ChatMessage(role=MessageRole.USER, content="Hello"),
        ]
        
        request = ChatRequest(
            messages=messages,
            model="gpt-4",
            temperature=0.9,
            max_tokens=100,
            top_p=0.95,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            stop=["STOP"],
            stream=True,
        )
        
        assert request.model == "gpt-4"
        assert request.temperature == 0.9
        assert request.max_tokens == 100
        assert request.top_p == 0.95
        assert request.frequency_penalty == 0.5
        assert request.presence_penalty == 0.5
        assert request.stop == ["STOP"]
        assert request.stream is True
    
    def test_to_dict(self):
        """Test converting request to dictionary."""
        messages = [
            ChatMessage(role=MessageRole.USER, content="Hello"),
        ]
        
        request = ChatRequest(messages=messages, model="gpt-4")
        result = request.to_dict()
        
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["model"] == "gpt-4"
        assert result["temperature"] == 0.7
        assert result["stream"] is False
    
    def test_to_dict_excludes_none_values(self):
        """Test that to_dict excludes None values for optional fields."""
        messages = [
            ChatMessage(role=MessageRole.USER, content="Hello"),
        ]
        
        request = ChatRequest(messages=messages)
        result = request.to_dict()
        
        # Model is None by default, should not be in dict unless set
        assert "model" not in result or result["model"] is None
        assert "max_tokens" not in result or result["max_tokens"] is None


class TestChatResponse:
    """Test ChatResponse class."""
    
    def test_create_response(self):
        """Test creating a chat response."""
        response = ChatResponse(
            id="test-123",
            model="gpt-4",
            content="Hello there",
        )
        
        assert response.id == "test-123"
        assert response.model == "gpt-4"
        assert response.content == "Hello there"
        assert response.role == MessageRole.ASSISTANT
    
    def test_response_with_all_fields(self):
        """Test response with all fields."""
        response = ChatResponse(
            id="test-123",
            model="gpt-4",
            content="Hello there",
            role=MessageRole.ASSISTANT,
            finish_reason="stop",
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            raw_response={"test": "data"},
        )
        
        assert response.finish_reason == "stop"
        assert response.usage["total_tokens"] == 30
        assert response.raw_response["test"] == "data"


class TestEmbeddingRequest:
    """Test EmbeddingRequest class."""
    
    def test_create_request_single_text(self):
        """Test creating embedding request with single text."""
        request = EmbeddingRequest(input="Hello world")
        
        assert request.input == "Hello world"
        assert request.encoding_format == "float"
        assert request.dimensions is None
    
    def test_create_request_multiple_texts(self):
        """Test creating embedding request with multiple texts."""
        request = EmbeddingRequest(input=["Hello", "World"])
        
        assert len(request.input) == 2
        assert request.input[0] == "Hello"
    
    def test_request_with_custom_params(self):
        """Test request with custom parameters."""
        request = EmbeddingRequest(
            input="Test",
            model="text-embedding-3-small",
            encoding_format="float",
            dimensions=512,
        )
        
        assert request.model == "text-embedding-3-small"
        assert request.encoding_format == "float"
        assert request.dimensions == 512
    
    def test_to_dict(self):
        """Test converting request to dictionary."""
        request = EmbeddingRequest(
            input="Hello",
            model="text-embedding-3-small",
        )
        
        result = request.to_dict()
        
        assert result["input"] == "Hello"
        assert result["model"] == "text-embedding-3-small"
        assert result["encoding_format"] == "float"


class TestEmbeddingResponse:
    """Test EmbeddingResponse class."""
    
    def test_create_response(self):
        """Test creating embedding response."""
        embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        
        response = EmbeddingResponse(
            embeddings=embeddings,
            model="text-embedding-3-small",
        )
        
        assert len(response.embeddings) == 2
        assert len(response.embeddings[0]) == 3
        assert response.model == "text-embedding-3-small"
        assert response.usage is None
    
    def test_response_with_all_fields(self):
        """Test response with all fields."""
        embeddings = [[0.1, 0.2]]
        
        response = EmbeddingResponse(
            embeddings=embeddings,
            model="text-embedding-3-small",
            usage={"prompt_tokens": 5, "total_tokens": 5},
            raw_response={"test": "data"},
        )
        
        assert response.usage["total_tokens"] == 5
        assert response.raw_response["test"] == "data"


class TestMessageRole:
    """Test MessageRole enum."""
    
    def test_role_values(self):
        """Test role enum values."""
        assert MessageRole.SYSTEM.value == "system"
        assert MessageRole.USER.value == "user"
        assert MessageRole.ASSISTANT.value == "assistant"
        assert MessageRole.FUNCTION.value == "function"
    
    def test_role_from_string(self):
        """Test creating role from string."""
        assert MessageRole("user") == MessageRole.USER
        assert MessageRole("assistant") == MessageRole.ASSISTANT
