import os
import google.generativeai as genai
from dotenv import load_dotenv
from constants import MODEL_ID_GEMINI

class GeminiHandler:
    """
    Handle Google Gemini API connections
    """
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
             # It might be passed via CLI and set in env later, but good to warn/check
             pass

    def setup(self):
         if self.api_key:
            genai.configure(api_key=self.api_key)

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using Gemini model
        """
        self.setup()
        model = genai.GenerativeModel(MODEL_ID_GEMINI)
        response = model.generate_content(prompt)
        return response.text
