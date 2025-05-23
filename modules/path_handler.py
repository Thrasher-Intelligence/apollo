import os
import platform
from typing import Optional, Tuple

def expand_path(path: str) -> str:
    """
    Expands a path that may contain a tilde (~) to represent the user's home directory.
    
    Args:
        path: A file path that may contain a tilde.
        
    Returns:
        The expanded absolute path with the tilde replaced by the user's home directory.
    """
    # Expand the tilde to the user's home directory
    expanded_path = os.path.expanduser(path)
    
    # Handle environment variables in the path
    expanded_path = os.path.expandvars(expanded_path)
    
    # Convert to absolute path
    absolute_path = os.path.abspath(expanded_path)
    
    return absolute_path

def validate_directory(path: str) -> Optional[str]:
    """
    Validates that a path exists and is a directory.
    
    Args:
        path: A file path to validate.
        
    Returns:
        The absolute path if valid, None otherwise.
    """
    expanded_path = expand_path(path)
    
    if not os.path.exists(expanded_path):
        return None
    
    if not os.path.isdir(expanded_path):
        return None
    
    # Check if we have read permissions on the directory
    if not os.access(expanded_path, os.R_OK):
        return None
        
    return expanded_path

def get_relative_path(path: str, base_dir: str) -> str:
    """
    Gets the relative path of a file compared to a base directory.
    
    Args:
        path: Absolute path to a file.
        base_dir: Base directory to compare against.
        
    Returns:
        Relative path from base_dir to path.
    """
    return os.path.relpath(path, base_dir)

def get_system_info() -> Tuple[str, str]:
    """
    Gets information about the current operating system.
    
    Returns:
        A tuple containing (system_name, system_version)
    """
    system = platform.system()
    version = platform.release()
    return system, version

def normalize_path(path: str) -> str:
    """
    Normalizes a path for the current operating system.
    
    Args:
        path: A file path to normalize.
        
    Returns:
        A normalized path appropriate for the current OS.
    """
    # Expand the path and handle special characters
    expanded_path = expand_path(path)
    
    # Normalize the path (resolve .. and .)
    normalized_path = os.path.normpath(expanded_path)
    
    # Handle symbolic links by resolving to the real path
    if os.path.exists(normalized_path):
        try:
            normalized_path = os.path.realpath(normalized_path)
        except (OSError, IOError):
            # If we can't resolve the real path, keep the normalized one
            pass
    
    return normalized_path