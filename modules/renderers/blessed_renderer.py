"""
Blessed renderer for Apollo Python Dependency Analyzer.
Fixed visual alignment with proper terminal positioning.
"""

import os
import sys
import time
from typing import Dict, Set, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from .base_renderer import BaseRenderer
from ..exceptions import RenderingError


class NodeState(Enum):
    """States for tree nodes"""
    COLLAPSED = "collapsed"
    EXPANDED = "expanded"
    LEAF = "leaf"


class ViewMode(Enum):
    """Different view modes for the renderer"""
    TREE = "tree"
    DEPENDENCIES = "dependencies"


@dataclass
class TreeNode:
    """Represents a node in the dependency tree"""
    name: str
    full_name: str
    children: List['TreeNode']
    incoming_deps: List[str]
    outgoing_deps: List[str]
    state: NodeState = NodeState.COLLAPSED
    level: int = 0
    parent: Optional['TreeNode'] = None

    def toggle(self):
        """Toggle between expanded and collapsed states"""
        if self.state == NodeState.COLLAPSED:
            self.state = NodeState.EXPANDED
        elif self.state == NodeState.EXPANDED:
            self.state = NodeState.COLLAPSED

    def can_expand(self) -> bool:
        """Check if this node can be expanded"""
        return len(self.children) > 0


