import os
from google import genai
from dotenv import load_dotenv
from constants import MODEL_ID_GEMINI


class GeminiHandler:
    """
    Handle Google Gemini API connections
    """

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if not self.api_key:
            # It might be passed via CLI and set in env later, but good to warn/check
            pass

    def setup(self):
        if self.api_key and not self.client:
            self.client = genai.Client(api_key=self.api_key)

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using Gemini model
        """
        self.setup()
        if not self.client:
            raise ValueError("Gemini Client not initialized. API Key might be missing.")
        
        response = self.client.models.generate_content(
            model=MODEL_ID_GEMINI, contents=prompt
        )
        return response.text
