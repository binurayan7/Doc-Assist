import json

from services.llm_service import LLMService


class AnalyzerAgent:
    """
    Analyzes the entire project and returns a structured
    understanding of the project.
    """

    def __init__(self):
        self.llm = LLMService()

    def analyze(self, project):
        """
        Analyze the project using Gemini.

        Parameters:
            project (dict): Project object from FileService.

        Returns:
            dict: Structured project analysis.
        """

        prompt = self.build_prompt(project)

        response = self.llm.generate_response(prompt)

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return {
                "error": "Gemini did not return valid JSON.",
                "raw_response": response,
            }

    def build_prompt(self, project):
        """
        Build the prompt sent to Gemini.
        """

        prompt = f"""
You are an expert software architect.

Analyze the following software project.

Return ONLY valid JSON.

Project Name:
{project["project_name"]}

Project Structure:
{chr(10).join(project["tree"])}

Source Files:

"""

        for file in project["files"]:
            prompt += f"""

==================================================
File: {file["path"]}
==================================================

{file["content"]}

"""

        prompt += """

Return ONLY JSON in this format:

{
    "project_name": "",
    "purpose": "",
    "summary": "",
    "architecture": "",
    "technologies": [],
    "entry_points": [],
    "modules": [],
    "key_components": []
}

Do not include markdown.
Do not explain your answer.
Return only JSON.
"""

        return prompt
