from pathlib import Path


class HTMLBuilder:
    def build(self, body: str):

        css_path = Path(__file__).parent / "styles.css"

        css = css_path.read_text(encoding="utf-8")

        html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<style>

{css}

</style>

</head>

<body>

{body}

</body>

</html>
"""

        return html
