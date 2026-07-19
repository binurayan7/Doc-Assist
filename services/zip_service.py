from pathlib import Path
import zipfile



class ZipService:
    """
    Handles all ZIP file operations.
    """

    def __init__(self):
        self.upload_folder = Path("uploads")

        # Create uploads folder if it doesn't exist
        self.upload_folder.mkdir(exist_ok=True)

    def save_uploaded_file(self, uploaded_file):
        """
        Save the uploaded ZIP file to the uploads folder.
        """

        file_path = self.upload_folder / uploaded_file.name

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        return file_path
    
    def extract_zip(self, saved_path):

        extract_folder = Path("extracted")
        extract_folder.mkdir(exist_ok=True)

        project_folder = extract_folder / saved_path.stem
        project_folder.mkdir(exist_ok=True)

        with zipfile.ZipFile(saved_path, "r") as zip_ref:
            zip_ref.extractall(project_folder)
        contents = list(project_folder.iterdir())

        if len(contents) == 1 and contents[0].is_dir():
            return contents[0]
        
        return project_folder