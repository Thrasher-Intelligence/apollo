"""
Exception classes for Apollo Python Dependency Analyzer.
Custom exceptions for better error handling and user experience.
"""

from .apollo_exceptions import (
    ApolloError,
    DirectoryNotFoundError,
    DirectoryAccessError,
    ParsingError,
    RenderingError,
    ConfigurationError
)

__all__ = [
    'ApolloError',
    'DirectoryNotFoundError', 
    'DirectoryAccessError',
    'ParsingError',
    'RenderingError',
    'ConfigurationError'
]