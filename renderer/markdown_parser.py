import markdown


class MarkdownParser:
    """
    Converts Markdown to HTML.
    """

    def parse(self, markdown_text: str) -> str:
        html = markdown.markdown(
            markdown_text, extensions=["fenced_code", "tables", "toc"]
        )

        return html
