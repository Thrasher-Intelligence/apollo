#!/bin/bash

# A simple script to run the Apollo Python Dependency Graph analyzer

# Exit if any command fails
set -e

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

# Run the Apollo application with interactive mode by default
python3 main.py --interactive "$@"

# Print usage instructions
echo
echo "Usage:"
echo "  ./run.sh [directory] [--view {ascii,blessed}]"
echo
echo "Examples:"
echo "  ./run.sh               # Interactive directory selection"
echo "  ./run.sh ~/my-project  # Analyze a specific directory"
echo "  ./run.sh --view blessed # Use the blessed UI renderer"