"""
Apollo Python Dependency Analyzer
Version Information Module
"""

__version__ = "0.1.0"
__author__ = "Jacob Eaker"
__license__ = "MIT"
__release_date__ = "2025-05-23"

def get_version():
    """Returns the current version of Apollo"""
    return __version__

def get_version_info():
    """Returns detailed version information"""
    return {
        "version": __version__,
        "author": __author__,
        "license": __license__,
        "release_date": __release_date__
    }

def print_version_info():
    """Prints formatted version information to stdout"""
    print(f"Apollo Python Dependency Analyzer v{__version__}")
    print(f"Released: {__release_date__}")
    print(f"License: {__license__}")
    print(f"Author: {__author__}")

if __name__ == "__main__":
    print_version_info()