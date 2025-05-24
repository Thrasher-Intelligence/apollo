"""
Apollo CLI Argument Parser
Handles command line argument parsing and validation.
"""

import argparse
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class ApolloArguments:
    """Data class to hold parsed command line arguments."""
    directory: Optional[str] = None
    view: str = 'blessed'
    interactive: bool = False
    ascii: bool = False
    version: bool = False
    force_ascii: bool = False


def parse_arguments(args: Optional[list] = None) -> ApolloArguments:
    """
    Parse command line arguments and return an ApolloArguments object.
    
    Args:
        args: Optional list of arguments to parse. If None, uses sys.argv.
        
    Returns:
        ApolloArguments object with parsed values.
    """
    parser = argparse.ArgumentParser(
        description="Analyze Python project dependencies.",
        prog="apollo"
    )
    
    parser.add_argument(
        'directory', 
        nargs='?', 
        default=None, 
        help="The directory to analyze (default: interactive selection). "
             "Supports tilde (~) for home directory."
    )
    
    parser.add_argument(
        '--view', 
        choices=['ascii', 'blessed'], 
        default='blessed',
        help="Rendering method (blessed or ascii, default: blessed)."
    )
    
    parser.add_argument(
        '--interactive', '-i', 
        action='store_true', 
        help="Use interactive directory selection regardless of whether "
             "a directory is provided."
    )
    
    parser.add_argument(
        '--ascii', '-a', 
        action='store_true', 
        help="Use simple ASCII output instead of the default blessed visualization."
    )
    
    parser.add_argument(
        '--version', '-v', 
        action='store_true', 
        help="Display version information and exit."
    )
    
    parser.add_argument(
        '--force-ascii', 
        action='store_true', 
        help=argparse.SUPPRESS  # Hidden option for troubleshooting
    )

    parsed_args = parser.parse_args(args)
    
    return ApolloArguments(
        directory=parsed_args.directory,
        view=parsed_args.view,
        interactive=parsed_args.interactive,
        ascii=parsed_args.ascii,
        version=parsed_args.version,
        force_ascii=parsed_args.force_ascii
    )


def validate_arguments(args: ApolloArguments) -> bool:
    """
    Validate the parsed arguments for logical consistency.
    
    Args:
        args: The parsed arguments to validate.
        
    Returns:
        True if arguments are valid, False otherwise.
    """
    # Currently no complex validation needed, but this provides
    # a place to add validation logic in the future
    return True