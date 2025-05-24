# Apollo Modules Documentation

This directory contains the modular components of the Apollo Python Dependency Analyzer. The code has been organized into logical modules to improve maintainability, testability, and code reuse.

## Module Structure

```
modules/
├── cli/                    # Command line interface components
│   ├── __init__.py
│   └── argument_parser.py  # CLI argument parsing and validation
├── config/                 # Configuration management
│   ├── __init__.py
│   └── settings.py         # Application configuration and environment detection
├── core/                   # Core application logic
│   ├── __init__.py
│   ├── application.py      # Main application orchestrator
│   └── dependency_analyzer.py  # Core dependency analysis logic
├── exceptions/             # Custom exception classes
│   ├── __init__.py
│   └── apollo_exceptions.py  # Apollo-specific exceptions
├── renderers/              # Graph rendering implementations
│   ├── __init__.py
│   ├── base_renderer.py    # Abstract base renderer class
│   ├── ascii_renderer.py   # ASCII text-based renderer
│   └── blessed_renderer.py # Interactive blessed TUI renderer
├── directory_selector.py   # Interactive directory selection
├── file_finder.py          # Python file discovery
├── graph_builder.py        # Dependency graph construction
├── parser.py               # Python AST parsing
├── path_handler.py         # Path manipulation utilities
└── version.py              # Version information
```

## Module Descriptions

### CLI Module (`cli/`)
Handles command line interface functionality:
- **argument_parser.py**: Parses and validates command line arguments using argparse
- **ApolloArguments**: Data class containing parsed CLI arguments

### Configuration Module (`config/`)
Manages application configuration and environment detection:
- **settings.py**: Creates application configuration based on CLI arguments and environment
- **ApolloConfig**: Configuration data class
- Terminal capability detection and view mode determination

### Core Module (`core/`)
Contains the main application logic:
- **application.py**: Main application orchestrator that coordinates the entire workflow
- **dependency_analyzer.py**: Core dependency analysis logic, file discovery, and graph building
- **ApolloApp**: Main application class
- **DependencyAnalyzer**: Core analysis engine

### Exceptions Module (`exceptions/`)
Defines custom exception classes for better error handling:
- **ApolloError**: Base exception class
- **DirectoryNotFoundError**: Directory-related errors
- **DirectoryAccessError**: Permission-related errors
- **ParsingError**: Python file parsing errors
- **RenderingError**: Graph rendering errors
- **ConfigurationError**: Configuration-related errors

### Renderers Module (`renderers/`)
Implements different rendering strategies for dependency graphs:
- **BaseRenderer**: Abstract base class defining the renderer interface
- **AsciiRenderer**: Simple text-based ASCII art renderer
- **BlessedRenderer**: Interactive terminal UI renderer with navigation and graph visualization

### Legacy Modules
These modules maintain the original functionality but have been refactored to work with the new modular structure:
- **directory_selector.py**: Interactive directory selection using curses
- **file_finder.py**: Discovers Python files in directories
- **graph_builder.py**: Builds dependency graphs from Python files
- **parser.py**: Parses Python files using AST to extract imports
- **path_handler.py**: Path manipulation and validation utilities
- **version.py**: Version information and metadata

## Design Principles

### Separation of Concerns
Each module has a single, well-defined responsibility:
- CLI handling is separate from core logic
- Configuration is isolated from business logic
- Rendering implementations are interchangeable
- Error handling is centralized

### Dependency Injection
The modular design allows for easy testing and extension:
- Renderers implement a common interface
- Core logic doesn't depend on specific CLI or rendering implementations
- Configuration is passed as a parameter rather than global state

### Error Handling
Custom exceptions provide better error messages and allow for graceful error handling:
- Specific exception types for different error conditions
- Error details preserved for debugging
- Graceful fallbacks (e.g., blessed → ASCII rendering)

### Extensibility
The modular structure makes it easy to add new functionality:
- New renderers can be added by implementing BaseRenderer
- New CLI options can be added to the argument parser
- New analysis features can be added to DependencyAnalyzer

## Usage Examples

### Using Individual Modules

```python
from modules.core import ApolloApp
from modules.cli import parse_arguments
from modules.renderers import AsciiRenderer

# Parse CLI arguments
args = parse_arguments(['--ascii', '/path/to/project'])

# Run full application
app = ApolloApp()
exit_code = app.run()

# Use individual components
renderer = AsciiRenderer()
result = renderer.render(dependency_graph)
```

### Extending the System

```python
from modules.renderers import BaseRenderer

class CustomRenderer(BaseRenderer):
    def get_renderer_type(self) -> str:
        return "custom"
    
    def render(self, graph: Dict[str, Set[str]]) -> str:
        # Custom rendering logic
        return "Custom output"
```

## Testing Strategy

The modular structure facilitates unit testing:
- Each module can be tested independently
- Mock objects can be used to isolate components
- Integration tests can verify module interactions
- CLI and core logic can be tested separately

## Migration from Monolithic Structure

The original `main.py` functionality has been distributed as follows:
- Argument parsing → `cli/argument_parser.py`
- Configuration logic → `config/settings.py`
- Main application flow → `core/application.py`
- Dependency analysis → `core/dependency_analyzer.py`
- Rendering → `renderers/` module

The new `main.py` serves only as an entry point, delegating all functionality to the modular components.