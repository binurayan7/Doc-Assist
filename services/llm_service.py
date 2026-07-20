import os

from dotenv import load_dotenv
from google import genai


class LLMService:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")

        self.client = genai.Client(api_key=api_key)

    def generate_response(self, prompt):

        try:
            response = self.client.models.generate_content(
                # model="gemini-3.5-flash",
                model="gemini-3.1-flash-lite",
                contents=prompt,
            )

            return response.text

        except Exception as e:
            return f"Error generating response: {e}"
