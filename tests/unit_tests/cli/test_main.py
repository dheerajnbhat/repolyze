"""Tests for repolyze.cli.main module."""


from unittest.mock import patch, MagicMock

from repolyze.cli.main import parse_args, main


def test_parse_args_default():
    """Test parsing args with defaults."""
    with patch('sys.argv', ['repolyze']):
        args = parse_args()
        
        assert args.path == "."
        assert args.json is False


def test_parse_args_with_path():
    """Test parsing args with custom path."""
    with patch('sys.argv', ['repolyze', '/custom/path']):
        args = parse_args()
        
        assert args.path == "/custom/path"


def test_parse_args_with_json_flag():
    """Test parsing args with --json flag."""
    with patch('sys.argv', ['repolyze', '--json']):
        args = parse_args()
        
        assert args.json is True


def test_parse_args_with_path_and_json():
    """Test parsing args with both path and --json."""
    with patch('sys.argv', ['repolyze', '/my/repo', '--json']):
        args = parse_args()
        
        assert args.path == "/my/repo"
        assert args.json is True


@patch('repolyze.cli.main.analyze')
@patch('builtins.print')
def test_main_human_readable_output(mock_print, mock_analyze, tmp_path):
    """Test main with human-readable output."""
    # Create a mock stats object
    mock_stats = MagicMock()
    mock_stats.path = tmp_path
    mock_stats.structure.total_files = 10
    mock_stats.structure.total_dirs = 3
    mock_stats.size.total_size = 5000
    mock_stats.size.large_files = []
    mock_stats.file_types.count_by_extension = {".py": 5, ".txt": 5}
    mock_analyze.return_value = mock_stats
    
    with patch('sys.argv', ['repolyze', str(tmp_path)]):
        main()
    
    # Check that analyze was called
    mock_analyze.assert_called_once()
    # Check that print was called (human readable output)
    assert mock_print.called


@patch('repolyze.cli.main.analyze')
@patch('builtins.print')
def test_main_json_output(mock_print, mock_analyze, tmp_path):
    """Test main with JSON output."""
    # Create a mock stats object
    mock_stats = MagicMock()
    mock_stats.to_dict.return_value = {"path": str(tmp_path), "files": 10}
    mock_analyze.return_value = mock_stats
    
    with patch('sys.argv', ['repolyze', str(tmp_path), '--json']):
        main()
    
    # Check that to_dict was called
    mock_stats.to_dict.assert_called_once()
    # Check that print was called with JSON
    assert mock_print.called


@patch('repolyze.cli.main.analyze')
@patch('builtins.print')
def test_main_displays_file_types(mock_print, mock_analyze, tmp_path):
    """Test that main displays file types."""
    mock_stats = MagicMock()
    mock_stats.path = tmp_path
    mock_stats.structure.total_files = 10
    mock_stats.structure.total_dirs = 3
    mock_stats.size.total_size = 5000
    mock_stats.size.large_files = []
    mock_stats.file_types.count_by_extension = {".py": 8, ".md": 2}
    mock_analyze.return_value = mock_stats
    
    with patch('sys.argv', ['repolyze', str(tmp_path)]):
        main()
    
    # Verify that file type information was printed
    print_calls = [str(call) for call in mock_print.call_args_list]
    output = ' '.join(print_calls)
    assert '.py' in output or 'File types' in output


@patch('repolyze.cli.main.analyze')
@patch('builtins.print')
def test_main_displays_large_files(mock_print, mock_analyze, tmp_path):
    """Test that main displays large files."""
    large_file = MagicMock()
    large_file.path = tmp_path / "large.bin"
    large_file.size = 10 * 1024 * 1024  # 10 MB
    
    mock_stats = MagicMock()
    mock_stats.path = tmp_path
    mock_stats.structure.total_files = 5
    mock_stats.structure.total_dirs = 1
    mock_stats.size.total_size = 15000000
    mock_stats.size.large_files = [large_file]
    mock_stats.file_types.count_by_extension = {".bin": 1}
    mock_analyze.return_value = mock_stats
    
    with patch('sys.argv', ['repolyze', str(tmp_path)]):
        main()
    
    # Verify that large files section was printed
    assert mock_print.called
