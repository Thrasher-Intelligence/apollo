"""
Core module for Apollo Python Dependency Analyzer.
Contains the main application logic and orchestration.
"""

from .application import ApolloApp
from .dependency_analyzer import DependencyAnalyzer

__all__ = ['ApolloApp', 'DependencyAnalyzer']