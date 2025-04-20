from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

from src.preview_server import run_preview_server


@pytest.fixture
def mock_lexer():
    """Fixture to mock the BarrelmanLexer and its tokenize method."""
    with patch("src.preview_server.BarrelmanLexer") as MockLexer:
        mock_lexer_instance = MockLexer.return_value
        mock_lexer_instance.tokenize.return_value = [
            MagicMock(
                indent_level=0,
                zone_1_declaration="declaration",
                zone_1_relation="relation",
                zone_2_modifier="modifier",
                zone_3_trigger="trigger",
            )
        ]
        yield MockLexer


@pytest.fixture
def mock_export_html():
    """Fixture to mock the export_html function."""
    with patch("src.preview_server.export_html") as mock_export:
        yield mock_export


@pytest.fixture
def mock_flask_app():
    """Fixture to mock Flask app's run method."""
    with patch.object(Flask, "run") as mock_run:
        yield mock_run


@pytest.mark.happy_path
class TestRunPreviewServer:
    def test_run_preview_server_normal(
        self, mock_lexer, mock_export_html, mock_flask_app
    ):
        """Test run_preview_server with normal content."""
        content = "normal content"
        run_preview_server(content)

        # Check if the lexer was called with the correct content
        mock_lexer.assert_called_once_with(content)

        # Check if the export_html was called with the correct parameters
        mock_export_html.assert_called_once()

        # Check if the Flask app's run method was called
        mock_flask_app.assert_called_once()


@pytest.mark.edge_case
class TestRunPreviewServerEdgeCases:
    def test_run_preview_server_empty_content(
        self, mock_lexer, mock_export_html, mock_flask_app
    ):
        """Test run_preview_server with empty content."""
        content = ""
        run_preview_server(content)

        # Check if the lexer was called with the correct content
        mock_lexer.assert_called_once_with(content)

        # Check if the export_html was called with the correct parameters
        mock_export_html.assert_called_once()

        # Check if the Flask app's run method was called
        mock_flask_app.assert_called_once()

    def test_run_preview_server_special_characters(
        self, mock_lexer, mock_export_html, mock_flask_app
    ):
        """Test run_preview_server with special characters in content."""
        content = "!@#$%^&*()_+"
        run_preview_server(content)

        # Check if the lexer was called with the correct content
        mock_lexer.assert_called_once_with(content)

        # Check if the export_html was called with the correct parameters
        mock_export_html.assert_called_once()

        # Check if the Flask app's run method was called
        mock_flask_app.assert_called_once()

    def test_run_preview_server_large_content(
        self, mock_lexer, mock_export_html, mock_flask_app
    ):
        """Test run_preview_server with large content."""
        content = "a" * 10000  # Large content
        run_preview_server(content)

        # Check if the lexer was called with the correct content
        mock_lexer.assert_called_once_with(content)

        # Check if the export_html was called with the correct parameters
        mock_export_html.assert_called_once()

        # Check if the Flask app's run method was called
        mock_flask_app.assert_called_once()
        # Check if the Flask app's run method was called
        mock_flask_app.assert_called_once()
