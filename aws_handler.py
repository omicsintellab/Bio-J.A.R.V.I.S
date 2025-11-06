# Libraries
import os
import boto3
import json
from dotenv import load_dotenv
from constants import MODEL_ID

class AwsHandler:
    """
    Handle AWS API conections with bedrock service
    """
    def __init__(self):
        load_dotenv()
        self.bedrock_client = {
            'service_name': 'bedrock-runtime',
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
            # 'aws_session_token': os.getenv('AWS_SESSION_TOKEN'),
            'region_name': os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        }

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
        """sumary_line
        Invoke the model by ID and return the response.
        """
        response_from_model = self.bedrock_client.invoke_model(
            modelId=MODEL_ID,
            body=request_body,
            contentType='application/json',
            accept='application/json'
        )
        response_body_model = response_from_model['body'].read().decode('utf-8')
        result_from_model = json.loads(response_body_model)

        try:
            return result_from_model['output']['message']['content'][0]['text']
        except:
            raise ValueError(f'Unexpected response format: {result_from_model.keys()}')
        