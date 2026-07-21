from pathlib import Path


class MarkdownLoader:
    """
    Loads a markdown file.
    """

    def load(self, md_path: str) -> str:
        path = Path(md_path)

        if not path.exists():
            raise FileNotFoundError(f"{md_path} not found.")

        return path.read_text(encoding="utf-8")
