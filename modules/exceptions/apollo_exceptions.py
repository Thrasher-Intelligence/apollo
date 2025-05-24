"""
Custom exception classes for Apollo Python Dependency Analyzer.
Provides specific exception types for better error handling and user experience.
"""


class ApolloError(Exception):
    """Base exception class for all Apollo-related errors."""
    
    def __init__(self, message: str, details: str = None):
        super().__init__(message)
        self.message = message
        self.details = details
    
    def __str__(self):
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class DirectoryNotFoundError(ApolloError):
    """Raised when a specified directory does not exist."""
    
    def __init__(self, directory_path: str):
        message = f"Directory not found: {directory_path}"
        super().__init__(message)
        self.directory_path = directory_path


class DirectoryAccessError(ApolloError):
    """Raised when a directory cannot be accessed due to permissions."""
    
    def __init__(self, directory_path: str, reason: str = "Permission denied"):
        message = f"Cannot access directory: {directory_path}"
        super().__init__(message, reason)
        self.directory_path = directory_path


class ParsingError(ApolloError):
    """Raised when a Python file cannot be parsed."""
    
    def __init__(self, file_path: str, parse_error: str):
        message = f"Failed to parse Python file: {file_path}"
        super().__init__(message, parse_error)
        self.file_path = file_path


class RenderingError(ApolloError):
    """Raised when graph rendering fails."""
    
    def __init__(self, renderer_type: str, error_details: str):
        message = f"Rendering failed with {renderer_type} renderer"
        super().__init__(message, error_details)
        self.renderer_type = renderer_type


class ConfigurationError(ApolloError):
    """Raised when there's an issue with application configuration."""
    
    def __init__(self, config_issue: str):
        message = f"Configuration error: {config_issue}"
        super().__init__(message)