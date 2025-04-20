from unittest.mock import mock_open, patch

import pytest

from src.exporters.html_exporter import export_html


# Mock class to simulate BarrelmanToken objects
class MockBarrelmanToken:
    def __init__(self, indent_level=0, zone_1_declaration=None, zone_1_relation=None, zone_2_modifier=None, zone_3_trigger=None):
        self.indent_level = indent_level
        self.zone_1_declaration = zone_1_declaration
        self.zone_1_relation = zone_1_relation
        self.zone_2_modifier = zone_2_modifier
        self.zone_3_trigger = zone_3_trigger

@pytest.mark.usefixtures("mock_open")
class TestExportHtml:

    @pytest.fixture
    def mock_open(self):
        with patch("builtins.open", mock_open()) as m:
            yield m

    @pytest.mark.happy_path
    def test_export_html_default_filename(self, mock_open):
        """Test exporting HTML with default filename and no options."""
        tokens = [MockBarrelmanToken(zone_1_relation="relation")]
        export_html(tokens)
        mock_open.assert_called_once_with("barrelman_syntax.html", 'w')
        handle = mock_open()
        handle.write.assert_called()  # Ensure write was called

    @pytest.mark.happy_path
    def test_export_html_custom_filename(self, mock_open):
        """Test exporting HTML with a custom filename."""
        tokens = [MockBarrelmanToken(zone_1_relation="relation")]
        export_html(tokens, filename="custom.html")
        mock_open.assert_called_once_with("custom.html", 'w')

    @pytest.mark.happy_path
    def test_export_html_dark_mode(self, mock_open):
        """Test exporting HTML with dark mode enabled."""
        tokens = [MockBarrelmanToken(zone_1_relation="relation")]
        export_html(tokens, options={"dark_mode": True})
        handle = mock_open()
        handle.write.assert_any_call("<body class='dark'><pre>\n")

    @pytest.mark.happy_path
    def test_export_html_light_mode(self, mock_open):
        """Test exporting HTML with light mode (default)."""
        tokens = [MockBarrelmanToken(zone_1_relation="relation")]
        export_html(tokens)
        handle = mock_open()
        handle.write.assert_any_call("<body class='light'><pre>\n")

    @pytest.mark.edge_case
    def test_export_html_empty_tokens(self, mock_open):
        """Test exporting HTML with an empty list of tokens."""
        export_html([])
        handle = mock_open()
        handle.write.assert_any_call("<body class='light'><pre>\n")
        handle.write.assert_any_call("</pre></body></html>")

    @pytest.mark.edge_case
    def test_export_html_no_relation(self, mock_open):
        """Test exporting HTML with a token missing a relation."""
        tokens = [MockBarrelmanToken(zone_1_declaration="declaration")]
        export_html(tokens)
        handle = mock_open()
        handle.write.assert_any_call("<span class='declaration'>declaration</span> <span class='relation'> //</span>")

    @pytest.mark.edge_case
    def test_export_html_no_declaration(self, mock_open):
        """Test exporting HTML with a token missing a declaration."""
        tokens = [MockBarrelmanToken(zone_1_relation="relation")]
        export_html(tokens)
        handle = mock_open()
        handle.write.assert_any_call("<span class='relation'>relation //</span>")

    @pytest.mark.edge_case
    def test_export_html_with_modifier_and_trigger(self, mock_open):
        """Test exporting HTML with tokens having modifiers and triggers."""
        tokens = [MockBarrelmanToken(zone_1_relation="relation", zone_2_modifier="modifier", zone_3_trigger="trigger")]
        export_html(tokens)
        handle = mock_open()
        handle.write.assert_any_call("<span class='modifier'>% modifier</span>")
        handle.write.assert_any_call("<span class='trigger'>-> trigger</span>")

    @pytest.mark.edge_case
    def test_export_html_invalid_options(self, mock_open):
        """Test exporting HTML with invalid options."""
        tokens = [MockBarrelmanToken(zone_1_relation="relation")]
        export_html(tokens, options={"invalid_option": True})
        handle = mock_open()
        handle.write.assert_any_call("<body class='light'><pre>\n")
