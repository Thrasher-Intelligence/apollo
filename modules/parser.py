import ast
import sys
from typing import Set

def parse_python_file(filepath: str) -> Set[str]:
    """Parses a Python file to extract imported modules."""
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    except Exception as e:
        print(f"Warning: Could not parse file {filepath}: {e}", file=sys.stderr)
    return imports