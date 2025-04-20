from io import StringIO

import pytest

from src.exporters.html_exporter import _dark_mode_html


# Define a simple Token class for testing purposes
class Token:
    def __init__(
        self,
        indent_level,
        zone_1_declaration,
        zone_1_relation,
        zone_2_modifier,
        zone_3_trigger,
    ):
        self.indent_level = indent_level
        self.zone_1_declaration = zone_1_declaration
        self.zone_1_relation = zone_1_relation
        self.zone_2_modifier = zone_2_modifier
        self.zone_3_trigger = zone_3_trigger


@pytest.mark.usefixtures("setup_file")
class TestDarkModeHtml:

    @pytest.fixture
    def setup_file(self):
        # Setup a StringIO object to simulate file writing
        self.f = StringIO()

    @pytest.mark.happy_path
    def test_dark_mode_with_full_tokens(self, setup_file):
        """Test dark mode with tokens having all attributes."""
        tokens = [
            Token(1, "declaration1", "relation1", "modifier1", "trigger1"),
            Token(2, "declaration2", "relation2", "modifier2", "trigger2"),
        ]
        _dark_mode_html(self.f, True, tokens)
        output = self.f.getvalue()
        assert "<body class='dark'>" in output
        assert (
            "<span class='declaration'>    declaration1</span> <span class='relation'>relation1 //</span>"
            in output
        )
        assert "<span class='modifier'>% modifier1</span>" in output
        assert "<span class='trigger'>-> trigger1</span>" in output

    @pytest.mark.happy_path
    def test_light_mode_with_partial_tokens(self, setup_file):
        """Test light mode with tokens missing some attributes."""
        tokens = [
            Token(0, None, "relation1", None, "trigger1"),
            Token(1, "declaration2", "relation2", None, None),
        ]
        _dark_mode_html(self.f, False, tokens)
        output = self.f.getvalue()
        assert "<body class='light'>" in output
        assert "<span class='relation'>relation1 //</span>" in output
        assert "<span class='trigger'>-> trigger1</span>" in output
        assert (
            "<span class='declaration'>    declaration2</span> <span class='relation'>relation2 //</span>"
            in output
        )

    @pytest.mark.edge_case
    def test_empty_tokens(self, setup_file):
        """Test with an empty list of tokens."""
        tokens = []
        _dark_mode_html(self.f, True, tokens)
        output = self.f.getvalue()
        assert "<body class='dark'>" in output
        assert "<pre>\n</pre>" in output

    @pytest.mark.edge_case
    def test_no_declaration_or_modifier_or_trigger(self, setup_file):
        """Test with tokens having no declaration, modifier, or trigger."""
        tokens = [
            Token(0, None, "relation1", None, None),
            Token(1, None, "relation2", None, None),
        ]
        _dark_mode_html(self.f, False, tokens)
        output = self.f.getvalue()
        assert "<body class='light'>" in output
        assert "<span class='relation'>relation1 //</span>" in output
        assert "<span class='relation'>    relation2 //</span>" in output

    @pytest.mark.edge_case
    def test_large_indent_level(self, setup_file):
        """Test with a token having a large indent level."""
        tokens = [Token(10, "declaration", "relation", "modifier", "trigger")]
        _dark_mode_html(self.f, True, tokens)
        output = self.f.getvalue()
        assert "<span class='declaration'>" + " " * 40 + "declaration</span>" in output
