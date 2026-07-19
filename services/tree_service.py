from pathlib import Path


class TreeService:
    def generate_tree(self, project_path):

        tree = []

        for item in project_path.rglob("*"):
            tree.append(str(item))
        return tree
