"""Tests for repolyze.core.analyze module."""

from repolyze.core.analyze import analyze


def test_analyze_empty_directory(tmp_path):
    """Test analyzing an empty directory."""
    stats = analyze(tmp_path)
    
    assert stats.path == tmp_path
    assert stats.structure.total_files == 0
    assert stats.structure.total_dirs == 0
    assert stats.size.total_size == 0


def test_analyze_with_files(tmp_path):
    """Test analyzing directory with files."""
    (tmp_path / "file1.txt").write_text("hello")
    (tmp_path / "file2.py").write_text("print('hello')")
    
    stats = analyze(tmp_path)
    
    assert stats.structure.total_files == 2
    assert stats.size.total_size > 0


def test_analyze_with_directories(tmp_path):
    """Test analyzing directory with subdirectories."""
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file.txt").write_text("content")
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "subdir").mkdir()
    
    stats = analyze(tmp_path)
    
    assert stats.structure.total_dirs >= 2
    assert stats.structure.total_files >= 1


def test_analyze_file_types(tmp_path):
    """Test that analyze correctly counts file types."""
    (tmp_path / "file.py").write_text("code")
    (tmp_path / "file.js").write_text("code")
    (tmp_path / "file.txt").write_text("text")
    (tmp_path / "file.py.bak").write_text("backup")  # .bak extension
    
    stats = analyze(tmp_path)
    
    assert ".py" in stats.file_types.count_by_extension
    assert ".js" in stats.file_types.count_by_extension
    assert ".txt" in stats.file_types.count_by_extension


def test_analyze_size_calculations(tmp_path):
    """Test that analyze correctly calculates sizes."""
    content1 = "x" * 1000
    content2 = "y" * 2000
    (tmp_path / "file1.txt").write_text(content1)
    (tmp_path / "file2.txt").write_text(content2)
    
    stats = analyze(tmp_path)
    
    assert stats.size.total_size >= 3000
    assert stats.size.average_file_size > 0


def test_analyze_depth(tmp_path):
    """Test that analyze calculates max depth correctly."""
    (tmp_path / "level1").mkdir()
    (tmp_path / "level1" / "level2").mkdir()
    (tmp_path / "level1" / "level2" / "level3").mkdir()
    (tmp_path / "level1" / "level2" / "level3" / "file.txt").touch()
    
    stats = analyze(tmp_path)
    
    assert stats.structure.max_depth >= 3


def test_analyze_empty_files(tmp_path):
    """Test that analyze counts empty files."""
    (tmp_path / "empty.txt").touch()
    (tmp_path / "nonempty.txt").write_text("content")
    
    stats = analyze(tmp_path)
    
    assert stats.hygiene.empty_files >= 1


def test_analyze_hidden_files(tmp_path):
    """Test that analyze counts hidden files."""
    (tmp_path / ".hidden").write_text("secret")
    (tmp_path / "visible.txt").write_text("public")
    
    stats = analyze(tmp_path)
    
    assert stats.hygiene.hidden_files >= 1


def test_analyze_temp_files(tmp_path):
    """Test that analyze counts temp files."""
    (tmp_path / "file.tmp").write_text("temp")
    (tmp_path / "file.bak").write_text("backup")
    (tmp_path / "normal.txt").write_text("normal")
    
    stats = analyze(tmp_path)
    
    assert stats.hygiene.temp_files >= 1


def test_analyze_large_files(tmp_path):
    """Test that analyze identifies large files."""
    # Create a file larger than 5MB
    large_content = "x" * (6 * 1024 * 1024)
    (tmp_path / "large.bin").write_text(large_content)
    
    stats = analyze(tmp_path)
    
    assert len(stats.hygiene.large_files) >= 1


def test_analyze_metadata(tmp_path):
    """Test that analyze detects metadata files."""
    (tmp_path / "README.md").write_text("# Project")
    (tmp_path / "LICENSE").write_text("MIT")
    (tmp_path / ".gitignore").write_text("*.pyc")
    (tmp_path / "pyproject.toml").write_text("[tool]")
    
    stats = analyze(tmp_path)
    
    assert stats.metadata.readme_present is True
    assert stats.metadata.license_present is True
    assert stats.metadata.gitignore_present is True
    assert "pyproject.toml" in stats.metadata.config_files


def test_analyze_primary_language(tmp_path):
    """Test that analyze determines primary language."""
    # Create more Python files
    for i in range(5):
        (tmp_path / f"file{i}.py").write_text("code")
    (tmp_path / "file.js").write_text("code")
    
    stats = analyze(tmp_path)
    
    assert stats.language.primary_language == ".py"


def test_analyze_string_path(tmp_path):
    """Test that analyze works with string path."""
    (tmp_path / "file.txt").write_text("content")
    
    stats = analyze(str(tmp_path))
    
    assert stats.structure.total_files >= 1


def test_analyze_respects_gitignore(tmp_path):
    """Test that analyze respects .gitignore patterns."""
    (tmp_path / ".gitignore").write_text("*.log\n")
    (tmp_path / "file.txt").write_text("text")
    (tmp_path / "file.log").write_text("log")
    
    stats = analyze(tmp_path)
    
    # file.log should be excluded
    assert ".log" not in stats.file_types.count_by_extension or \
           stats.file_types.count_by_extension.get(".log", 0) == 0


def test_analyze_skips_common_dirs(tmp_path):
    """Test that analyze skips common directories like .git, __pycache__."""
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("git config")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "cache.pyc").write_bytes(b"cache")
    (tmp_path / "normal.txt").write_text("normal")
    
    stats = analyze(tmp_path)
    
    # Should only count normal.txt
    assert stats.structure.total_files == 1


def test_analyze_tree_structure(tmp_path):
    """Test that analyze includes tree structure."""
    (tmp_path / "file.txt").write_text("content")
    (tmp_path / "dir1").mkdir()
    
    stats = analyze(tmp_path)
    
    assert stats.tree is not None
    assert stats.tree.path == tmp_path
