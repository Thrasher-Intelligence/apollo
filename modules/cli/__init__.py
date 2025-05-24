"""
CLI module for Apollo Python Dependency Analyzer.
Handles command line argument parsing and validation.
"""

from .argument_parser import parse_arguments, ApolloArguments

__all__ = ['parse_arguments', 'ApolloArguments']