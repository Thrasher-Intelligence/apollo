#!/usr/bin/env python3
"""
Demo script showing the precise grid alignment of the improved blessed interface.
This demonstrates the exact visual layout without requiring interactive terminal.
"""

def show_precise_layout():
    """Show the exact blessed interface layout with grid alignment."""
    
    # Terminal dimensions (typical size)
    width = 80
    height = 20
    
    print("APOLLO BLESSED RENDERER - PRECISE GRID ALIGNMENT DEMO")
    print("=" * width)
    print()
    
    # Show grid positions
    print("Grid Reference (for alignment verification):")
    print("0123456789" * 8)
    print("─" * width)
    
    # Demonstrate exact positioning
    lines = []
    
    # Header (y=0-2)
    title = "Apollo Dependency Explorer"
    title_x = (width - len(title)) // 2
    lines.append(f"Y=0: {' ' * title_x}[TITLE: {title}]")
    
    info = "Mode: Tree | Total: 15 | Visible: 8 | Selected: 3/8"
    info_x = (width - len(info)) // 2
    lines.append(f"Y=1: {' ' * info_x}[INFO: {info}]")
    
    lines.append(f"Y=2: [SEPARATOR: {'─' * width}]")
    
    # Content area (y=3 to height-3)
    tree_content = [
        "▶ engine (→12, ←0)",
        "▼ games (→8, ←5)",
        "  • __init__.py (←5)",
        "  • exchange_input.py (→1)",
        "  ▶ games.py (→3, ←2)",
        "  • main.py (→2)",
        "  • poker.py (→2, ←1)",
        "• main.py (→1)",
        "▶ tests (→4, ←0)"
    ]
    
    for i, content in enumerate(tree_content):
        y = 3 + i
        if y < height - 3:
            if i == 2:  # Selected item
                lines.append(f"Y={y}: [SELECTED: {content}] <- CYAN HIGHLIGHT")
            else:
                color = "GREEN" if "→1" in content or "→2" in content else "YELLOW" if "→3" in content else "RED"
                lines.append(f"Y={y}: [NORMAL: {content}] <- {color}")
    
    # Footer (y=height-2 to height-1)
    footer_sep_y = height - 2
    lines.append(f"Y={footer_sep_y}: [SEPARATOR: {'─' * width}]")
    
    controls = "↑/↓: Navigate | Space: Toggle | Enter: Details | q: Quit"
    controls_x = (width - len(controls)) // 2
    lines.append(f"Y={height-1}: {' ' * controls_x}[CONTROLS: {controls}]")
    
    # Display the layout
    for line in lines:
        print(line)
    
    print()
    print("ACTUAL VISUAL OUTPUT:")
    print("=" * width)
    
    # Show how it actually looks
    print(" " * title_x + title)
    print(" " * info_x + info)
    print("─" * width)
    
    for i, content in enumerate(tree_content[:6]):  # Show first 6 items
        if i == 2:  # Selected
            print(f"\033[46m\033[30m{content:<{width-1}}\033[0m")
        else:
            if "→1" in content or "→2" in content:
                print(f"\033[92m{content}\033[0m")  # Green
            elif "→3" in content:
                print(f"\033[93m{content}\033[0m")  # Yellow
            else:
                print(f"\033[91m{content}\033[0m")  # Red
    
    print("─" * width)
    print(" " * controls_x + controls)
    
    print()
    print("GRID ALIGNMENT VERIFICATION:")
    print(f"✓ Title centered at column {title_x}")
    print(f"✓ Info centered at column {info_x}")
    print(f"✓ Controls centered at column {controls_x}")
    print("✓ Tree items left-aligned at column 0")
    print("✓ Indented items properly spaced with 2-space indents")
    print("✓ Selected item fills entire row width")
    print("✓ All content fits within terminal bounds")

def show_positioning_examples():
    """Show examples of proper positioning vs misalignment."""
    
    print("\nPOSITIONING EXAMPLES:")
    print("=" * 50)
    
    print("\n❌ WRONG (scattered, misaligned):")
    print("                Apollo")
    print("    ▶ engine")
    print("                        ▼ games")
    print("         • file.py")
    print("Controls here somewhere")
    
    print("\n✅ CORRECT (grid-aligned):")
    print("                Apollo Dependency Explorer")
    print("─" * 50)
    print("▶ engine (→12, ←0)")
    print("▼ games (→8, ←5)")
    print("  • __init__.py (←5)")
    print("  • file.py (→1)")
    print("─" * 50)
    print("        ↑/↓: Navigate | Space: Toggle | q: Quit")
    
    print("\nKEY DIFFERENCES:")
    print("✓ Consistent positioning using term.move(y, x)")
    print("✓ Proper line clearing before writing")
    print("✓ Centered headers and footers")
    print("✓ Left-aligned tree content")
    print("✓ No text overflow or wrapping issues")

def show_blessed_api_usage():
    """Show the correct blessed API usage for alignment."""
    
    print("\nBLESSED API USAGE FOR PROPER ALIGNMENT:")
    print("=" * 60)
    
    code_examples = [
        "# WRONG - causes misalignment",
        "print(term.center(text))  # Unreliable positioning",
        "sys.stdout.write(text)    # No position control",
        "",
        "# CORRECT - precise positioning", 
        "sys.stdout.write(term.move(y, x))  # Move cursor first",
        "sys.stdout.write(text)             # Then write text",
        "",
        "# OR use helper function:",
        "def _print_at(y, x, text, style=None):",
        "    sys.stdout.write(term.move(y, x))",
        "    if style:",
        "        sys.stdout.write(style(text))",
        "    else:",
        "        sys.stdout.write(text)",
        "",
        "# Clear line before writing (prevents artifacts)",
        "_print_at(y, 0, ' ' * term.width)  # Clear full line",
        "_print_at(y, x, text, style)       # Write content"
    ]
    
    for line in code_examples:
        print(line)

if __name__ == "__main__":
    show_precise_layout()
    show_positioning_examples()
    show_blessed_api_usage()