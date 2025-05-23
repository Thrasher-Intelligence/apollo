import sys
import argparse

from modules.graph_builder import build_dependency_graph
from modules.renderer import render_ascii_graph, render_blessed_graph
from modules.file_finder import find_python_files
from modules.path_handler import normalize_path, validate_directory, get_system_info
from modules.directory_selector import select_directory
from modules.version import get_version, print_version_info

def main():
    parser = argparse.ArgumentParser(description="Analyze Python project dependencies.")
    parser.add_argument('directory', nargs='?', default=None, help="The directory to analyze (default: interactive selection). Supports tilde (~) for home directory.")
    parser.add_argument('--view', choices=['ascii', 'blessed'], default='ascii',
                        help="Rendering method (ascii or blessed, default: ascii).")
    parser.add_argument('--interactive', '-i', action='store_true', help="Use interactive directory selection regardless of whether a directory is provided.")
    parser.add_argument('--version', '-v', action='store_true', help="Display version information and exit.")

    args = parser.parse_args()

    # Check if version information was requested
    if args.version:
        print_version_info()
        sys.exit(0)

    # Determine if we should use interactive selection
    use_interactive = args.interactive or args.directory is None
    
    if use_interactive:
        # Use interactive directory selection
        start_path = args.directory if args.directory else '.'
        selected_dir = select_directory(start_path)
        if not selected_dir:
            print("No directory selected. Exiting.")
            sys.exit(0)
        target_dir = selected_dir
    else:
        # Use command line argument
        normalized_path = normalize_path(args.directory)
        
        # Validate the directory
        target_dir = validate_directory(normalized_path)
        if not target_dir:
            print(f"Error: Directory not found, not a directory, or no read permissions: {normalized_path}", file=sys.stderr)
            sys.exit(1)

    # Get system info for better reporting
    system, system_version = get_system_info()
    apollo_version = get_version()
    print(f"Apollo v{apollo_version} - Running on {system} {system_version}")
    print(f"Scanning directory: {target_dir}...")
    python_files = find_python_files(target_dir)

    if not python_files:
        print("No Python files found in the specified directory.")
        sys.exit(0)

    print(f"Found {len(python_files)} Python files.")
    print("Building dependency graph...")
    dependency_graph = build_dependency_graph(python_files, target_dir)

    print("Rendering graph...")
    if args.view == 'ascii':
        print(render_ascii_graph(dependency_graph))
    elif args.view == 'blessed':
        render_blessed_graph(dependency_graph)

if __name__ == "__main__":
    main()