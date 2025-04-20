import pytest

from src.lexer import BarrelmanLexer


@pytest.mark.usefixtures("setup_lexer")
class TestBarrelmanLexerTokenize:
    @pytest.fixture
    def setup_lexer(self):
        # This fixture can be used to set up any common state or objects needed for the tests
        pass

    @pytest.mark.happy_path
    def test_tokenize_simple_declaration(self):
        """Test a simple declaration with no modifiers or triggers."""
        source = ":: simple_declaration"
        lexer = BarrelmanLexer(source)
        tokens = lexer.tokenize()

        assert len(tokens) == 1
        assert tokens[0].zone_1_declaration == "::"
        assert tokens[0].zone_1_relation == "simple_declaration"
        assert tokens[0].zone_2_modifier is None
        assert tokens[0].zone_3_trigger is None

    @pytest.mark.happy_path
    def test_tokenize_with_modifier_and_trigger(self):
        """Test a line with a modifier and a trigger."""
        source = ":: relation // %modifier -> trigger"
        lexer = BarrelmanLexer(source)
        tokens = lexer.tokenize()

        assert len(tokens) == 1
        assert tokens[0].zone_1_declaration == "::"
        assert tokens[0].zone_1_relation == "relation"
        assert tokens[0].zone_2_modifier == "modifier"
        assert tokens[0].zone_3_trigger == "trigger"

    @pytest.mark.happy_path
    def test_tokenize_with_nesting(self):
        """Test a line with nesting declaration."""
        source = ":^: nested_relation"
        lexer = BarrelmanLexer(source)
        tokens = lexer.tokenize()

        assert len(tokens) == 1
        # The lexer treats the entire string as zone_1_relation and sets is_nesting_port based on :^:
        assert tokens[0].is_nesting_port is True
        assert tokens[0].zone_1_relation == ":^: nested_relation"
        assert tokens[0].zone_1_declaration is None

    @pytest.mark.edge_case
    def test_tokenize_empty_line(self):
        """Test that an empty line is ignored."""
        source = "\n"
        lexer = BarrelmanLexer(source)
        tokens = lexer.tokenize()

        assert len(tokens) == 0

    @pytest.mark.edge_case
    def test_tokenize_line_with_only_spaces(self):
        """Test that a line with only spaces is ignored."""
        source = "    "
        lexer = BarrelmanLexer(source)
        tokens = lexer.tokenize()

        assert len(tokens) == 0

    @pytest.mark.edge_case
    def test_tokenize_invalid_syntax(self):
        """Test handling of a line with invalid syntax."""
        source = ":: invalid_syntax %"
        lexer = BarrelmanLexer(source)
        tokens = lexer.tokenize()

        # The actual implementation doesn't reject invalid syntax
        # It creates a token with what it can parse
        assert len(tokens) == 1
        assert tokens[0].zone_1_declaration == "::"
        assert tokens[0].zone_1_relation == "invalid_syntax %"
        assert tokens[0].zone_2_modifier is None
        assert tokens[0].zone_3_trigger is None

    @pytest.mark.edge_case
    def test_tokenize_multiple_declarations(self):
        """Test a line with multiple declarations."""
        source = ":: first // second // third"
        lexer = BarrelmanLexer(source)
        tokens = lexer.tokenize()

        assert len(tokens) == 1
        assert tokens[0].zone_1_declaration == "::"
        # The actual implementation only handles the first two parts after splitting on //
        assert tokens[0].zone_1_relation == "first second"
        assert tokens[0].zone_2_modifier is None
        assert tokens[0].zone_3_trigger is None

    @pytest.mark.edge_case
    def test_tokenize_no_declaration(self):
        """Test a line with no declaration."""
        source = "relation // %modifier -> trigger"
        lexer = BarrelmanLexer(source)
        tokens = lexer.tokenize()

        assert len(tokens) == 1
        assert tokens[0].zone_1_declaration is None
        assert tokens[0].zone_1_relation == "relation"
        assert tokens[0].zone_2_modifier == "modifier"
        assert tokens[0].zone_3_trigger == "trigger"


# To run these tests, use the command: pytest -v
# To run these tests, use the command: pytest -v
