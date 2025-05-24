"""
Base renderer abstract class for Apollo Python Dependency Analyzer.
Defines the interface that all renderers must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Set


class BaseRenderer(ABC):
    """Abstract base class for all dependency graph renderers."""
    
    def __init__(self):
        """Initialize the renderer."""
        pass
    
    @abstractmethod
    def render(self, graph: Dict[str, Set[str]]) -> str:
        """
        Render the dependency graph.
        
        Args:
            graph: Dictionary mapping module names to their dependencies
            
        Returns:
            Rendered graph as a string (for ASCII) or None (for interactive renderers)
        """
        pass
    
    @abstractmethod
    def get_renderer_type(self) -> str:
        """
        Get the type/name of this renderer.
        
        Returns:
            String identifier for this renderer type
        """
        pass
    
    def validate_graph(self, graph: Dict[str, Set[str]]) -> bool:
        """
        Validate that the graph is properly formatted.
        
        Args:
            graph: The dependency graph to validate
            
        Returns:
            True if graph is valid, False otherwise
        """
        if not isinstance(graph, dict):
            return False
        
        for module, dependencies in graph.items():
            if not isinstance(module, str):
                return False
            if not isinstance(dependencies, set):
                return False
            for dep in dependencies:
                if not isinstance(dep, str):
                    return False
        
        return True
    
    def get_all_modules(self, graph: Dict[str, Set[str]]) -> Set[str]:
        """
        Get all unique modules mentioned in the graph.
        
        Args:
            graph: The dependency graph
            
        Returns:
            Set of all module names
        """
        all_modules = set(graph.keys())
        for dependencies in graph.values():
            all_modules.update(dependencies)
        return all_modules