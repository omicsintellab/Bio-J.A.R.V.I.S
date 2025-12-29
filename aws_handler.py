# Libraries
import os
import json
import boto3
from dotenv import load_dotenv

from constants import MODEL_ID_1


class AwsHandler:
    """
    Handle AWS API connections with Bedrock service
    """

    def __init__(self):
        # Load environment variables from .env
        load_dotenv()

        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        # IMPORTANT:
        # AWS_BEARER_TOKEN_BEDROCK is automatically picked up by the SDK
        # It should NOT be passed as aws_session_token
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region
        )

    @staticmethod
    def get_bedrock_prompt_response(prompt_text: str) -> bytes:
        """
        Build Bedrock request body and return it encoded as UTF-8
        """
        return json.dumps(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt_text}]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": 300,
                    "temperature": 0.1,
                    "topP": 0.1
                }
            }
        ).encode("utf-8")

    def return_bedrock_response(self, request_body: bytes) -> str:
        """
        Invoke the Bedrock model and return the generated text
        """
        response = self.bedrock_client.invoke_model(
            modelId=MODEL_ID_1,
            body=request_body,
            contentType="application/json",
            accept="application/json"
        )

        response_body = response["body"].read().decode("utf-8")
        result = json.loads(response_body)

        try:
            return result["output"]["message"]["content"][0]["text"]
        except KeyError:
            raise ValueError(
                f"Unexpected Bedrock response format. Keys: {result.keys()}"
            )