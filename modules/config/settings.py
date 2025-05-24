"""
Apollo Configuration Settings
Manages application configuration, environment detection, and runtime settings.
"""

import os
from dataclasses import dataclass
from typing import Tuple

from ..cli.argument_parser import ApolloArguments
from ..path_handler import get_system_info


@dataclass
class ApolloConfig:
    """Configuration settings for Apollo application."""
    target_directory: str
    view_mode: str
    interactive_mode: bool
    supports_advanced_terminal: bool
    system_name: str
    system_version: str
    apollo_version: str


def detect_terminal_capabilities() -> bool:
    """
    Detect if the terminal supports advanced features like colors and cursor control.
    
    Returns:
        True if terminal supports advanced features, False otherwise.
    """
    term = os.environ.get('TERM', '').lower()
    
    # List of terminals that don't support advanced features
    unsupported_terms = {'dumb', 'unknown', ''}
    
    return term not in unsupported_terms


def determine_view_mode(args: ApolloArguments, terminal_supports_advanced: bool) -> str:
    """
    Determine the appropriate view mode based on arguments and terminal capabilities.
    
    Args:
        args: Parsed command line arguments
        terminal_supports_advanced: Whether terminal supports advanced features
        
    Returns:
        The view mode to use ('ascii' or 'blessed')
    """
    # Force ASCII if explicitly requested or terminal doesn't support advanced features
    if args.ascii or args.force_ascii or not terminal_supports_advanced:
        return 'ascii'
    
    return args.view


def create_config(args: ApolloArguments, target_directory: str) -> ApolloConfig:
    """
    Create application configuration from arguments and environment.
    
    Args:
        args: Parsed command line arguments
        target_directory: The validated target directory path
        
    Returns:
        Configured ApolloConfig object
    """
    from ..version import get_version
    
    # Get system information
    system_name, system_version = get_system_info()
    
    # Detect terminal capabilities
    supports_advanced = detect_terminal_capabilities()
    
    # Determine view mode
    view_mode = determine_view_mode(args, supports_advanced)
    
    return ApolloConfig(
        target_directory=target_directory,
        view_mode=view_mode,
        interactive_mode=args.interactive or args.directory is None,
        supports_advanced_terminal=supports_advanced,
        system_name=system_name,
        system_version=system_version,
        apollo_version=get_version()
    )