from pathlib import Path


class FileService:
    """
    Reads an entire project and returns a structured
    project object for the AI agents.
    """

    SUPPORTED_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".html",
        ".css",
        ".scss",
        ".json",
        ".xml",
        ".md",
        ".txt",
        ".yml",
        ".yaml",
        ".sql",
        ".sh",
    }

    def load_project(self, project_path):
        """
        Read all supported source files from the project.

        Parameters:
            project_path (Path | str): Root directory of the extracted project.

        Returns:
            dict: Complete project information.
        """

        project_path = Path(project_path)

        project = {
            "project_name": project_path.name,
            "root_path": str(project_path),
            "tree": [],
            "files": [],
            "stats": {
                "total_items": 0,
                "supported_files": 0,
                "ignored_files": 0,
            },
        }

        for item in project_path.rglob("*"):
            project["stats"]["total_items"] += 1

            # Store relative path
            relative_path = item.relative_to(project_path)

            project["tree"].append(str(relative_path))

            if not item.is_file():
                continue

            # Skip unsupported files
            if item.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                project["stats"]["ignored_files"] += 1
                continue

            try:
                with open(item, "r", encoding="utf-8") as file:
                    project["files"].append(
                        {
                            "name": item.name,
                            "path": str(relative_path),
                            "extension": item.suffix.lower(),
                            "content": file.read(),
                        }
                    )

                    project["stats"]["supported_files"] += 1

            except UnicodeDecodeError:
                project["stats"]["ignored_files"] += 1

            except Exception as e:
                print(f"Error reading {item}: {e}")

                project["stats"]["ignored_files"] += 1

        return project
