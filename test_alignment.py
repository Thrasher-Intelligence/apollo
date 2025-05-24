#!/usr/bin/env python3
"""
Test script to verify blessed renderer alignment and positioning.
This tests the visual alignment without requiring full interactive mode.
"""

import sys
import os

def test_alignment():
    """Test the alignment functionality of the blessed renderer."""
    
    try:
        from blessed import Terminal
    except ImportError:
        print("blessed library not available, skipping alignment test")
        return
    
    # Initialize terminal
    term = Terminal()
    
    print("Testing blessed renderer alignment...")
    print(f"Terminal size: {term.width}x{term.height}")
    print()
    
    # Test basic positioning
    print("Testing basic positioning:")
    
    # Simulate the header
    title = "Apollo Dependency Explorer"
    title_x = (term.width - len(title)) // 2
    print(f"Title position: x={title_x}, width={len(title)}")
    print(f"Centered title: '{title}'")
    print(" " * title_x + title)
    print()
    
    # Test tree alignment
    print("Testing tree alignment:")
    tree_items = [
        "▶ engine (→12, ←0)",
        "▼ games (→8, ←5)",
        "  • __init__.py (←5)",
        "  • exchange_input.py (→1)",
        "  ▶ games.py (→3, ←2)",
        "• main.py (→1)"
    ]
    
    for item in tree_items:
        print(f"'{item}'")
    print()
    
    # Test footer alignment
    print("Testing footer alignment:")
    controls = "↑/↓: Navigate | Space: Toggle | Enter: Details | q: Quit"
    controls_x = (term.width - len(controls)) // 2
    print(f"Controls position: x={controls_x}, width={len(controls)}")
    print(" " * controls_x + controls)
    print()
    
    # Test positioning boundaries
    print("Testing positioning boundaries:")
    print(f"Safe content area: x=0 to {term.width-1}, y=3 to {term.height-3}")
    print(f"Header area: y=0 to 2")
    print(f"Footer area: y={term.height-2} to {term.height-1}")
    print()
    
    # Test text truncation
    print("Testing text truncation:")
    long_text = "This is a very long line that might exceed terminal width and needs to be truncated properly"
    max_width = term.width - 4  # Leave some margin
    if len(long_text) > max_width:
        truncated = long_text[:max_width-3] + "..."
        print(f"Original: {len(long_text)} chars")
        print(f"Truncated: {len(truncated)} chars")
        print(f"Result: '{truncated}'")
    else:
        print(f"Text fits: '{long_text}'")
    
    print("\nAlignment test completed successfully!")

def test_blessed_renderer_components():
    """Test individual blessed renderer components."""
    
    try:
        from modules.renderers import BlessedRenderer
        from modules.core import DependencyAnalyzer
    except ImportError as e:
        print(f"Cannot import required modules: {e}")
        return
    
    print("\nTesting blessed renderer components...")
    
    # Create test data
    analyzer = DependencyAnalyzer()
    renderer = BlessedRenderer()
    
    try:
        # Test with current directory
        analyzer.set_target_directory('.')
        analyzer.find_python_files()
        graph = analyzer.build_dependency_graph()
        
        # Test tree building
        tree_root = renderer._build_tree_structure(graph)
        renderer.tree_root = tree_root
        renderer._update_visible_nodes()
        
        print(f"✓ Tree structure: {len(tree_root.children)} packages")
        print(f"✓ Visible nodes: {len(renderer.visible_nodes)}")
        
        # Test positioning function
        if hasattr(renderer, '_print_at'):
            print("✓ Position function available")
        else:
            print("✗ Position function missing")
        
        # Test node selection
        if renderer.visible_nodes:
            test_node = renderer.visible_nodes[0]
            print(f"✓ Test node: {test_node.name} (level {test_node.level})")
            print(f"  Can expand: {test_node.can_expand()}")
            print(f"  Dependencies: →{len(test_node.outgoing_deps)}, ←{len(test_node.incoming_deps)}")
        
        print("✓ Component test passed")
        
    except Exception as e:
        print(f"✗ Component test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_alignment()
    test_blessed_renderer_components()