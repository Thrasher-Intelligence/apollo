#!/usr/bin/env python3
"""
Apollo Python Dependency Analyzer
Main entry point for the application.
"""

import sys
from modules.core import ApolloApp


def main():
    """Main entry point for Apollo."""
    app = ApolloApp()
    exit_code = app.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()