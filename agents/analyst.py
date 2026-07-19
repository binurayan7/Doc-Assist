class AnalyzerAgent:
    def analyze(self, file_data):
        """
        Analyze a single file.

        Parameters:
            file_data (dict): Metadata and content of the file.

        Returns:
            dict: Analysis result.
        """

        analysis = {
            "name": file_data["name"],
            "path": file_data["path"],
            "extension": file_data["extension"],
            "lines": len(file_data["content"].splitlines()),
            "characters": len(file_data["content"]),
            "summary": f"{file_data['name']} contains {len(file_data['content'].splitlines())} lines of code.",
        }

        return analysis
