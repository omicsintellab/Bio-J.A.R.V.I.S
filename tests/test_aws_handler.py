import json
import pytest

from aws_handler import AwsHandler
from constants import MODEL_ID_1


class _DummyStream:
    """Simple stream-like object that mimics botocore responses."""

    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self) -> bytes:
        return self._payload


class _DummyClient:
    """Collects the invocation payload and returns canned responses."""

    def __init__(self, response_payload: bytes):
        self.response_payload = response_payload
        self.invocation_kwargs = None

    def invoke_model(self, **kwargs):
        self.invocation_kwargs = kwargs
        return {"body": _DummyStream(self.response_payload)}


@pytest.fixture(autouse=True)
def _aws_env(monkeypatch):
    """Ensure the handler sees deterministic environment variables."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test-key")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test-secret")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "test-token")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")


def test_get_bedrock_prompt_response_serializes_prompt():
    prompt_text = "Example prompt body"

    result = AwsHandler.get_bedrock_prompt_response(prompt_text)

    assert isinstance(result, bytes)
    payload = json.loads(result.decode("utf-8"))
    assert payload["messages"][0]["content"][0]["text"] == prompt_text


def test_return_bedrock_response_parses_model_output(monkeypatch):
    model_text = "Clinical summary text"
    response_body = json.dumps(
        {
            "output": {
                "message": {
                    "content": [
                        {"text": model_text},
                    ]
                }
            }
        }
    ).encode("utf-8")
    dummy_client = _DummyClient(response_body)
    monkeypatch.setattr("aws_handler.boto3.client", lambda *_, **__: dummy_client)
    handler = AwsHandler()

    result = handler.return_bedrock_response(b"{}")

    assert result == model_text
    assert dummy_client.invocation_kwargs["modelId"] == MODEL_ID_1
    assert dummy_client.invocation_kwargs["contentType"] == "application/json"


def test_return_bedrock_response_raises_on_unknown_format(monkeypatch):
    response_body = json.dumps({"output": {}}).encode("utf-8")
    dummy_client = _DummyClient(response_body)
    monkeypatch.setattr("aws_handler.boto3.client", lambda *_, **__: dummy_client)
    handler = AwsHandler()

    with pytest.raises(ValueError):
        handler.return_bedrock_response(b"{}")
