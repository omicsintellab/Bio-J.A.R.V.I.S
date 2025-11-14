# Libraries
import os
import boto3
import json
from dotenv import load_dotenv
from constants import MODEL_ID_1

class AwsHandler:
    """
    Handle AWS API conections with bedrock service
    """
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("BEDROCK_API_KEY")
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        #Verify if API KEY environment virable is defined
        if api_key is None:
            raise RuntimeError("The environment variable BEDROCK_API_KEY is not defined")

        #Set API KEY as Token
        os.environ["AWS_BEARER_TOKEN_BEDROCK"] = api_key

        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )

    def get_bedrock_prompt_response(prompt_text):
        """
        Get prompt and return it enconded in utf-8
        """
        return json.dumps(
            {
                'messages': [
                    {'role': 'user', 'content': [{'text': prompt_text}]}
                ],
                'inferenceConfig': {
                    'maxTokens': 300,
                    'temperature': 0.1,
                    'topP': 0.1
                }
            }
        ).encode('utf-8')

    def return_bedrock_response(self, request_body):
        """
        Invoke the model by ID and return the response.
        """
        response_from_model = self.bedrock_client.invoke_model(
            modelId = MODEL_ID_1,
            body = request_body,
            contentType = 'application/json',
            accept = 'application/json'
        )
        response_body_model = response_from_model['body'].read().decode('utf-8')
        result_from_model = json.loads(response_body_model)

        try:
            return result_from_model['output']['message']['content'][0]['text']
        except:
            raise ValueError(f'Unexpected response format: {result_from_model.keys()}')
        
