"""Tests for repolyze.core.filesystem.paths module."""

from pathlib import Path
import pytest

from repolyze.core.filesystem.paths import depth


def test_depth_same_directory():
    """Test depth when target is the same as base."""
    base = Path("/home/user/project")
    target = Path("/home/user/project")
    assert depth(base, target) == 0


def test_depth_one_level_deep():
    """Test depth for target one level below base."""
    base = Path("/home/user/project")
    target = Path("/home/user/project/src")
    assert depth(base, target) == 1


def test_depth_multiple_levels():
    """Test depth for target multiple levels below base."""
    base = Path("/home/user/project")
    target = Path("/home/user/project/src/core/utils")
    assert depth(base, target) == 3


def test_depth_with_file():
    """Test depth with a file path as target."""
    base = Path("/home/user/project")
    target = Path("/home/user/project/src/main.py")
    assert depth(base, target) == 2


def test_depth_raises_when_not_relative():
    """Test that depth raises ValueError when target is not relative to base."""
    base = Path("/home/user/project")
    target = Path("/different/path")
    with pytest.raises(ValueError):
        depth(base, target)