class BlessedRenderer(BaseRenderer):
    """Enhanced interactive blessed-based renderer with proper alignment."""
    
    def __init__(self):
        """Initialize the blessed renderer."""
        super().__init__()
        self.term: Optional[Any] = None
        self.original_stty: Optional[str] = None
        self.tree_root: Optional[TreeNode] = None
        self.flat_nodes: List[TreeNode] = []
        self.visible_nodes: List[TreeNode] = []
        self.selected_index: int = 0
        self.scroll_offset: int = 0
        self.view_mode: ViewMode = ViewMode.TREE
        self.search_query: str = ""
        self.show_help: bool = False
    
    def get_renderer_type(self) -> str:
        """Get the renderer type identifier."""
        return "blessed"
    
    def _import_blessed(self) -> Any:
        """Import blessed library with error handling."""
        try:
            from blessed import Terminal
            return Terminal
        except ImportError:
            raise RenderingError(
                "blessed",
                "'blessed' library is required for TUI rendering. Install it using: pip install blessed"
            )
    
    def _initialize_terminal(self) -> Any:
        """Initialize the terminal with proper settings."""
        Terminal = self._import_blessed()
        
        try:
            term = Terminal()
        except Exception as e:
            raise RenderingError("blessed", f"Error initializing terminal: {str(e)}")
        
        os.environ.setdefault('ESCDELAY', '25')
        
        if not term.is_a_tty or term.height < 10 or term.width < 50:
            raise RenderingError(
                "blessed",
                f"Terminal too small. Minimum size: 50x10, current: {term.width}x{term.height}"
            )
        
        return term
    
    def _setup_terminal(self):
        """Setup terminal for interactive mode."""
        if not self.term:
            return
            
        try:
            self.original_stty = os.popen('stty -g').read().strip()
        except Exception:
            pass
        
        os.system('stty raw -echo')
        sys.stdout.write(self.term.enter_fullscreen)
        sys.stdout.write(self.term.hide_cursor)
        sys.stdout.flush()
    
    def _cleanup_terminal(self):
        """Restore terminal to original state."""
        try:
            if self.original_stty:
                os.system(f'stty {self.original_stty}')
            else:
                os.system('stty sane')
        except Exception:
            try:
                os.system('stty sane')
            except Exception:
                pass
        
        try:
            if self.term:
                sys.stdout.write(self.term.exit_fullscreen)
                sys.stdout.write(self.term.show_cursor)
                sys.stdout.write(self.term.clear)
                sys.stdout.flush()
        except Exception:
            print("\033[?25h", end='', flush=True)
    
    def _build_tree_structure(self, graph: Dict[str, Set[str]]) -> TreeNode:
        """Build a hierarchical tree structure from the dependency graph."""
        all_modules = self.get_all_modules(graph)
        
        # Create nodes for all modules
        nodes = {}
        for module in sorted(all_modules):
            outgoing = list(graph.get(module, set()))
            incoming = [m for m, deps in graph.items() if module in deps]
            
            # Create a simple display name
            display_name = module.split('.')[-1] if '.' in module else module
            
            nodes[module] = TreeNode(
                name=display_name,
                full_name=module,
                children=[],
                incoming_deps=incoming,
                outgoing_deps=outgoing,
                state=NodeState.LEAF
            )
        
        # Build simple flat structure grouped by package prefix
        packages = {}
        root_nodes = []
        
        for module_name, node in nodes.items():
            parts = module_name.split('.')
            
            if len(parts) == 1:
                # Top-level module
                root_nodes.append(node)
            else:
                # Group by first part
                package_name = parts[0]
                if package_name not in packages:
                    # Create package node
                    package_node = TreeNode(
                        name=package_name,
                        full_name=package_name,
                        children=[],
                        incoming_deps=[],
                        outgoing_deps=[],
                        state=NodeState.COLLAPSED
                    )
                    packages[package_name] = package_node
                    root_nodes.append(package_node)
                
                # Add to package
                package_node = packages[package_name]
                node.parent = package_node
                node.level = 1
                package_node.children.append(node)
        
        # Create virtual root
        root = TreeNode(
            name="Dependencies",
            full_name="__root__",
            children=sorted(root_nodes, key=lambda x: x.name),
            incoming_deps=[],
            outgoing_deps=[],
            state=NodeState.EXPANDED,
            level=-1
        )
        
        for child in root.children:
            child.parent = root
            if child.level == 0:
                child.level = 0
        
        return root
    
    def _flatten_visible_nodes(self, node: TreeNode, result: List[TreeNode]) -> None:
        """Recursively flatten tree into visible nodes list."""
        if node.full_name != "__root__":
            result.append(node)
        
        if node.state == NodeState.EXPANDED:
            for child in sorted(node.children, key=lambda x: x.name):
                self._flatten_visible_nodes(child, result)
    
    def _update_visible_nodes(self):
        """Update the list of visible nodes based on current tree state."""
        self.visible_nodes = []
        if self.tree_root:
            self._flatten_visible_nodes(self.tree_root, self.visible_nodes)
        
        # Apply search filter if active
        if self.search_query:
            query_lower = self.search_query.lower()
            self.visible_nodes = [
                node for node in self.visible_nodes
                if query_lower in node.full_name.lower() or query_lower in node.name.lower()
            ]
    
    def _get_selected_node(self) -> Optional[TreeNode]:
        """Get the currently selected node."""
        if 0 <= self.selected_index < len(self.visible_nodes):
            return self.visible_nodes[self.selected_index]
        return None
    
    def _print_at(self, y: int, x: int, text: str, style=None):
        """Print text at specific position with proper alignment."""
        if not self.term:
            return
        
        # Ensure we stay within terminal bounds
        if y < 0 or y >= self.term.height or x < 0:
            return
        
        # Truncate text if it would exceed terminal width
        max_width = self.term.width - x
        if len(text) > max_width:
            text = text[:max_width]
        
        # Move cursor and print
        sys.stdout.write(self.term.move(y, x))
        if style:
            sys.stdout.write(style(text))
        else:
            sys.stdout.write(text)
    
    def _render_tree_view(self):
        """Render the main tree view with proper positioning."""
        if not self.term:
            return
        
        content_start_y = 3  # Start after header
        max_visible = self.term.height - 6  # Reserve space for header/footer
        start_idx = self.scroll_offset
        end_idx = min(start_idx + max_visible, len(self.visible_nodes))
        
        current_y = content_start_y
        
        for i in range(start_idx, end_idx):
            if i >= len(self.visible_nodes) or current_y >= self.term.height - 3:
                break
                
            node = self.visible_nodes[i]
            is_selected = (i == self.selected_index)
            
            # Build indentation based on level
            indent = "  " * node.level
            
            # Add expand/collapse indicator
            if node.can_expand():
                if node.state == NodeState.EXPANDED:
                    indicator = "▼ "
                else:
                    indicator = "▶ "
            else:
                indicator = "• "
            
            # Build the main text
            text = f"{indent}{indicator}{node.name}"
            
            # Add dependency counts
            out_count = len(node.outgoing_deps)
            in_count = len(node.incoming_deps)
            
            if out_count > 0 or in_count > 0:
                counts = []
                if out_count > 0:
                    counts.append(f"→{out_count}")
                if in_count > 0:
                    counts.append(f"←{in_count}")
                text += f" ({', '.join(counts)})"
            
            # Apply colors and selection
            if is_selected:
                # Clear the entire line first
                self._print_at(current_y, 0, " " * self.term.width)
                # Print selected item with highlight
                self._print_at(current_y, 0, text, self.term.black_on_cyan)
            else:
                # Clear the line first
                self._print_at(current_y, 0, " " * self.term.width)
                # Color based on dependency count
                if out_count == 0 and in_count == 0:
                    style = self.term.bright_black
                elif out_count > 5:
                    style = self.term.red
                elif out_count > 2:
                    style = self.term.yellow
                else:
                    style = self.term.green
                
                self._print_at(current_y, 0, text, style)
            
            current_y += 1
    
    def _render_dependency_view(self):
        """Render detailed dependency view for selected node."""
        if not self.term:
            return
        
        node = self._get_selected_node()
        if not node:
            self._print_at(4, 2, "No module selected.")
            return
        
        current_y = 4
        self._print_at(current_y, 2, f"Module: {node.full_name}", self.term.bold_cyan)
        current_y += 2
        
        # Show outgoing dependencies
        if node.outgoing_deps:
            self._print_at(current_y, 2, "Dependencies (imports):", self.term.green)
            current_y += 1
            for dep in node.outgoing_deps[:15]:
                if current_y >= self.term.height - 3:
                    break
                self._print_at(current_y, 4, f"→ {dep}", self.term.green)
                current_y += 1
            if len(node.outgoing_deps) > 15:
                self._print_at(current_y, 4, f"... and {len(node.outgoing_deps) - 15} more", self.term.bright_black)
                current_y += 1
            current_y += 1
        
        # Show incoming dependencies
        if node.incoming_deps:
            self._print_at(current_y, 2, "Used by:", self.term.magenta)
            current_y += 1
            for dep in node.incoming_deps[:15]:
                if current_y >= self.term.height - 3:
                    break
                self._print_at(current_y, 4, f"← {dep}", self.term.magenta)
                current_y += 1
            if len(node.incoming_deps) > 15:
                self._print_at(current_y, 4, f"... and {len(node.incoming_deps) - 15} more", self.term.bright_black)
                current_y += 1
        
        if not node.outgoing_deps and not node.incoming_deps:
            self._print_at(current_y, 2, "No dependencies found.", self.term.bright_black)
    
    def _render_header(self):
        """Render the application header."""
        if not self.term:
            return
        
        # Clear header area
        for y in range(3):
            self._print_at(y, 0, " " * self.term.width)
        
        title = "Apollo Dependency Explorer"
        title_x = (self.term.width - len(title)) // 2
        self._print_at(0, title_x, title, self.term.white_on_blue)
        
        # Show current mode and stats
        mode_text = f"Mode: {self.view_mode.value.title()}"
        if self.search_query:
            mode_text += f" | Search: '{self.search_query}'"
        
        stats_text = f"Total: {len(self.flat_nodes)} | Visible: {len(self.visible_nodes)}"
        if self.visible_nodes:
            stats_text += f" | Selected: {self.selected_index + 1}/{len(self.visible_nodes)}"
        
        info_line = f"{mode_text} | {stats_text}"
        info_x = (self.term.width - len(info_line)) // 2
        self._print_at(1, info_x, info_line)
        
        # Separator line
        self._print_at(2, 0, "─" * self.term.width)
    
    def _render_footer(self):
        """Render the help footer."""
        if not self.term:
            return
        
        footer_y = self.term.height - 2
        
        # Clear footer area
        self._print_at(footer_y, 0, "─" * self.term.width)
        
        if self.show_help:
            help_lines = [
                "↑/↓: Navigate | Space/Enter: Toggle/Expand | ←: Collapse | →: Expand",
                "t: Tree View | d: Dependencies View | /: Search | Esc: Clear Search",
                "PgUp/PgDn: Fast Scroll | Home/End: Jump | h: Help | q: Quit"
            ]
            for i, line in enumerate(help_lines):
                if footer_y + 1 + i < self.term.height:
                    line_x = (self.term.width - len(line)) // 2
                    self._print_at(footer_y + 1 + i, line_x, line, self.term.bright_black)
        else:
            controls = "↑/↓: Navigate | Space: Toggle | Enter: Details | t/d: Views | /: Search | h: Help | q: Quit"
            controls_x = (self.term.width - len(controls)) // 2
            self._print_at(footer_y + 1, controls_x, controls, self.term.bright_black)
    
    def _handle_search_input(self, key) -> bool:
        """Handle search input mode."""
        if key.name == 'KEY_ESCAPE':
            self.search_query = ""
            return True
        elif key.name == 'KEY_ENTER':
            return True
        elif key.name == 'KEY_BACKSPACE':
            if self.search_query:
                self.search_query = self.search_query[:-1]
        elif key and len(key) == 1 and key.isprintable():
            self.search_query += key
        
        self._update_visible_nodes()
        self.selected_index = 0
        self.scroll_offset = 0
        return False
    
    def _adjust_scroll(self):
        """Adjust scroll offset to keep selected item visible."""
        if not self.term:
            return
        
        max_visible = self.term.height - 6
        
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + max_visible:
            self.scroll_offset = self.selected_index - max_visible + 1
    
    def _handle_input(self) -> bool:
        """Handle keyboard input and return True if should exit."""
        if not self.term:
            return True
        
        try:
            key = self.term.inkey(timeout=0.1)
        except Exception:
            return True
        
        if not key:
            return False
        
        # Global commands
        if key.lower() == 'q':
            return True
        elif key.lower() == 'h':
            self.show_help = not self.show_help
            return False
        elif key == '/':
            # Enter search mode
            while True:
                sys.stdout.write(self.term.clear)
                sys.stdout.flush()
                search_prompt = f"Search: {self.search_query}_"
                search_x = (self.term.width - len(search_prompt)) // 2
                self._print_at(self.term.height // 2, search_x, search_prompt)
                self._print_at(self.term.height // 2 + 1, (self.term.width - 40) // 2, "(Type to search, Enter to confirm, Esc to cancel)")
                sys.stdout.flush()
                
                search_key = self.term.inkey()
                if self._handle_search_input(search_key):
                    break
            return False
        elif key.name == 'KEY_ESCAPE':
            self.search_query = ""
            self._update_visible_nodes()
            return False
        
        # View mode switches
        elif key.lower() == 't':
            self.view_mode = ViewMode.TREE
            return False
        elif key.lower() == 'd':
            self.view_mode = ViewMode.DEPENDENCIES
            return False
        
        # Navigation
        elif key.name == 'KEY_UP':
            self.selected_index = max(0, self.selected_index - 1)
            self._adjust_scroll()
        elif key.name == 'KEY_DOWN':
            self.selected_index = min(len(self.visible_nodes) - 1, self.selected_index + 1)
            self._adjust_scroll()
        elif key.name == 'KEY_HOME':
            self.selected_index = 0
            self.scroll_offset = 0
        elif key.name == 'KEY_END':
            self.selected_index = max(0, len(self.visible_nodes) - 1)
            self._adjust_scroll()
        elif key.name == 'KEY_PGUP':
            self.selected_index = max(0, self.selected_index - 10)
            self._adjust_scroll()
        elif key.name == 'KEY_PGDN':
            self.selected_index = min(len(self.visible_nodes) - 1, self.selected_index + 10)
            self._adjust_scroll()
        
        # Tree operations
        elif key == ' ' or key.name == 'KEY_ENTER':
            node = self._get_selected_node()
            if node and node.can_expand():
                node.toggle()
                self._update_visible_nodes()
        elif key.name == 'KEY_RIGHT':
            node = self._get_selected_node()
            if node and node.can_expand() and node.state == NodeState.COLLAPSED:
                node.state = NodeState.EXPANDED
                self._update_visible_nodes()
        elif key.name == 'KEY_LEFT':
            node = self._get_selected_node()
            if node and node.can_expand() and node.state == NodeState.EXPANDED:
                node.state = NodeState.COLLAPSED
                self._update_visible_nodes()
        
        return False
    
    def render(self, graph: Dict[str, Set[str]]) -> Optional[str]:
        """Render the dependency graph using enhanced blessed TUI."""
        if not self.validate_graph(graph):
            raise RenderingError("blessed", "Invalid graph format")
        
        if not graph:
            print("No dependencies found.")
            return None
        
        # Initialize terminal
        self.term = self._initialize_terminal()
        
        # Build tree structure
        self.tree_root = self._build_tree_structure(graph)
        self.flat_nodes = []
        self._flatten_visible_nodes(self.tree_root, self.flat_nodes)
        self._update_visible_nodes()
        
        try:
            self._setup_terminal()
            
            # Main rendering loop
            while True:
                # Clear screen
                sys.stdout.write(self.term.clear)
                sys.stdout.flush()
                
                # Render components
                self._render_header()
                
                if self.view_mode == ViewMode.DEPENDENCIES:
                    self._render_dependency_view()
                else:
                    self._render_tree_view()
                
                self._render_footer()
                
                # Flush output
                sys.stdout.flush()
                
                if self._handle_input():
                    break
        
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self._cleanup_terminal()
            raise RenderingError("blessed", f"Blessed visualization failed: {str(e)}")
        finally:
            self._cleanup_terminal()
        
        return None