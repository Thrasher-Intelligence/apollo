#!/bin/bash

# A simple script to run the Apollo Python Dependency Graph analyzer

# Exit if any command fails
set -e

# Enable debug mode with -d flag
DEBUG_MODE=false

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found. Please install Python 3."
    exit 1
fi

# Check if required modules are installed
if ! python3 -c "import curses" &> /dev/null; then
    echo "The 'curses' module is required for the interactive interface."
    echo "It should be included with most Python installations."
    exit 1
fi

# Process script arguments
for arg in "$@"; do
    if [ "$arg" = "-d" ] || [ "$arg" = "--debug" ]; then
        DEBUG_MODE=true
        # Remove debug flag from args passed to Python
        set -- "${@/$arg/}"
    fi
done

# Run with debug options if debug mode is enabled
if [ "$DEBUG_MODE" = true ]; then
    echo "Running in debug mode..."
    export PYTHONIOENCODING=utf-8
    export TERM=xterm-256color
    
    # Run with ASCII first to test basic functionality
    echo "Testing basic ASCII mode..."
    python3 main.py --ascii . && echo "ASCII mode works correctly."
    
    echo "Now trying blessed mode with verbose logging..."
    python3 -u main.py --interactive "$@" 2>apollo_error.log
    
    if [ -f "apollo_error.log" ] && [ -s "apollo_error.log" ]; then
        echo "Errors detected! Check apollo_error.log for details."
        echo "Error summary:"
        tail -10 apollo_error.log
    else
        echo "No errors detected."
    fi
else
    # Run the Apollo application with interactive mode by default
    python3 main.py --interactive --view blessed "$@"
fi

# Print usage instructions
echo
echo "Usage:"
echo "  ./run.sh [directory] [--view {ascii,blessed}] [-d|--debug]"
echo
echo "Examples:"
echo "  ./run.sh               # Interactive directory selection with blessed UI"
echo "  ./run.sh ~/my-project  # Analyze a specific directory"
echo "  ./run.sh --ascii       # Use simple ASCII output instead of blessed UI"
echo "  ./run.sh -d            # Run in debug mode for troubleshooting terminal issues"