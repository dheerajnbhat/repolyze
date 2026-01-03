"""Tests for repolyze.core.formatting.human module."""


from repolyze.core.formatting.human import format_bytes


def test_format_bytes_zero():
    """Test formatting zero bytes."""
    assert format_bytes(0) == "0.0 B"


def test_format_bytes_small():
    """Test formatting small byte values."""
    assert format_bytes(100) == "100.0 B"
    assert format_bytes(512) == "512.0 B"
    assert format_bytes(1023) == "1023.0 B"


def test_format_bytes_kilobytes():
    """Test formatting kilobytes."""
    assert format_bytes(1024) == "1.0 KB"
    assert format_bytes(2048) == "2.0 KB"
    assert format_bytes(1536) == "1.5 KB"
    assert format_bytes(10240) == "10.0 KB"


def test_format_bytes_megabytes():
    """Test formatting megabytes."""
    assert format_bytes(1024 * 1024) == "1.0 MB"
    assert format_bytes(5 * 1024 * 1024) == "5.0 MB"
    assert format_bytes(1.5 * 1024 * 1024) == "1.5 MB"


def test_format_bytes_gigabytes():
    """Test formatting gigabytes."""
    assert format_bytes(1024 * 1024 * 1024) == "1.0 GB"
    assert format_bytes(2.5 * 1024 * 1024 * 1024) == "2.5 GB"


def test_format_bytes_terabytes():
    """Test formatting terabytes."""
    assert format_bytes(1024 * 1024 * 1024 * 1024) == "1.0 TB"
    assert format_bytes(5 * 1024 * 1024 * 1024 * 1024) == "5.0 TB"


def test_format_bytes_precision():
    """Test that format_bytes maintains one decimal place."""
    result = format_bytes(1234)
    assert result == "1.2 KB"
    
    result = format_bytes(1234567)
    assert result == "1.2 MB"
