from services.llm_service import LLMService


class AnalyzerAgent:
    def __init__(self):
        self.llm_service = LLMService()

    def analyze(self, file_data):
        """
        Analyze a single file using Gemini.

        Parameters:
            file_data (dict): Metadata and content of the file.

        Returns:
            dict: AI-generated analysis.
        """

        prompt = f"""
You are an expert software engineer and technical documentation writer.

Analyze the following source code.

File Name:
{file_data["name"]}

File Extension:
{file_data["extension"]}

Source Code:
{file_data["content"]}

Generate documentation in the following format:

Purpose:
(Explain what this file does.)

Responsibilities:
(List the main responsibilities.)

Key Components:
(List important classes, functions, or methods.)

Dependencies:
(List important libraries or modules used.)

Summary:
(Give a short overall summary.)
"""

        ai_response = self.llm_service.generate_response(prompt)

        analysis = {
            "name": file_data["name"],
            "path": file_data["path"],
            "extension": file_data["extension"],
            "documentation": ai_response,
        }

        return analysis
