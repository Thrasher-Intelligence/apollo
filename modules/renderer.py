from typing import Dict, Set

def render_ascii_graph(graph: Dict[str, Set[str]]) -> str:
    """Renders the dependency graph using ASCII art."""
    if not graph:
        return "No dependencies found."

    # Get all unique modules
    all_modules = set(graph.keys())
    for deps in graph.values():
        all_modules.update(deps)

    sorted_modules = sorted(list(all_modules))

    # Create a mapping from module name to index for sorting
    module_to_index = {module: i for i, module in enumerate(sorted_modules)}
    num_modules = len(sorted_modules)

    # Build adjacency list based on sorted modules
    adj = [[] for _ in range(num_modules)]
    for module, deps in graph.items():
        if module in module_to_index:
            u_idx = module_to_index[module]
            for dep in deps:
                if dep in module_to_index:
                    v_idx = module_to_index[dep]
                    adj[u_idx].append(v_idx)

    # Simple tree representation (can be improved)
    output = []
    for i, module in enumerate(sorted_modules):
        output.append(f"{module}")
        for dep_idx in adj[i]:
            dep_module = sorted_modules[dep_idx]
            output.append(f"  └── {dep_module}")

    return "\n".join(output)

def render_blessed_graph(graph: Dict[str, Set[str]]):
    """Renders the dependency graph using the blessed library TUI."""
    try:
        from blessed import Terminal
    except ImportError:
        import sys
        print("Error: 'blessed' library is required for TUI rendering.", file=sys.stderr)
        print("Install it using: pip install blessed", file=sys.stderr)
        return

    term = Terminal()

    if not graph:
        print(term.yellow("No dependencies found."))
        return

    # Get all unique modules
    all_modules = set(graph.keys())
    for deps in graph.values():
        all_modules.update(deps)

    sorted_modules = sorted(list(all_modules))

    # Create a mapping from module name to index for sorting
    module_to_index = {module: i for i, module in enumerate(sorted_modules)}
    num_modules = len(sorted_modules)

    # Build adjacency list based on sorted modules
    adj = [[] for _ in range(num_modules)]
    for module, deps in graph.items():
        if module in module_to_index:
            u_idx = module_to_index[module]
            for dep in deps:
                if dep in module_to_index:
                    v_idx = module_to_index[dep]
                    adj[u_idx].append(v_idx)

    # Simple TUI rendering
    with term.cbreak(), term.hidden():
        print(term.bold("Python Dependency Graph"))
        print("-" * term.width)

        for i, module in enumerate(sorted_modules):
            print(f"{term.blue(module)}:")
            for dep_idx in adj[i]:
                dep_module = sorted_modules[dep_idx]
                print(f"  └── {term.green(dep_module)}")

        print("-" * term.width)
        print(term.dim("Legend:"))
        print(f"  {term.blue('Blue')}: Dependent Module")
        print(f"  {term.green('Green')}: Dependency Module")
        print(term.dim("Press Ctrl+C to exit."))

        try:
            while True:
                term.inkey() # Wait for user input
        except KeyboardInterrupt:
            pass