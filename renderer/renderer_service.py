from pathlib import Path

from renderer.markdown_loader import MarkdownLoader
from renderer.markdown_parser import MarkdownParser
from renderer.html_builder import HTMLBuilder
from renderer.pdf_generator import PDFGenerator


class RendererService:
    """
    Orchestrates the complete rendering pipeline.

    Markdown
        ↓
    HTML
        ↓
    PDF
    """

    def __init__(self):
        self.loader = MarkdownLoader()
        self.parser = MarkdownParser()
        self.builder = HTMLBuilder()
        self.pdf_generator = PDFGenerator()

    def render(self, markdown_path: str):

        # -------------------------
        # Load Markdown
        # -------------------------
        markdown_text = self.loader.load(markdown_path)

        # -------------------------
        # Markdown → HTML Body
        # -------------------------
        html_body = self.parser.parse(markdown_text)

        # -------------------------
        # Build Complete HTML
        # -------------------------
        html = self.builder.build(html_body)

        # -------------------------
        # Output Paths
        # -------------------------
        md_file = Path(markdown_path)

        html_path = md_file.with_suffix(".html")
        pdf_path = md_file.with_suffix(".pdf")

        # -------------------------
        # Save HTML
        # -------------------------
        html_path.write_text(html, encoding="utf-8")

        # -------------------------
        # Generate PDF
        # -------------------------
        self.pdf_generator.generate(html, str(pdf_path))

        return str(html_path), str(pdf_path)
