from services.llm_service import LLMService


class EditorAgent:
    def __init__(self):
        self.llm = LLMService()

    def edit(self, markdown: str, instruction: str) -> str:
        """
        Edit an existing Markdown document based on a natural language instruction.
        """

        prompt = self.build_prompt(markdown, instruction)

        updated_markdown = self.llm.generate_response(prompt)

        return updated_markdown

    def build_prompt(self, markdown: str, instruction: str) -> str:
        """
        Build the editing prompt sent to Gemini.
        """

        prompt = f"""
You are an expert technical documentation editor.

You will receive:

1. An existing Markdown document.
2. A user editing instruction.

Your task is to edit ONLY what the user requests.

Rules:

- Preserve the Markdown formatting.
- Do NOT remove unrelated sections.
- Do NOT rewrite the whole document unless requested.
- Keep headings, tables and code blocks valid.
- Return ONLY the updated Markdown.
- Do NOT explain your changes.
- Do NOT wrap the response in markdown fences.

==============================
CURRENT DOCUMENT
==============================

{markdown}

==============================
USER REQUEST
==============================

{instruction}
"""

        return prompt
