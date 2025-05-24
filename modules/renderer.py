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

    # Calculate some metrics for visualization
    max_deps = max([len(deps) for deps in adj] or [0])
    num_root_modules = sum(1 for i, deps in enumerate(adj) if any(sorted_modules[i] in sorted_modules[adj_idx] for adj_idx in range(num_modules)))
    
    # Calculate node positions for the graph visualization
    def calculate_graph_positions(modules, adjacency_list, width, height):
        """Calculate 2D positions for nodes in the graph."""
        import math
        
        # Basic force-directed layout algorithm
        positions = {}
        
        # Initial positions in a circle
        radius = min(width, height) * 0.35
        center_x = width // 2
        center_y = height // 2
        
        for i, module in enumerate(modules):
            angle = 2 * math.pi * i / len(modules)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions[i] = (int(x), int(y))
        
        return positions
    
    # Draw a visual graph of connections
    def draw_graph(term, modules, adjacency_list, selected_idx, width, height):
        # Calculate positions
        node_positions = calculate_graph_positions(modules, adjacency_list, width, height)
        
        # Create a blank canvas
        canvas = [[" " for _ in range(width)] for _ in range(height)]
        
        # Draw edges first (so nodes appear on top)
        for i, deps in enumerate(adjacency_list):
            if not deps:
                continue
                
            x1, y1 = node_positions[i]
            for dep_idx in deps:
                x2, y2 = node_positions[dep_idx]
                
                # Draw a line between nodes
                # Simple Bresenham's line algorithm
                dx, dy = abs(x2 - x1), abs(y2 - y1)
                sx = 1 if x1 < x2 else -1
                sy = 1 if y1 < y2 else -1
                err = dx - dy
                
                x, y = x1, y1
                while not (x == x2 and y == y2):
                    if 0 <= x < width and 0 <= y < height:
                        canvas[y][x] = "·"  # Use a dot for the line
                    err2 = 2 * err
                    if err2 > -dy:
                        err -= dy
                        x += sx
                    if err2 < dx:
                        err += dx
                        y += sy
        
        # Draw nodes
        for i, module in enumerate(modules):
            x, y = node_positions[i]
            if 0 <= x < width and 0 <= y < height:
                # Use different characters for nodes based on their properties
                if i == selected_idx:
                    node_char = "◉"  # Selected node
                    node_color = term.white_on_cyan
                elif len(adjacency_list[i]) > 3:
                    node_char = "●"  # Node with many dependencies
                    node_color = term.yellow
                elif not adjacency_list[i]:
                    node_char = "○"  # Node with no dependencies
                    node_color = term.bright_black
                else:
                    node_char = "●"  # Regular node
                    node_color = term.green
                
                canvas[y][x] = node_color(node_char)
                
                # Add short label for the node (just first 2 parts of the module name)
                short_name = ".".join(modules[i].split(".")[:2])
                if len(short_name) > 10:
                    short_name = short_name[:9] + "…"
                
                label_x = x + 1
                if label_x < width and y < height:
                    # Make sure the label fits in the canvas
                    label_end = min(label_x + len(short_name), width)
                    for c_idx, char in enumerate(short_name[:label_end-label_x]):
                        if i == selected_idx:
                            canvas[y][label_x + c_idx] = term.white_on_cyan(char)
                        else:
                            canvas[y][label_x + c_idx] = char
        
        # Print the canvas
        for row in canvas:
            print("".join(row))
    
    # Enhanced TUI rendering
    try:
        # Setup terminal
        print(term.enter_fullscreen())
        print(term.hide_cursor())
        
        current_page = 0
        items_per_page = term.height - 15  # Reserve space for header and footer
        total_pages = (num_modules + items_per_page - 1) // items_per_page
        selected_idx = 0
        view_mode = "list"  # Start in list view, can toggle to "graph"
        
        # Define colors
        HEADER_COLOR = term.white_on_blue
        MODULE_COLOR = term.bold_blue
        DEPENDENCY_COLOR = term.green
        HIGHLIGHT_COLOR = term.white_on_cyan
        BOX_COLOR = term.bright_white
        INFO_COLOR = term.bright_white
        HELP_COLOR = term.bright_black
        
        # Arrow characters for connections
        VERTICAL = "│"
        HORIZONTAL = "─"
        CORNER = "└"
        ARROW = "→"
        TEE = "├"
        
        while True:
            term.clear()
            
            # Calculate page bounds
            start_idx = current_page * items_per_page
            end_idx = min(start_idx + items_per_page, num_modules)
            
            # Draw decorative header
            print(HEADER_COLOR(term.center(" Python Dependency Graph Visualizer ")))
            print(term.center(f"Modules: {num_modules} | Dependencies: {sum(len(d) for d in adj)} | Max Dependencies: {max_deps}"))
            print(BOX_COLOR("┌" + "─" * (term.width - 2) + "┐"))
            
            if view_mode == "list":
                # Display modules for current page
                for i in range(start_idx, end_idx):
                    module = sorted_modules[i]
                    is_selected = (i == selected_idx)
                    
                    # Format the module line
                    indent = " " * 2
                    module_text = f"{module}"
                    if is_selected:
                        print(f"{indent}{HIGHLIGHT_COLOR(' ' + module_text + ' ')}")
                    else:
                        print(f"{indent}{MODULE_COLOR(module_text)}")
                    
                    # Display dependencies if this is the selected module
                    if is_selected:
                        # Draw incoming dependencies (what depends on this module)
                        incoming = [j for j in range(num_modules) if i in adj[j]]
                        if incoming:
                            print(f"{indent}{indent}{term.bright_magenta('Used by:')}")
                            for idx, dep_idx in enumerate(incoming[:5]):  # Limit to 5 dependencies for display
                                last = (idx == len(incoming) - 1) or idx == 4
                                prefix = f"{indent}{indent}{CORNER if last else TEE}{HORIZONTAL}"
                                print(f"{prefix} {term.magenta(sorted_modules[dep_idx])}")
                            if len(incoming) > 5:
                                print(f"{indent}{indent}{CORNER}{HORIZONTAL} {term.magenta(f'... and {len(incoming) - 5} more')}")
                        
                        # Draw outgoing dependencies (what this module depends on)
                        outgoing = adj[i]
                        if outgoing:
                            print(f"{indent}{indent}{DEPENDENCY_COLOR('Depends on:')}")
                            for idx, dep_idx in enumerate(outgoing[:5]):  # Limit to 5 dependencies for display
                                last = (idx == len(outgoing) - 1) or idx == 4
                                prefix = f"{indent}{indent}{CORNER if last else TEE}{HORIZONTAL}"
                                print(f"{prefix} {DEPENDENCY_COLOR(sorted_modules[dep_idx])}")
                            if len(outgoing) > 5:
                                print(f"{indent}{indent}{CORNER}{HORIZONTAL} {DEPENDENCY_COLOR(f'... and {len(outgoing) - 5} more')}")
                    else:
                        # Just show dependency count for non-selected modules
                        deps_count = len(adj[i])
                        if deps_count > 0:
                            print(f"{indent}{indent}{DEPENDENCY_COLOR(f'» {deps_count} dependencies')}")
            else:  # Graph view
                # Draw the graph visualization
                graph_height = term.height - 12  # Reserve space for header and footer
                graph_width = term.width - 4
                print()  # Space before the graph
                draw_graph(term, sorted_modules, adj, selected_idx, graph_width, graph_height)
            
            # Footer with module details if selected
            if 0 <= selected_idx < num_modules:
                module = sorted_modules[selected_idx]
                print(BOX_COLOR("├" + "─" * (term.width - 2) + "┤"))
                print(f" {INFO_COLOR('Selected:')} {MODULE_COLOR(module)}")
                
                # Calculate dependency metrics for this module
                outgoing = len(adj[selected_idx])
                incoming = sum(1 for j in range(num_modules) if selected_idx in adj[j])
                
                # Display metrics in a horizontal layout
                metrics = [
                    f"Outgoing: {outgoing}",
                    f"Incoming: {incoming}",
                    f"Total: {outgoing + incoming}"
                ]
                print(" " + " | ".join(INFO_COLOR(m) for m in metrics))
            
            # Navigation footer
            print(BOX_COLOR("└" + "─" * (term.width - 2) + "┘"))
            if total_pages > 1 and view_mode == "list":
                page_info = f"Page {current_page + 1}/{total_pages}"
                print(term.center(HELP_COLOR(page_info)))
            
            # Help text
            controls = [
                "↑/↓: Navigate",
                "←/→: Change page" if view_mode == "list" else "←/→: Navigate",
                "g: Toggle Graph View",
                "q: Quit"
            ]
            print(term.center(HELP_COLOR(" | ".join(controls))))
            
            # Handle keyboard input
            key = term.inkey()
            
            if key.name == 'KEY_UP':
                selected_idx = max(0, selected_idx - 1)
                # If selected item is now on previous page, change page
                if selected_idx < start_idx and view_mode == "list":
                    current_page = max(0, current_page - 1)
                    
            elif key.name == 'KEY_DOWN':
                selected_idx = min(num_modules - 1, selected_idx + 1)
                # If selected item is now on next page, change page
                if selected_idx >= end_idx and view_mode == "list":
                    current_page = min(total_pages - 1, current_page + 1)
                    
            elif key.name == 'KEY_LEFT':
                if view_mode == "list":
                    current_page = max(0, current_page - 1)
                    # Adjust selected item to be on this page
                    selected_idx = min(selected_idx, end_idx - 1)
                    selected_idx = max(selected_idx, start_idx)
                else:
                    # In graph view, just navigate between nodes
                    selected_idx = max(0, selected_idx - 1)
                
            elif key.name == 'KEY_RIGHT':
                if view_mode == "list":
                    current_page = min(total_pages - 1, current_page + 1)
                    # Adjust selected item to be on this page
                    start_idx = current_page * items_per_page
                    end_idx = min(start_idx + items_per_page, num_modules)
                    selected_idx = max(selected_idx, start_idx)
                    selected_idx = min(selected_idx, end_idx - 1)
                else:
                    # In graph view, just navigate between nodes
                    selected_idx = min(num_modules - 1, selected_idx + 1)
                
            elif key.lower() == 'g':
                # Toggle between list and graph view
                view_mode = "graph" if view_mode == "list" else "list"
                
            elif key.lower() == 'q' or key.name == 'KEY_ESCAPE':
                break
    
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up terminal
        print(term.exit_fullscreen())
        print(term.normal_cursor())
        print(term.clear())