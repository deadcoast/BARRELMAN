from unittest.mock import mock_open, patch

import pytest

from src.exporters.markdown_exporter import export_markdown


# Assuming BarrelmanToken is a class with attributes: indent_level, zone_1_declaration, zone_1_relation, zone_2_modifier, zone_3_trigger
class BarrelmanToken:
    def __init__(self, indent_level=0, zone_1_declaration=None, zone_1_relation=None, zone_2_modifier=None, zone_3_trigger=None):
        self.indent_level = indent_level
        self.zone_1_declaration = zone_1_declaration
        self.zone_1_relation = zone_1_relation
        self.zone_2_modifier = zone_2_modifier
        self.zone_3_trigger = zone_3_trigger


@pytest.mark.usefixtures("mock_open")
class TestExportMarkdown:

    @pytest.fixture
    def mock_open(self):
        with patch("builtins.open", mock_open()) as m:
            yield m

    @pytest.mark.happy_path
    def test_export_markdown_basic(self, mock_open):
        """Test exporting a basic list of tokens to markdown."""
        tokens = [
            BarrelmanToken(indent_level=0, zone_1_declaration="declare", zone_1_relation="relate"),
            BarrelmanToken(indent_level=1, zone_1_declaration="subdeclare", zone_1_relation="subrelate")
        ]
        export_markdown(tokens, "test.md")
        mock_open().write.assert_any_call("```barrelman\n")
        mock_open().write.assert_any_call("declare relate //\n")
        mock_open().write.assert_any_call("    subdeclare subrelate //\n")
        mock_open().write.assert_any_call("```\n")

    @pytest.mark.happy_path
    def test_export_markdown_with_modifiers_and_triggers(self, mock_open):
        """Test exporting tokens with modifiers and triggers."""
        tokens = [
            BarrelmanToken(indent_level=0, zone_1_declaration="declare", zone_1_relation="relate", zone_2_modifier="mod", zone_3_trigger="trigger")
        ]
        export_markdown(tokens, "test.md")
        mock_open().write.assert_any_call("declare relate // % mod -> trigger\n")

    @pytest.mark.edge_case
    def test_export_markdown_empty_tokens(self, mock_open):
        """Test exporting with an empty list of tokens."""
        tokens = []
        export_markdown(tokens, "test.md")
        mock_open().write.assert_any_call("```barrelman\n")
        mock_open().write.assert_any_call("```\n")

    @pytest.mark.edge_case
    def test_export_markdown_no_declaration(self, mock_open):
        """Test exporting tokens without a zone_1_declaration."""
        tokens = [
            BarrelmanToken(indent_level=0, zone_1_relation="relate")
        ]
        export_markdown(tokens, "test.md")
        mock_open().write.assert_any_call("relate //\n")

    @pytest.mark.edge_case
    def test_export_markdown_no_relation(self, mock_open):
        """Test exporting tokens without a zone_1_relation."""
        tokens = [
            BarrelmanToken(indent_level=0, zone_1_declaration="declare")
        ]
        export_markdown(tokens, "test.md")
        mock_open().write.assert_any_call("declare //\n")

    @pytest.mark.edge_case
    def test_export_markdown_no_modifier_or_trigger(self, mock_open):
        """Test exporting tokens without modifiers or triggers."""
        tokens = [
            BarrelmanToken(indent_level=0, zone_1_declaration="declare", zone_1_relation="relate")
        ]
        export_markdown(tokens, "test.md")
        mock_open().write.assert_any_call("declare relate //\n")

    @pytest.mark.edge_case
    def test_export_markdown_with_options(self, mock_open):
        """Test exporting with options provided (though not used)."""
        tokens = [
            BarrelmanToken(indent_level=0, zone_1_declaration="declare", zone_1_relation="relate")
        ]
        export_markdown(tokens, "test.md", options={"unused_option": True})
        mock_open().write.assert_any_call("declare relate //\n")
