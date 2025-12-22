# aws_handler.py

import os
import json
import boto3
from dotenv import load_dotenv
from typing import Dict, Any

from constants import MODEL_ID_1, MODEL_ID_2, MODEL_ID_3, MODEL_ID_4
from utils import extract_text_from_bedrock_response


class AwsHandler:
    """
    Handles all AWS Bedrock Runtime interactions.
    """

    def __init__(self) -> None:
        load_dotenv()

        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        )

    # ------------------------------------------------------------------
    # Payload builders
    # ------------------------------------------------------------------

    @staticmethod
    def build_nova_payload(
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.1
    ) -> bytes:
        """
        STRICT payload for Amazon Nova Micro.
        Nova DOES NOT accept `type` nor `topP`.
        """

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ],
                }
            ],
            "inferenceConfig": {
                "maxTokens": max_tokens,
                "temperature": temperature,
            },
        }

        return json.dumps(payload).encode("utf-8")

    @staticmethod
    def build_openai_style_payload(
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.1,
        top_p: float = 0.1
    ) -> bytes:
        """
        Payload for Claude, OpenAI-style and Gemma models.
        """

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
            "inferenceConfig": {
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": top_p,
            },
        }

        return json.dumps(payload).encode("utf-8")

    # ------------------------------------------------------------------
    # Internal invoke
    # ------------------------------------------------------------------

    def _invoke_model(self, model_id: str, body: bytes) -> Dict[str, Any]:
        response = self.bedrock_client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        raw_body = response["body"].read().decode("utf-8")
        return json.loads(raw_body)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def invoke_nova_micro(self, payload: bytes) -> str:
        result = self._invoke_model(MODEL_ID_1, payload)
        return extract_text_from_bedrock_response(result)

    def invoke_openai(self, payload: bytes) -> str:
        result = self._invoke_model(MODEL_ID_2, payload)
        return extract_text_from_bedrock_response(result)

    def invoke_claude(self, payload: bytes) -> str:
        result = self._invoke_model(MODEL_ID_3, payload)
        return extract_text_from_bedrock_response(result)

    def invoke_gemma(self, payload: bytes) -> str:
        result = self._invoke_model(MODEL_ID_4, payload)
        return extract_text_from_bedrock_response(result)
