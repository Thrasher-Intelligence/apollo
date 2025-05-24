# apollo/modules/__init__.py
# This file makes the modules directory a Python package

# Core application components
from .core import ApolloApp, DependencyAnalyzer

# CLI components
from .cli import parse_arguments, ApolloArguments

# Configuration
from .config import ApolloConfig, create_config

# Renderers
from .renderers import AsciiRenderer, BlessedRenderer, BaseRenderer

# Exceptions
from .exceptions import (
    ApolloError,
    DirectoryNotFoundError,
    DirectoryAccessError,
    ParsingError,
    RenderingError,
    ConfigurationError
)

# Legacy modules (keeping for backward compatibility)
from . import path_handler
from . import directory_selector
from . import file_finder
from . import graph_builder
from . import parser
from . import version

__all__ = [
    # Core
    'ApolloApp',
    'DependencyAnalyzer',
    
    # CLI
    'parse_arguments',
    'ApolloArguments',
    
    # Config
    'ApolloConfig',
    'create_config',
    
    # Renderers
    'AsciiRenderer',
    'BlessedRenderer',
    'BaseRenderer',
    
    # Exceptions
    'ApolloError',
    'DirectoryNotFoundError',
    'DirectoryAccessError',
    'ParsingError',
    'RenderingError',
    'ConfigurationError',
    
    # Legacy modules
    'path_handler',
    'directory_selector',
    'file_finder',
    'graph_builder',
    'parser',
    'version'
]