import os
from typing import List, Dict, Set
from collections import defaultdict
from modules.parser import parse_python_file

def build_dependency_graph(files: List[str], base_dir: str) -> Dict[str, Set[str]]:
    """Builds a dependency graph based on file imports."""
    graph = defaultdict(set)
    file_to_module = {}

    # Map file paths to module names
    for filepath in files:
        relative_path = os.path.relpath(filepath, base_dir)
        module_name = os.path.splitext(relative_path)[0].replace(os.sep, '.')
        file_to_module[filepath] = module_name

    # Build the graph
    for filepath in files:
        current_module = file_to_module.get(filepath)
        if not current_module:
            continue

        imports = parse_python_file(filepath)
        for imported_module_base in imports:
            # Try to find a corresponding file for the imported module
            imported_filepath = None
            for other_filepath, other_module in file_to_module.items():
                if other_module.startswith(imported_module_base + '.') or other_module == imported_module_base:
                    # Check if the imported module is within the same package or a sibling
                    # This is a simplified check for local modules/relative imports
                    # More robust handling would involve checking __init__.py files and sys.path
                    if other_filepath.endswith('.py'):
                        imported_filepath = other_filepath
                        break # Found a potential match

            if imported_filepath:
                imported_module = file_to_module.get(imported_filepath)
                if imported_module and imported_module != current_module:
                    graph[current_module].add(imported_module)

    return dict(graph)