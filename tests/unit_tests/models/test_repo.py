"""Tests for repolyze.models.repo module."""

from pathlib import Path
from datetime import datetime
import pytest

from repolyze.models import (
    FileStat, DirStat, StructureStats, SizeStats, 
    FileTypeStats, LanguageStats, TimeStats, 
    HygieneStats, MetadataStats, TreeNode, RepoStats
)


def test_file_stat_creation():
    """Test creating a FileStat object."""
    path = Path("/test/file.txt")
    stat = FileStat(path=path, size=100, mtime=1234567890.0)
    
    assert stat.path == path
    assert stat.size == 100
    assert stat.mtime == 1234567890.0
    assert stat.lines is None


def test_file_stat_with_lines():
    """Test creating a FileStat with line count."""
    path = Path("/test/file.py")
    stat = FileStat(path=path, size=500, mtime=1234567890.0, lines=50)
    
    assert stat.lines == 50


def test_file_stat_immutable():
    """Test that FileStat is immutable (frozen)."""
    stat = FileStat(path=Path("/test"), size=100, mtime=1.0)
    
    with pytest.raises(AttributeError):
        stat.size = 200


def test_dir_stat_creation():
    """Test creating a DirStat object."""
    path = Path("/test/dir")
    stat = DirStat(path=path, depth=3)
    
    assert stat.path == path
    assert stat.depth == 3


def test_structure_stats_defaults():
    """Test StructureStats default values."""
    stats = StructureStats()
    
    assert stats.total_files == 0
    assert stats.total_dirs == 0
    assert stats.max_depth == 0
    assert stats.deepest_paths == []


def test_structure_stats_with_values():
    """Test StructureStats with values."""
    deepest = [DirStat(Path("/deep/path"), 5)]
    stats = StructureStats(
        total_files=100,
        total_dirs=20,
        max_depth=5,
        deepest_paths=deepest
    )
    
    assert stats.total_files == 100
    assert stats.total_dirs == 20
    assert stats.max_depth == 5
    assert len(stats.deepest_paths) == 1


def test_size_stats_defaults():
    """Test SizeStats default values."""
    stats = SizeStats()
    
    assert stats.total_size == 0
    assert stats.average_file_size == 0.0
    assert stats.large_files == []
    assert stats.small_files == []


def test_file_type_stats_defaults():
    """Test FileTypeStats default values."""
    stats = FileTypeStats()
    
    assert stats.count_by_extension == {}
    assert stats.size_by_extension == {}


def test_file_type_stats_with_data():
    """Test FileTypeStats with data."""
    stats = FileTypeStats(
        count_by_extension={".py": 10, ".js": 5},
        size_by_extension={".py": 50000, ".js": 25000}
    )
    
    assert stats.count_by_extension[".py"] == 10
    assert stats.size_by_extension[".js"] == 25000


def test_language_stats_defaults():
    """Test LanguageStats default values."""
    stats = LanguageStats()
    
    assert stats.primary_language is None
    assert stats.code_vs_non_code_ratio is None
    assert stats.total_lines_of_code is None


def test_time_stats_defaults():
    """Test TimeStats default values."""
    stats = TimeStats()
    
    assert stats.oldest_file is None
    assert stats.newest_file is None
    assert stats.modified_last_24h == 0
    assert stats.modified_last_7d == 0
    assert stats.modified_last_30d == 0
    assert stats.median_file_age_days is None


def test_hygiene_stats_defaults():
    """Test HygieneStats default values."""
    stats = HygieneStats()
    
    assert stats.empty_files == 0
    assert stats.empty_dirs == 0
    assert stats.large_files == []
    assert stats.temp_files == 0
    assert stats.hidden_files == 0


def test_metadata_stats_defaults():
    """Test MetadataStats default values."""
    stats = MetadataStats()
    
    assert stats.readme_present is False
    assert stats.license_present is False
    assert stats.gitignore_present is False
    assert stats.ci_present is False
    assert stats.config_files == []


def test_tree_node_creation():
    """Test creating a TreeNode."""
    node = TreeNode(path=Path("/test"), file_count=5, total_size=1000)
    
    assert node.path == Path("/test")
    assert node.file_count == 5
    assert node.total_size == 1000
    assert node.children == []


def test_tree_node_with_children():
    """Test TreeNode with children."""
    child1 = TreeNode(Path("/test/child1"), 1, 100)
    child2 = TreeNode(Path("/test/child2"), 2, 200)
    parent = TreeNode(Path("/test"), 3, 300, [child1, child2])
    
    assert len(parent.children) == 2
    assert parent.children[0].path == Path("/test/child1")


def test_repo_stats_to_dict(tmp_path):
    """Test converting RepoStats to dictionary."""
    test_path = tmp_path / "test_repo"
    stats = RepoStats(
        path=test_path,
        structure=StructureStats(total_files=5),
        size=SizeStats(total_size=1000),
        file_types=FileTypeStats(),
        language=LanguageStats(),
        time=TimeStats(),
        hygiene=HygieneStats(),
        metadata=MetadataStats(),
        tree=None
    )
    
    result = stats.to_dict()
    
    assert isinstance(result, dict)
    # Use str() for cross-platform path comparison
    assert result["path"] == str(test_path)
    assert result["structure"]["total_files"] == 5
    assert result["size"]["total_size"] == 1000
    assert "created_at" in result


def test_repo_stats_tree_to_dict(tmp_path):
    """Test converting RepoStats with tree to dictionary."""
    test_path = tmp_path / "test_repo"
    tree = TreeNode(test_path, 1, 100)
    stats = RepoStats(
        path=test_path,
        structure=StructureStats(),
        size=SizeStats(),
        file_types=FileTypeStats(),
        language=LanguageStats(),
        time=TimeStats(),
        hygiene=HygieneStats(),
        metadata=MetadataStats(),
        tree=tree
    )
    
    result = stats.to_dict()
    
    assert result["tree"] is not None
    # Use str() for cross-platform path comparison
    assert result["tree"]["path"] == str(test_path)
    assert result["tree"]["file_count"] == 1
    assert result["tree"]["total_size"] == 100


def test_repo_stats_created_at():
    """Test that RepoStats has created_at timestamp."""
    stats = RepoStats(
        path=Path("/test"),
        structure=StructureStats(),
        size=SizeStats(),
        file_types=FileTypeStats(),
        language=LanguageStats(),
        time=TimeStats(),
        hygiene=HygieneStats(),
        metadata=MetadataStats()
    )
    
    assert isinstance(stats.created_at, datetime)
    # Should be recent
    assert (datetime.utcnow() - stats.created_at).total_seconds() < 1
