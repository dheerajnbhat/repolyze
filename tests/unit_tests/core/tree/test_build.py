"""Tests for repolyze.core.tree.build module."""

import pytest

from repolyze.core.tree.build import build_tree, _load_gitignore, _matches_gitignore


def test_build_tree_empty_directory(tmp_path):
    """Test building tree from empty directory."""
    tree = build_tree(tmp_path)
    
    assert tree.path == tmp_path
    assert tree.children == []


def test_build_tree_with_files(tmp_path):
    """Test building tree with files."""
    (tmp_path / "file1.txt").write_text("content")
    (tmp_path / "file2.py").write_text("code")
    
    tree = build_tree(tmp_path)
    
    assert len(tree.children) == 2
    child_names = [child.path.name for child in tree.children]
    assert "file1.txt" in child_names
    assert "file2.py" in child_names


def test_build_tree_with_subdirectories(tmp_path):
    """Test building tree with subdirectories."""
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file.txt").touch()
    (tmp_path / "dir2").mkdir()
    
    tree = build_tree(tmp_path)
    
    assert len(tree.children) == 2
    # Find dir1 and check its children
    dir1 = next(c for c in tree.children if c.path.name == "dir1")
    assert len(dir1.children) == 1
    assert dir1.children[0].path.name == "file.txt"


def test_build_tree_skips_skip_dirs(tmp_path):
    """Test that build_tree skips directories in SKIP_DIRS."""
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").touch()
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "normal").mkdir()
    (tmp_path / "normal" / "file.txt").touch()
    
    tree = build_tree(tmp_path)
    
    child_names = [child.path.name for child in tree.children]
    assert ".git" not in child_names
    assert "__pycache__" not in child_names
    assert "normal" in child_names


def test_build_tree_respects_gitignore(tmp_path):
    """Test that build_tree respects .gitignore patterns."""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.log\ntemp/\n")
    
    (tmp_path / "file.txt").touch()
    (tmp_path / "file.log").touch()
    (tmp_path / "temp").mkdir()
    
    tree = build_tree(tmp_path)
    
    child_names = [child.path.name for child in tree.children]
    assert "file.txt" in child_names
    assert "file.log" not in child_names
    assert "temp" not in child_names


def test_build_tree_skips_symlinks(tmp_path):
    """Test that build_tree skips symlinks."""
    (tmp_path / "real_file.txt").touch()
    (tmp_path / "real_dir").mkdir()
    
    # Create symlinks - skip test on Windows if privileges are insufficient
    try:
        (tmp_path / "link_to_file").symlink_to(tmp_path / "real_file.txt")
        (tmp_path / "link_to_dir").symlink_to(tmp_path / "real_dir")
    except OSError as e:
        # Windows requires admin privileges for symlinks
        pytest.skip(f"Cannot create symlinks: {e}")
    
    tree = build_tree(tmp_path)
    
    child_names = [child.path.name for child in tree.children]
    assert "real_file.txt" in child_names
    assert "real_dir" in child_names
    assert "link_to_file" not in child_names
    assert "link_to_dir" not in child_names


def test_load_gitignore_from_build(tmp_path):
    """Test _load_gitignore function."""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.pyc\n# comment\nbuild/\n")
    
    patterns = _load_gitignore(tmp_path)
    
    assert patterns == ["*.pyc", "build/"]


def test_matches_gitignore_from_build():
    """Test _matches_gitignore function."""
    patterns = ["*.log", "temp/"]
    
    assert _matches_gitignore("file.log", patterns, is_dir=False)
    assert _matches_gitignore("temp", patterns, is_dir=True)
    assert not _matches_gitignore("file.txt", patterns, is_dir=False)
