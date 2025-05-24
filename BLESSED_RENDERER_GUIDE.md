# Apollo Blessed Renderer User Guide

## Overview

The enhanced Apollo Blessed Renderer provides a clean, intuitive interface for exploring Python dependency graphs. The messy, scattered display has been completely redesigned into a proper hierarchical tree view with reliable collapsible functionality.

## Interface Layout

### Header Section
```
                    Apollo Dependency Explorer
        Mode: Tree | Total: 15 | Visible: 8 | Selected: 3/8
────────────────────────────────────────────────────────
```

### Tree View (Main Display)
```
 ▶ engine (→12, ←0)
 ▼ games (→8, ←5)
   • __init__.py (←5)
   • exchange_input.py (→1)
   ▶ games.py (→3, ←2)
   • main.py (→2)
   • poker.py (→2, ←1)
 • main.py (→1)
 ▶ tests (→4, ←0)
```

### Footer Controls
```
↑/↓: Navigate | Space: Toggle | Enter: Details | t/d: Views | /: Search | h: Help | q: Quit
```

## Visual Elements

### Tree Symbols
- **▼** - Expanded package (showing contents)
- **▶** - Collapsed package (contents hidden)
- **•** - Individual module/file (leaf node)

### Dependency Indicators
- **(→5, ←3)** - Module has 5 outgoing and 3 incoming dependencies
- **(→2)** - Module has 2 outgoing dependencies only
- **(←4)** - Module has 4 incoming dependencies only

### Color Coding
- **Green** - Few dependencies (≤2) - healthy modules
- **Yellow** - Moderate dependencies (3-5) - watch these
- **Red** - Many dependencies (>5) - potential refactor candidates
- **Gray** - No dependencies - leaf modules
- **Cyan background** - Currently selected item

## Navigation Controls

### Basic Movement
- **↑/↓** - Move selection up/down through visible items
- **Home** - Jump to first item
- **End** - Jump to last item
- **PgUp/PgDn** - Fast scroll (10 items at a time)

### Tree Operations
- **Space** - Toggle expand/collapse of selected package
- **→** - Expand selected package (if collapsed)
- **←** - Collapse selected package (if expanded)
- **Enter** - Switch to dependencies view for selected module

### View Modes
- **t** - Tree view (hierarchical package display)
- **d** - Dependencies view (detailed analysis of selected module)

### Search and Utilities
- **/** - Enter search mode (type to filter modules)
- **Esc** - Clear search and return to full view
- **h** - Toggle help display on/off
- **q** - Quit application

## Using the Tree View

### Exploring Package Structure
1. **Start with collapsed packages** - Use ▶ symbols to see package overview
2. **Expand interesting packages** - Press Space or → on packages with many dependencies
3. **Navigate efficiently** - Use the tree structure to understand project organization
4. **Focus on problem areas** - Look for red-colored modules with many dependencies

### Understanding Dependencies
- **High outgoing (→)** - Module imports many things, might be doing too much
- **High incoming (←)** - Module is heavily used, core to the project
- **Balanced counts** - Healthy module with reasonable coupling
- **Zero dependencies** - Standalone utility or leaf module

### Collapsing for Clarity
When you have a large project:
1. Keep most packages collapsed initially
2. Expand only the packages you're investigating
3. Use search (/) to quickly find specific modules
4. Collapse packages when done to reduce visual clutter

## Dependencies View

Press **Enter** on any module to see detailed dependency information:

```
 Module: games.poker

 Dependencies (imports):
   → engine.deck
   → engine.hand
   → random

 Used by:
   ← games.main
   ← tests.test_poker
```

### Information Shown
- **Full module path** - Complete name and location
- **Dependencies section** - What this module imports
- **Used by section** - What modules import this one
- **Truncation** - Lists up to 15 items, shows "... and X more" if needed

## Search Functionality

### Entering Search Mode
1. Press **/** to enter search mode
2. Type your search term (searches module names)
3. Results filter in real-time as you type
4. Press **Enter** to confirm search
5. Press **Esc** to cancel and clear search

### Search Behavior
- **Case insensitive** - "POKER" matches "poker.py"
- **Partial matching** - "test" matches "test_poker.py", "tests.py"
- **Live filtering** - Tree updates immediately as you type
- **Maintains structure** - Filtered results keep tree hierarchy

## Keyboard Shortcuts Summary

```
Movement:      ↑↓ Navigate    Home/End Jump    PgUp/PgDn Fast scroll
Tree Control:  Space Toggle   ←→ Collapse/Expand    Enter Details
Views:         t Tree view    d Dependencies view
Utility:       / Search      Esc Clear search    h Help    q Quit
```

## Troubleshooting

### Display Issues
- **Scattered text** - This has been fixed in the new version
- **Misaligned tree** - Restart the application if you see formatting issues
- **Missing colors** - Ensure your terminal supports ANSI colors

### Navigation Problems
- **Can't collapse** - Make sure you're on a package (▼/▶) not a file (•)
- **Nothing happens on Space** - Files can't be collapsed, only packages can
- **Selection jumps around** - Fixed in new version with proper scroll management

### Terminal Requirements
- **Minimum size** - 50 columns by 10 rows (reduced from previous 60x15)
- **Color support** - Terminal must support ANSI color codes
- **Key support** - Arrow keys, Space, Enter must work properly

## Tips for Effective Use

### Project Analysis Workflow
1. **Start with tree view** - Get overview of project structure
2. **Look for red modules** - These have many dependencies and need attention
3. **Expand suspicious packages** - Investigate areas with high coupling
4. **Use dependencies view** - Understand specific relationships
5. **Search for patterns** - Find all test files, utils, etc.

### Performance Tips
- **Keep packages collapsed** when not actively investigating them
- **Use search** to narrow focus in very large projects
- **Navigate with PgUp/PgDn** for fast movement through long lists

### Understanding Your Codebase
- **Package organization** - Tree view shows if modules are logically grouped
- **Dependency direction** - Incoming arrows show which modules are core utilities
- **Coupling levels** - Color coding highlights modules that might need refactoring
- **Circular dependencies** - Look for modules that both import each other

The improved blessed renderer now provides a clean, professional interface that makes dependency analysis intuitive and efficient, with reliable collapsing functionality and proper tree navigation.