import pytest
import os
from unittest.mock import MagicMock, patch
from gemini_handler import GeminiHandler
from constants import MODEL_ID_GEMINI


@pytest.fixture
def mock_genai_client(monkeypatch):
    """Mock google.genai.Client class."""
    mock_client_class = MagicMock()
    monkeypatch.setattr("gemini_handler.genai.Client", mock_client_class)
    return mock_client_class


@pytest.fixture
def gemini_handler(monkeypatch):
    """Fixture to provide a GeminiHandler instance with mocked environment."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    return GeminiHandler()


def test_gemini_handler_initialization(gemini_handler):
    """Test proper initialization of GeminiHandler."""
    assert gemini_handler.api_key == "test-api-key"
    assert gemini_handler.client is None


def test_setup_creates_client(gemini_handler, mock_genai_client):
    """Test that setup() creates a genai.Client."""
    gemini_handler.setup()
    mock_genai_client.assert_called_once_with(api_key="test-api-key")
    assert gemini_handler.client is not None


def test_generate_text_calls_model(gemini_handler, mock_genai_client):
    """Test that generate_text calls access models.generate_content."""
    # Setup mocks for client instance and its methods
    mock_client_instance = mock_genai_client.return_value
    mock_response = MagicMock()
    mock_response.text = "Generated text content"
    
    mock_client_instance.models.generate_content.return_value = mock_response

    # Execute
    result = gemini_handler.generate_text("Test prompt")

    assert result == "Generated text content"
    mock_genai_client.assert_called_with(api_key="test-api-key")
    mock_client_instance.models.generate_content.assert_called_with(
        model=MODEL_ID_GEMINI, contents="Test prompt"
    )
