import json

from services.llm_service import LLMService


class PlannerAgent:
    """
    Creates a documentation plan based on the
    project analysis.
    """

    def __init__(self):
        self.llm = LLMService()

    def plan(self, analysis):
        """
        Generate a documentation plan.

        Parameters:
            analysis (dict): Output from AnalyzerAgent.

        Returns:
            dict: Documentation plan.
        """

        prompt = self.build_prompt(analysis)

        response = self.llm.generate_response(prompt)

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return {
                "error": "Gemini did not return valid JSON.",
                "raw_response": response,
            }

    def build_prompt(self, analysis):
        """
        Build the prompt for the Planner Agent.
        """

        prompt = f"""
You are an expert technical documentation architect.

You are given the analysis of a software project.

Based on the analysis, create a documentation plan.

Return ONLY valid JSON.

Project Analysis:

{json.dumps(analysis, indent=4)}

Return ONLY JSON in the following format:

{{
    "document_type": "",
    "target_audience": "",
    "sections": [
        {{
            "title": "",
            "description": ""
        }}
    ]
}}

Do not include markdown.

Do not explain your answer.

Return only JSON.
"""

        return prompt
