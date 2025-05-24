"""
Core dependency analysis logic for Apollo Python Dependency Analyzer.
Orchestrates the analysis of Python projects and dependency graph generation.
"""

import os
from typing import Dict, Set, List, Optional

from ..file_finder import find_python_files
from ..graph_builder import build_dependency_graph
from ..path_handler import validate_directory, normalize_path
from ..directory_selector import select_directory
from ..exceptions import DirectoryNotFoundError, DirectoryAccessError


class DependencyAnalyzer:
    """Core class for analyzing Python project dependencies."""
    
    def __init__(self):
        """Initialize the dependency analyzer."""
        self.target_directory: Optional[str] = None
        self.python_files: List[str] = []
        self.dependency_graph: Dict[str, Set[str]] = {}
    
    def set_target_directory(self, directory_path: Optional[str], 
                           use_interactive: bool = False) -> str:
        """
        Set and validate the target directory for analysis.
        
        Args:
            directory_path: The directory path to analyze
            use_interactive: Whether to use interactive directory selection
            
        Returns:
            The validated target directory path
            
        Raises:
            DirectoryNotFoundError: If directory doesn't exist
            DirectoryAccessError: If directory cannot be accessed
        """
        if use_interactive:
            # Use interactive directory selection
            start_path = directory_path if directory_path else '.'
            selected_dir = select_directory(start_path)
            if not selected_dir:
                raise DirectoryNotFoundError("No directory selected")
            self.target_directory = selected_dir
        else:
            # Use provided directory path
            if not directory_path:
                raise DirectoryNotFoundError("No directory provided")
            
            normalized_path = normalize_path(directory_path)
            validated_dir = validate_directory(normalized_path)
            
            if not validated_dir:
                if not os.path.exists(normalized_path):
                    raise DirectoryNotFoundError(normalized_path)
                elif not os.path.isdir(normalized_path):
                    raise DirectoryAccessError(normalized_path, "Path is not a directory")
                else:
                    raise DirectoryAccessError(normalized_path, "No read permissions")
            
            self.target_directory = validated_dir
        
        return self.target_directory
    
    def find_python_files(self) -> List[str]:
        """
        Find all Python files in the target directory.
        
        Returns:
            List of Python file paths
            
        Raises:
            ValueError: If target directory is not set
        """
        if not self.target_directory:
            raise ValueError("Target directory must be set before finding Python files")
        
        self.python_files = find_python_files(self.target_directory)
        return self.python_files
    
    def build_dependency_graph(self) -> Dict[str, Set[str]]:
        """
        Build the dependency graph from the found Python files.
        
        Returns:
            Dictionary mapping module names to their dependencies
            
        Raises:
            ValueError: If Python files haven't been found yet
        """
        if not self.python_files:
            raise ValueError("Python files must be found before building dependency graph")
        
        if not self.target_directory:
            raise ValueError("Target directory must be set")
        
        self.dependency_graph = build_dependency_graph(self.python_files, self.target_directory)
        return self.dependency_graph
    
    def analyze(self, directory_path: Optional[str] = None, 
               use_interactive: bool = False) -> Dict[str, Set[str]]:
        """
        Perform complete dependency analysis.
        
        Args:
            directory_path: The directory path to analyze
            use_interactive: Whether to use interactive directory selection
            
        Returns:
            The dependency graph
        """
        # Set target directory
        self.set_target_directory(directory_path, use_interactive)
        
        # Find Python files
        self.find_python_files()
        
        # Build dependency graph
        self.build_dependency_graph()
        
        return self.dependency_graph
    
    def get_analysis_summary(self) -> Dict[str, int]:
        """
        Get a summary of the analysis results.
        
        Returns:
            Dictionary containing analysis statistics
        """
        if not self.dependency_graph:
            return {
                "total_modules": 0,
                "modules_with_dependencies": 0,
                "total_dependency_relationships": 0,
                "python_files_found": len(self.python_files)
            }
        
        all_modules = set(self.dependency_graph.keys())
        for dependencies in self.dependency_graph.values():
            all_modules.update(dependencies)
        
        modules_with_deps = len([deps for deps in self.dependency_graph.values() if deps])
        total_relationships = sum(len(deps) for deps in self.dependency_graph.values())
        
        return {
            "total_modules": len(all_modules),
            "modules_with_dependencies": modules_with_deps,
            "total_dependency_relationships": total_relationships,
            "python_files_found": len(self.python_files)
        }
    
    def get_module_statistics(self, module_name: str) -> Optional[Dict[str, int]]:
        """
        Get statistics for a specific module.
        
        Args:
            module_name: Name of the module to analyze
            
        Returns:
            Dictionary with module statistics or None if module not found
        """
        if not self.dependency_graph:
            return None
        
        # Find all modules
        all_modules = set(self.dependency_graph.keys())
        for dependencies in self.dependency_graph.values():
            all_modules.update(dependencies)
        
        if module_name not in all_modules:
            return None
        
        # Calculate outgoing dependencies
        outgoing = len(self.dependency_graph.get(module_name, set()))
        
        # Calculate incoming dependencies
        incoming = sum(1 for deps in self.dependency_graph.values() 
                      if module_name in deps)
        
        return {
            "outgoing_dependencies": outgoing,
            "incoming_dependencies": incoming,
            "total_connections": outgoing + incoming
        }