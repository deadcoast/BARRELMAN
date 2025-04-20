import pytest

from src.lexer import BarrelmanLexer


@pytest.mark.usefixtures("setup_lexer")
class TestBarrelmanLexerGetIndentLevel:
    @pytest.fixture
    def setup_lexer(self):
        # Setup a BarrelmanLexer instance with a dummy source
        self.lexer = BarrelmanLexer("")

    @pytest.mark.happy_path
    def test_no_indent(self):
        """Test that a line with no leading spaces returns an indent level of 0."""
        line = "No indent"
        expected_indent_level = 0
        assert self.lexer.get_indent_level(line) == expected_indent_level

    @pytest.mark.happy_path
    def test_single_space_indent(self):
        """Test that a line with a single leading space returns an indent level of 1."""
        line = " Single space indent"
        expected_indent_level = 1
        assert self.lexer.get_indent_level(line) == expected_indent_level

    @pytest.mark.happy_path
    def test_multiple_spaces_indent(self):
        """Test that a line with multiple leading spaces returns the correct indent level."""
        line = "    Four spaces indent"
        expected_indent_level = 4
        assert self.lexer.get_indent_level(line) == expected_indent_level

    @pytest.mark.edge_case
    def test_empty_line(self):
        """Test that an empty line returns an indent level of 0."""
        line = ""
        expected_indent_level = 0
        assert self.lexer.get_indent_level(line) == expected_indent_level

    @pytest.mark.edge_case
    def test_line_with_only_spaces(self):
        """Test that a line with only spaces returns the correct indent level."""
        line = "    "
        expected_indent_level = 4
        assert self.lexer.get_indent_level(line) == expected_indent_level

    @pytest.mark.edge_case
    def test_tab_indentation(self):
        """Test that a line with tabs is not counted as spaces for indentation."""
        line = "\tTabbed indent"
        expected_indent_level = 0  # Assuming tabs are not counted as spaces
        assert self.lexer.get_indent_level(line) == expected_indent_level

    @pytest.mark.edge_case
    def test_mixed_spaces_and_tabs(self):
        """Test that a line with mixed spaces and tabs only counts spaces for indentation."""
        line = "  \tMixed spaces and tabs"
        expected_indent_level = 2  # Only spaces are counted
        assert self.lexer.get_indent_level(line) == expected_indent_level

    @pytest.mark.edge_case
    def test_leading_newline_character(self):
        """Test that a line with a leading newline character returns an indent level of 0."""
        line = "\nNewline character"
        expected_indent_level = 0
        assert self.lexer.get_indent_level(line) == expected_indent_level
