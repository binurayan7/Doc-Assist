from services.llm_service import LLMService
from pathlib import Path


class WriterAgent:
    """
    Generates documentation based on the project
    analysis and documentation plan.
    """

    def __init__(self):
        self.llm = LLMService()

    def write(self, analysis, plan):
        """
        Generate project documentation.

        Parameters:
            analysis (dict): Output from AnalyzerAgent.
            plan (dict): Output from PlannerAgent.

        Returns:
            str: Markdown documentation.
        """

        prompt = self.build_prompt(analysis, plan)

        documentation = self.llm.generate_response(prompt)

        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # Save markdown
        markdown_path = output_dir / "documentation.md"

        markdown_path.write_text(documentation, encoding="utf-8")

        return {"content": documentation, "path": str(markdown_path)}

    def build_prompt(self, analysis, plan):
        """
        Build the prompt for the Writer Agent.
        """

        return f"""
You are an expert technical documentation writer.

Your task is to write professional software documentation.

Use the project analysis and documentation plan below.

Project Analysis:

{analysis}

Documentation Plan:

{plan}

Write complete documentation in Markdown.

Requirements:

- Follow the documentation plan exactly.
- Use proper Markdown headings.
- Explain each section clearly.
- Use professional language.
- Do not invent information.
- Base everything on the supplied analysis.
- Return only the Markdown document.
"""
