from io import StringIO
from unittest import mock

import pytest

from src.cli import run_cli


# Create fixtures at the module level
@pytest.fixture
def mock_export_dot_graph():
    with mock.patch("src.cli.export_dot_graph") as mock_func:
        yield mock_func


@pytest.fixture
def mock_export_markdown():
    with mock.patch("src.cli.export_markdown") as mock_func:
        yield mock_func


@pytest.fixture
def mock_export_html():
    with mock.patch("src.cli.export_html") as mock_func:
        yield mock_func


@pytest.fixture
def mock_run_preview_server():
    with mock.patch("src.cli.run_preview_server") as mock_func:
        yield mock_func


class TestRunCli:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        mock_export_dot_graph,
        mock_export_markdown,
        mock_export_html,
        mock_run_preview_server,
    ):
        # Setup code that runs before each test
        self.mock_export_dot_graph = mock_export_dot_graph
        self.mock_export_markdown = mock_export_markdown
        self.mock_export_html = mock_export_html
        self.mock_run_preview_server = mock_run_preview_server

    @pytest.mark.happy_path
    def test_highlight_option(self):
        """Test that the highlight option calls the highlight method of the lexer."""
        test_args = ["cli.py", "test.bman", "--highlight"]
        with mock.patch("sys.argv", test_args), mock.patch(
            "src.cli.BarrelmanLexer.highlight"
        ) as mock_highlight, mock.patch(
            "builtins.open", mock.mock_open(read_data="content")
        ):
            run_cli()
            mock_highlight.assert_called_once()

    @pytest.mark.happy_path
    def test_html_export(self):
        """Test that the HTML export option calls the export_html function."""
        test_args = ["cli.py", "test.bman", "--html"]
        with mock.patch("sys.argv", test_args), mock.patch(
            "builtins.open", mock.mock_open(read_data="content")
        ):
            run_cli()
            self.mock_export_html.assert_called_once()

    @pytest.mark.happy_path
    def test_markdown_export(self):
        """Test that the Markdown export option calls the export_markdown function."""
        test_args = ["cli.py", "test.bman", "--markdown"]
        with mock.patch("sys.argv", test_args), mock.patch(
            "builtins.open", mock.mock_open(read_data="content")
        ):
            run_cli()
            self.mock_export_markdown.assert_called_once()

    @pytest.mark.happy_path
    def test_dot_export(self):
        """Test that the dot export option calls the export_dot_graph function."""
        test_args = ["cli.py", "test.bman", "--dot"]
        with mock.patch("sys.argv", test_args), mock.patch(
            "builtins.open", mock.mock_open(read_data="content")
        ):
            run_cli()
            self.mock_export_dot_graph.assert_called_once()

    @pytest.mark.happy_path
    def test_preview_server(self):
        """Test that the preview option calls the run_preview_server function."""
        test_args = ["cli.py", "test.bman", "--preview"]
        with mock.patch("sys.argv", test_args), mock.patch(
            "builtins.open", mock.mock_open(read_data="content")
        ):
            run_cli()
            self.mock_run_preview_server.assert_called_once()

    @pytest.mark.edge_case
    def test_no_arguments(self):
        """Test that the function handles no arguments gracefully."""
        test_args = ["cli.py"]
        with mock.patch("sys.argv", test_args), mock.patch(
            "sys.stderr", new_callable=StringIO
        ) as mock_stderr:
            with pytest.raises(SystemExit):
                run_cli()
            assert (
                "the following arguments are required: file" in mock_stderr.getvalue()
            )

    @pytest.mark.edge_case
    def test_non_existent_file(self):
        """Test that the function handles non-existent file input gracefully."""
        test_args = ["cli.py", "non_existent.bman"]
        with mock.patch("sys.argv", test_args), mock.patch(
            "builtins.open", side_effect=FileNotFoundError
        ):
            with pytest.raises(FileNotFoundError):
                run_cli()

    @pytest.mark.edge_case
    def test_empty_file(self):
        """Test that the function handles an empty file gracefully."""
        test_args = ["cli.py", "empty.bman"]
        with mock.patch("sys.argv", test_args), mock.patch(
            "builtins.open", mock.mock_open(read_data="")
        ):
            run_cli()
            # Ensure no export functions are called
            self.mock_export_html.assert_not_called()
            self.mock_export_markdown.assert_not_called()
            self.mock_export_dot_graph.assert_not_called()
            self.mock_run_preview_server.assert_not_called()
