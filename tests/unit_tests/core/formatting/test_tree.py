"""Tests for repolyze.core.formatting.tree module."""

from pathlib import Path

from repolyze.core.formatting.tree import render_tree
from repolyze.models import TreeNode


def test_render_tree_single_node():
    """Test rendering a tree with a single node."""
    node = TreeNode(Path("/root"), 0, 0, [])
    result = render_tree(node)
    
    assert result == ["root/"]


def test_render_tree_with_files():
    """Test rendering a tree with files."""
    root = TreeNode(Path("/root"), 0, 0, [
        TreeNode(Path("/root/file1.txt"), 1, 100, []),
        TreeNode(Path("/root/file2.py"), 1, 200, []),
    ])
    
    result = render_tree(root)
    
    assert len(result) == 3
    assert result[0] == "root/"
    assert "file1.txt" in result[1]
    assert "file2.py" in result[2]
    assert "├─ " in result[1]
    assert "└─ " in result[2]


def test_render_tree_with_subdirectories():
    """Test rendering a tree with subdirectories."""
    root = TreeNode(Path("/root"), 0, 0, [
        TreeNode(Path("/root/dir1"), 0, 0, [
            TreeNode(Path("/root/dir1/file.txt"), 1, 100, []),
        ]),
    ])
    
    result = render_tree(root)
    
    assert result[0] == "root/"
    assert "dir1/" in result[1]
    assert "file.txt" in result[2]


def test_render_tree_multiple_levels():
    """Test rendering a tree with multiple levels."""
    root = TreeNode(Path("/root"), 0, 0, [
        TreeNode(Path("/root/file1.txt"), 1, 100, []),
        TreeNode(Path("/root/dir1"), 0, 0, [
            TreeNode(Path("/root/dir1/file2.txt"), 1, 200, []),
            TreeNode(Path("/root/dir1/subdir"), 0, 0, [
                TreeNode(Path("/root/dir1/subdir/file3.txt"), 1, 300, []),
            ]),
        ]),
    ])
    
    result = render_tree(root)
    
    # Check that it has multiple lines
    assert len(result) > 5
    assert result[0] == "root/"
    # Verify file names appear
    assert any("file1.txt" in line for line in result)
    assert any("file2.txt" in line for line in result)
    assert any("file3.txt" in line for line in result)


def test_render_tree_connectors():
    """Test that tree connectors are correct."""
    root = TreeNode(Path("/root"), 0, 0, [
        TreeNode(Path("/root/first.txt"), 1, 100, []),
        TreeNode(Path("/root/second.txt"), 1, 200, []),
    ])
    
    result = render_tree(root)
    
    # First item should use ├─
    assert "├─ first.txt" in result[1]
    # Last item should use └─
    assert "└─ second.txt" in result[2]
