from services.llm_service import LLMService


class EditorAgent:
    def __init__(self):
        print("\n[EditorAgent] Initializing EditorAgent")
        self.llm = LLMService()

    def edit(self, markdown: str, instruction: str) -> str:
        print("\n" + "=" * 80)
        print("[EditorAgent] edit() ENTERED")
        print(f"[EditorAgent] Instruction: {instruction}")
        print(f"[EditorAgent] Markdown length: {len(markdown)}")

        prompt = self.build_prompt(markdown, instruction)

        print("[EditorAgent] Prompt built")
        print("[EditorAgent] Sending request to LLM...")

        updated_markdown = self.llm.generate_response(prompt)

        print("[EditorAgent] Response received from LLM")

        if updated_markdown is None:
            print("[EditorAgent] ERROR: LLM returned None")
            return markdown

        print(f"[EditorAgent] Updated markdown length: {len(updated_markdown)}")
        print("=" * 80)

        return updated_markdown

    def build_prompt(self, markdown: str, instruction: str) -> str:
        """
        Build the editing prompt sent to Gemini.
        """

        print("[EditorAgent] Building editing prompt...")

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

        print("[EditorAgent] Prompt construction completed")

        return prompt
