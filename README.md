# Apollo Python Dependency Analyzer

A tool for analyzing and visualizing Python project dependencies.

## Features

- **Interactive Directory Selection**: Navigate through your file system using arrow keys
- **Dependency Analysis**: Discover and analyze Python module dependencies
- **Multiple Visualization Options**: View dependencies in ASCII or with a rich TUI using the blessed library
- **Path Flexibility**: Supports tilde (~) expansion and environment variables in paths

## Installation

You have several options for installation:

### Option 1: Clone and Run (No Installation)

No installation required! Apollo is a standalone Python application.

```bash
# Clone the repository
git clone https://github.com/thrasher-intelligence/apollo.git
cd apollo

# Install dependencies
pip install -r requirements.txt

# Run the application
./run.sh
```

### Option 2: Install as a Package

```bash
# Clone the repository
git clone https://github.com/thrasher-intelligence/apollo.git
cd apollo

# Install the package
pip install .

# Run the application
apollo
```

### Option 3: Install from PyPI (coming soon)

```bash
pip install apollo-deps
apollo
```

*Created and maintained by Jacob Eaker (jacob.eaker@gmail.com)*

### Requirements

- Python 3.6 or higher
- Blessed library (optional, for enhanced TUI rendering)

To install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the included shell script for the easiest experience:

```bash
./run.sh
```

This will launch Apollo in interactive mode, allowing you to navigate to the directory you want to analyze.

### Command Line Options

```bash
python main.py [directory] [--view {ascii,blessed}] [--interactive]
```

- `directory`: The directory to analyze (optional, defaults to interactive selection)
- `--view`: Rendering method (ascii or blessed, default: ascii)
- `--interactive`, `-i`: Force interactive directory selection

### Examples

```bash
# Interactive directory selection
python main.py

# Analyze a specific directory
python main.py ~/my-project

# Analyze current directory with blessed UI
python main.py . --view blessed

# Force interactive mode but start in a specific directory
python main.py ~/projects --interactive
```

## Interactive Navigation

When using interactive mode:

- **↑/↓ arrows**: Navigate through files and directories
- **→ arrow or Enter**: Enter a directory or select current directory
- **← arrow**: Go to parent directory
- **q or Esc**: Quit without selecting

## Project Structure

- `main.py`: Entry point for the application
- `modules/`: Directory containing modularized components:
  - `parser.py`: Python file parsing functionality
  - `graph_builder.py`: Dependency graph generation
  - `renderer.py`: Visualization of dependency graphs
  - `file_finder.py`: File discovery utilities
  - `path_handler.py`: Path expansion and validation
  - `directory_selector.py`: Interactive directory selection

## How It Works

1. Apollo scans the selected directory for Python files
2. It parses each file to identify imports
3. It builds a dependency graph based on these imports
4. The graph is visualized according to the chosen renderer

## License

MIT License, Copyright (c) 2025 Jacob Eaker
