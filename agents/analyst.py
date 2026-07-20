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
        # ROLE

        You are a Senior Software Architect and Technical Documentation Expert.

        Your responsibility is to analyze an entire software project and produce an accurate, structured overview of the project.

        You should reason using the complete project structure and source code before producing your final answer.

        ---

        # OBJECTIVE

        Analyze the supplied project and identify:

        - The overall purpose of the application.
        - A concise project summary.
        - The software architecture.
        - Technologies and frameworks used.
        - Main application entry points.
        - Important modules.
        - Key components and their responsibilities.

        Only include information that can be inferred from the provided source code.

        Do not invent functionality.

        ---

        # PROJECT INFORMATION

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

        ---

        # OUTPUT REQUIREMENTS

        Return ONLY valid JSON.

        The response MUST exactly match this schema:

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

        Rules:

        - Return valid JSON only.
        - Do not use Markdown.
        - Do not wrap the JSON inside code blocks.
        - Do not include explanations.
        - Do not include comments.
        - If information cannot be determined, use an empty string ("") or an empty array ([]).
        """

        return prompt
