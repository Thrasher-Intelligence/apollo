"""
ASCII renderer for Apollo Python Dependency Analyzer.
Provides simple text-based rendering of dependency graphs.
"""

from typing import Dict, Set
from .base_renderer import BaseRenderer


class AsciiRenderer(BaseRenderer):
    """ASCII-based renderer for dependency graphs."""
    
    def __init__(self):
        """Initialize the ASCII renderer."""
        super().__init__()
    
    def get_renderer_type(self) -> str:
        """Get the renderer type identifier."""
        return "ascii"
    
    def render(self, graph: Dict[str, Set[str]]) -> str:
        """
        Render the dependency graph using ASCII art.
        
        Args:
            graph: Dictionary mapping module names to their dependencies
            
        Returns:
            ASCII representation of the dependency graph
        """
        if not self.validate_graph(graph):
            return "Error: Invalid graph format"
        
        if not graph:
            return "No dependencies found."
        
        # Get all unique modules and sort them
        all_modules = self.get_all_modules(graph)
        sorted_modules = sorted(list(all_modules))
        
        # Create a mapping from module name to index
        module_to_index = {module: i for i, module in enumerate(sorted_modules)}
        num_modules = len(sorted_modules)
        
        # Build adjacency list based on sorted modules
        adjacency_list = [[] for _ in range(num_modules)]
        for module, dependencies in graph.items():
            if module in module_to_index:
                module_index = module_to_index[module]
                for dependency in dependencies:
                    if dependency in module_to_index:
                        dep_index = module_to_index[dependency]
                        adjacency_list[module_index].append(dep_index)
        
        # Generate the ASCII tree representation
        output_lines = []
        for i, module in enumerate(sorted_modules):
            output_lines.append(f"{module}")
            
            # Add dependencies for this module
            dependencies = adjacency_list[i]
            for j, dep_index in enumerate(dependencies):
                dependency_module = sorted_modules[dep_index]
                
                # Use different tree characters for last dependency
                if j == len(dependencies) - 1:
                    output_lines.append(f"  └── {dependency_module}")
                else:
                    output_lines.append(f"  ├── {dependency_module}")
        
        return "\n".join(output_lines)
    
    def render_with_stats(self, graph: Dict[str, Set[str]]) -> str:
        """
        Render the graph with additional statistics.
        
        Args:
            graph: The dependency graph to render
            
        Returns:
            ASCII representation with statistics
        """
        if not graph:
            return "No dependencies found."
        
        # Calculate statistics
        all_modules = self.get_all_modules(graph)
        total_modules = len(all_modules)
        modules_with_deps = len([m for m in graph.values() if m])
        total_dependencies = sum(len(deps) for deps in graph.values())
        
        # Generate main graph
        graph_output = self.render(graph)
        
        # Add statistics
        stats = [
            "",
            "=" * 50,
            "DEPENDENCY STATISTICS",
            "=" * 50,
            f"Total modules: {total_modules}",
            f"Modules with dependencies: {modules_with_deps}",
            f"Total dependency relationships: {total_dependencies}",
            ""
        ]
        
        return graph_output + "\n" + "\n".join(stats)