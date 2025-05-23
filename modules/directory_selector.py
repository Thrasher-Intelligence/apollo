import os
import sys
import curses
from typing import Optional, List, Tuple

def _setup_colors() -> None:
    """Initialize color pairs for the directory selector."""
    # Define color pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Selected item
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Directory
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Python file
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Regular file
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Help text

def _get_directory_contents(path: str) -> List[Tuple[str, str]]:
    """
    Get directory contents with file types.
    
    Args:
        path: Path to the directory
        
    Returns:
        List of tuples (name, type) where type is 'dir', 'py', or 'file'
    """
    try:
        contents = []
        
        # Add parent directory option unless we're at root
        if os.path.abspath(path) != os.path.abspath(os.path.sep):
            contents.append(("..", "dir"))
        
        # List all entries in the directory
        for entry in sorted(os.listdir(path)):
            full_path = os.path.join(path, entry)
            
            # Skip hidden files/directories (starting with .)
            if entry.startswith('.') and entry != "..":
                continue
                
            # Determine type
            if os.path.isdir(full_path):
                contents.append((entry, "dir"))
            elif entry.endswith(".py"):
                contents.append((entry, "py"))
            else:
                contents.append((entry, "file"))
        
        return contents
    except (PermissionError, FileNotFoundError):
        # Return just parent directory if we can't read this one
        return [("..", "dir")]

def _draw_directory_contents(
    stdscr, 
    path: str, 
    contents: List[Tuple[str, str]], 
    selected_idx: int, 
    start_idx: int,
    height: int
) -> None:
    """
    Draw directory contents with scrolling.
    
    Args:
        stdscr: Curses window
        path: Current path
        contents: List of directory contents
        selected_idx: Index of selected item
        start_idx: Index to start displaying from (for scrolling)
        height: Number of lines available for display
    """
    max_y, max_x = stdscr.getmaxyx()
    
    # Clear screen
    stdscr.clear()
    
    # Display header with current path
    header = f" Directory: {path} "
    stdscr.addstr(0, 0, header, curses.A_BOLD)
    stdscr.addstr(0, len(header), " " * (max_x - len(header) - 1))
    
    # Display separator
    stdscr.addstr(1, 0, "─" * (max_x - 1))
    
    # Display directory contents with scrolling
    display_count = min(height, len(contents))
    
    for i in range(display_count):
        idx = start_idx + i
        if idx >= len(contents):
            break
            
        name, item_type = contents[idx]
        
        # Determine display style based on type and selection
        if idx == selected_idx:
            attr = curses.color_pair(1) | curses.A_BOLD  # Selected item
        elif item_type == "dir":
            attr = curses.color_pair(2)  # Directory
            name = f"📁 {name}/"
        elif item_type == "py":
            attr = curses.color_pair(3)  # Python file
            name = f"🐍 {name}"
        else:
            attr = curses.color_pair(4)  # Regular file
            name = f"📄 {name}"
        
        # Truncate name if it's too long
        if len(name) > max_x - 4:
            name = name[:max_x - 7] + "..."
            
        # Display item
        stdscr.addstr(i + 2, 2, name, attr)
    
    # Display footer with help
    footer_y = height + 2
    if footer_y < max_y - 1:
        stdscr.addstr(footer_y, 0, "─" * (max_x - 1))
        help_text = " ↑/↓: Navigate | ←: Parent | →/Enter: Select | q: Quit "
        stdscr.addstr(footer_y + 1, 0, help_text, curses.color_pair(5))

def select_directory(start_path: Optional[str] = None) -> Optional[str]:
    """
    Interactive directory selector using curses.
    
    Args:
        start_path: Starting directory path (defaults to current directory)
        
    Returns:
        Selected directory path or None if user cancelled
    """
    if not start_path:
        start_path = os.getcwd()
    
    # Ensure the start path is valid
    try:
        start_path = os.path.abspath(os.path.expanduser(start_path))
        if not os.path.isdir(start_path):
            start_path = os.getcwd()
    except Exception:
        start_path = os.getcwd()
    
    # Function to be called by wrapper
    def _selector(stdscr) -> Optional[str]:
        # Setup
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        stdscr.refresh()
        _setup_colors()
        
        # Initial state
        current_path = start_path
        selected_idx = 0
        start_idx = 0  # For scrolling
        
        # Get window dimensions
        max_y, max_x = stdscr.getmaxyx()
        list_height = max_y - 4  # Space for header, separator, and footer
        
        # Main loop
        while True:
            # Get directory contents
            contents = _get_directory_contents(current_path)
            
            # Adjust indices if needed
            if selected_idx >= len(contents):
                selected_idx = max(0, len(contents) - 1)
            
            # Adjust scroll position if selected item is out of view
            if selected_idx < start_idx:
                start_idx = selected_idx
            elif selected_idx >= start_idx + list_height:
                start_idx = selected_idx - list_height + 1
            
            # Draw the interface
            _draw_directory_contents(
                stdscr, current_path, contents, 
                selected_idx, start_idx, list_height
            )
            stdscr.refresh()
            
            # Handle input
            try:
                key = stdscr.getch()
            except KeyboardInterrupt:
                return None
                
            if key == curses.KEY_UP:
                # Move selection up
                selected_idx = max(0, selected_idx - 1)
            elif key == curses.KEY_DOWN:
                # Move selection down
                selected_idx = min(len(contents) - 1, selected_idx + 1)
            elif key == curses.KEY_LEFT:
                # Go to parent directory
                current_path = os.path.dirname(current_path)
                selected_idx = 0
                start_idx = 0
            elif key == curses.KEY_RIGHT or key == 10 or key == 13:  # Right arrow or Enter
                # Enter directory or select file
                if selected_idx < len(contents):
                    name, item_type = contents[selected_idx]
                    
                    if item_type == "dir":
                        if name == "..":
                            # Go to parent directory
                            current_path = os.path.dirname(current_path)
                        else:
                            # Enter subdirectory
                            current_path = os.path.join(current_path, name)
                        selected_idx = 0
                        start_idx = 0
                    elif item_type == "py":
                        # If it's a python file, select its directory
                        return current_path
            elif key == ord('q') or key == 27:  # 'q' or Escape
                # Cancel
                return None
            elif key == ord('\t'):  # Tab
                # Toggle between file types (dirs, python files, all files)
                pass  # Not implemented in this version
        
        # Should never reach here
        return None
    
    # Use curses wrapper to handle terminal reset on exceptions
    try:
        return curses.wrapper(_selector)
    except Exception as e:
        print(f"Error in directory selector: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    # Test the directory selector
    selected = select_directory()
    if selected:
        print(f"Selected directory: {selected}")
    else:
        print("No directory selected")