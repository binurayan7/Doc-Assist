from pathlib import Path


class FileService:
    # File types we want to read
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

    def read_file(self, file_path):

        file_path = Path(file_path)
        # Skip unsupported files
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return {
                    "name": file_path.name,
                    "path": str(file_path),
                    "extension": file_path.suffix,
                    "content": file.read(),
                }

        except UnicodeDecodeError:
            return None

        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
