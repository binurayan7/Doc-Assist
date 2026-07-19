from pathlib import Path


class FileService:
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

        project_path = Path(project_path)

        project = {
            "project_name": project_path.name,
            "root_path": str(project_path),
            "tree": [],
            "files": [],
        }

        for item in project_path.rglob("*"):
            project["tree"].append(str(item))

            if not item.is_file():
                continue

            if item.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            try:
                with open(item, "r", encoding="utf-8") as file:
                    project["files"].append(
                        {
                            "name": item.name,
                            "path": str(item),
                            "extension": item.suffix,
                            "content": file.read(),
                        }
                    )

            except UnicodeDecodeError:
                continue

            except Exception as e:
                print(f"Error reading {item}: {e}")

        return project
