import os
from typing import List

def find_python_files(root_dir: str) -> List[str]:
    """Finds all Python .py files recursively, excluding specified directories."""
    python_files = []
    excluded_dirs = {'.venv', 'venv', '__pycache__', '.git', 'node_modules'}

    for root, dirs, files in os.walk(root_dir):
        # Exclude directories from traversal
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files