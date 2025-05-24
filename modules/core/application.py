"""
Main application orchestrator for Apollo Python Dependency Analyzer.
Coordinates the entire application flow from argument parsing to rendering.
"""

import sys
from typing import Optional

from ..cli import parse_arguments, ApolloArguments
from ..config import create_config, ApolloConfig
from ..version import print_version_info
from ..renderers import AsciiRenderer, BlessedRenderer
from ..exceptions import ApolloError, RenderingError
from .dependency_analyzer import DependencyAnalyzer


class ApolloApp:
    """Main application class that orchestrates the entire Apollo workflow."""
    
    def __init__(self):
        """Initialize the Apollo application."""
        self.analyzer = DependencyAnalyzer()
        self.config: Optional[ApolloConfig] = None
        self.args: Optional[ApolloArguments] = None
    
    def run(self, args: Optional[list] = None) -> int:
        """
        Run the complete Apollo application.
        
        Args:
            args: Optional list of command line arguments
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Parse command line arguments
            self.args = parse_arguments(args)
            
            # Handle version request
            if self.args.version:
                print_version_info()
                return 0
            
            # Determine if we should use interactive selection
            use_interactive = self.args.interactive or self.args.directory is None
            
            # Perform dependency analysis
            dependency_graph = self.analyzer.analyze(
                directory_path=self.args.directory,
                use_interactive=use_interactive
            )
            
            # Create configuration
            if not self.analyzer.target_directory:
                raise ValueError("Target directory not set after analysis")
            self.config = create_config(self.args, self.analyzer.target_directory)
            
            # Check if we found any Python files
            if not self.analyzer.python_files:
                print("No Python files found in the specified directory.")
                return 0
            
            # Display progress information in ASCII mode
            if self.config.view_mode == 'ascii':
                self._display_analysis_info()
            
            # Render the dependency graph
            self._render_graph(dependency_graph)
            
            return 0
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return 1
        except ApolloError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1
    
    def _display_analysis_info(self):
        """Display analysis information for ASCII mode."""
        if not self.config:
            return
        
        print(f"Apollo v{self.config.apollo_version} - Running on {self.config.system_name} {self.config.system_version}")
        print(f"Scanning directory: {self.config.target_directory}...")
        print(f"Found {len(self.analyzer.python_files)} Python files.")
        print("Building dependency graph...")
        print("Rendering graph...")
    
    def _render_graph(self, dependency_graph):
        """
        Render the dependency graph using the appropriate renderer.
        
        Args:
            dependency_graph: The dependency graph to render
        """
        if not self.config:
            raise ValueError("Configuration must be set before rendering")
        
        try:
            if self.config.view_mode == 'ascii':
                renderer = AsciiRenderer()
                result = renderer.render(dependency_graph)
                if result:
                    print(result)
            else:
                renderer = BlessedRenderer()
                renderer.render(dependency_graph)
                
        except RenderingError as e:
            if e.renderer_type == 'blessed':
                print(f"\nError with blessed visualization: {e.details}")
                print("Falling back to ASCII visualization...")
                # Fallback to ASCII renderer
                renderer = AsciiRenderer()
                result = renderer.render(dependency_graph)
                if result:
                    print(result)
            else:
                raise
        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            raise
    
    def get_analysis_summary(self):
        """Get a summary of the current analysis."""
        return self.analyzer.get_analysis_summary()
    
    def get_module_statistics(self, module_name: str):
        """Get statistics for a specific module."""
        return self.analyzer.get_module_statistics(module_name)