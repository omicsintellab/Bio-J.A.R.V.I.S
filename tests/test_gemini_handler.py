import pytest
import os
from unittest.mock import MagicMock
from gemini_handler import GeminiHandler
from constants import MODEL_ID_GEMINI


@pytest.fixture
def mock_genai(monkeypatch):
    """Mock google.generativeai module."""
    mock_module = MagicMock()
    monkeypatch.setattr("gemini_handler.genai", mock_module)
    return mock_module


@pytest.fixture
def gemini_handler(monkeypatch):
    """Fixture to provide a GeminiHandler instance with mocked environment."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    return GeminiHandler()


def test_gemini_handler_initialization(gemini_handler):
    """Test proper initialization of GeminiHandler."""
    assert gemini_handler.api_key == "test-api-key"


def test_setup_configures_genai(gemini_handler, mock_genai):
    """Test that setup() configures genai with API key."""
    gemini_handler.setup()
    mock_genai.configure.assert_called_once_with(api_key="test-api-key")


def test_generate_text_calls_model(gemini_handler, mock_genai):
    """Test that generate_text creates a model and generates content."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Generated text content"

    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model

    result = gemini_handler.generate_text("Test prompt")

    assert result == "Generated text content"
    mock_genai.configure.assert_called_with(api_key="test-api-key")
    mock_genai.GenerativeModel.assert_called_with(MODEL_ID_GEMINI)
    mock_model.generate_content.assert_called_with("Test prompt")
