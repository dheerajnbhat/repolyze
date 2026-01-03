"""Tests for repolyze.core.filesystem.scan module."""


from repolyze.core.filesystem.scan import scan, _load_gitignore, _matches_gitignore


def test_scan_empty_directory(tmp_path):
    """Test scanning an empty directory."""
    result = list(scan(tmp_path))
    assert result == []


def test_scan_with_files(tmp_path):
    """Test scanning directory with files."""
    (tmp_path / "file1.txt").touch()
    (tmp_path / "file2.py").touch()
    
    result = list(scan(tmp_path))
    assert len(result) == 2
    assert tmp_path / "file1.txt" in result
    assert tmp_path / "file2.py" in result


def test_scan_with_subdirectories(tmp_path):
    """Test scanning directory with subdirectories."""
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.txt").touch()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "file2.txt").touch()
    
    result = list(scan(tmp_path))
    assert len(result) == 4  # 2 dirs + 2 files
    assert tmp_path / "dir1" in result
    assert tmp_path / "dir2" in result


def test_scan_skips_skip_dirs(tmp_path):
    """Test that scan skips directories in SKIP_DIRS."""
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").touch()
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "cache.pyc").touch()
    (tmp_path / "normal").mkdir()
    (tmp_path / "normal" / "file.txt").touch()
    
    result = list(scan(tmp_path))
    # Should only include normal dir and file
    assert len(result) == 2
    assert tmp_path / "normal" in result
    assert tmp_path / "normal" / "file.txt" in result


def test_scan_respects_gitignore(tmp_path):
    """Test that scan respects .gitignore patterns."""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.log\ntemp/\n")
    
    (tmp_path / "file.txt").touch()
    (tmp_path / "file.log").touch()
    (tmp_path / "temp").mkdir()
    (tmp_path / "temp" / "file.txt").touch()
    
    result = list(scan(tmp_path))
    result_names = [p.name for p in result]
    
    # file.txt should be included, file.log and temp should be excluded
    assert "file.txt" in result_names
    assert "file.log" not in result_names
    assert "temp" not in result_names


def test_load_gitignore_not_exists(tmp_path):
    """Test loading .gitignore when it doesn't exist."""
    result = _load_gitignore(tmp_path)
    assert result is None


def test_load_gitignore_exists(tmp_path):
    """Test loading .gitignore when it exists."""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.log\n# comment\ntemp/\n\n")
    
    result = _load_gitignore(tmp_path)
    assert result == ["*.log", "temp/"]


def test_load_gitignore_empty(tmp_path):
    """Test loading empty .gitignore."""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("# only comments\n\n")
    
    result = _load_gitignore(tmp_path)
    assert result is None


def test_matches_gitignore_simple_pattern():
    """Test gitignore pattern matching with simple patterns."""
    patterns = ["*.log", "temp.txt"]
    
    assert _matches_gitignore("file.log", patterns, is_dir=False)
    assert _matches_gitignore("temp.txt", patterns, is_dir=False)
    assert not _matches_gitignore("file.txt", patterns, is_dir=False)


def test_matches_gitignore_directory_pattern():
    """Test gitignore pattern matching with directory patterns."""
    patterns = ["build/", "*.pyc"]
    
    assert _matches_gitignore("build", patterns, is_dir=True)
    assert not _matches_gitignore("build", patterns, is_dir=False)
    assert _matches_gitignore("file.pyc", patterns, is_dir=False)


def test_matches_gitignore_nested_path():
    """Test gitignore pattern matching with nested paths."""
    patterns = ["*.log", "temp/"]
    
    assert _matches_gitignore("dir/file.log", patterns, is_dir=False)
    assert _matches_gitignore("temp", patterns, is_dir=True)


def test_matches_gitignore_no_patterns():
    """Test gitignore pattern matching with no patterns."""
    assert not _matches_gitignore("any/path", [], is_dir=False)
    assert not _matches_gitignore("any/path", None, is_dir=False)
