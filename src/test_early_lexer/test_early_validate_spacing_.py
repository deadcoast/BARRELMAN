import pytest

from src.lexer import BarrelmanLexer


@pytest.mark.parametrize("line, lineno, expected", [
    # Happy path tests
    (":: valid line", 1, None),
    (":^: valid line", 2, None),
    (" :^: valid line", 3, None),
])
@pytest.mark.happy_path
def test_barrelman_lexer_validate_spacing_happy_paths(line, lineno, expected):
    """
    Test validate_spacing for happy path scenarios.
    """
    lexer = BarrelmanLexer("")
    result = lexer.validate_spacing(line, lineno)
    assert result == expected

@pytest.mark.parametrize("line, lineno, expected", [
    # Edge case tests
    ("::  :: invalid spacing", 4, "[Line 4] ERROR: Extra spacing on nested '::' block."),
    ("some text :^: invalid position", 5, "[Line 5] ERROR: ':^:' must be at the start of the line or have a single space before it."),
    ("::", 6, None),  # Edge case: minimal valid '::' line
    (":^:", 7, None),  # Edge case: minimal valid ':^:' line
    ("", 8, None),  # Edge case: empty line
])
@pytest.mark.edge_case
def test_barrelman_lexer_validate_spacing_edge_cases(line, lineno, expected):
    """
    Test validate_spacing for edge case scenarios.
    """
    lexer = BarrelmanLexer("")
    result = lexer.validate_spacing(line, lineno)
    assert result == expected

class TestBarrelmanLexerValidateSpacing:
    """
    Test class for BarrelmanLexer.validate_spacing method.
    """

    @pytest.mark.happy_path
    def test_happy_paths(self):
        """
        Test validate_spacing for happy path scenarios.
        """
        lexer = BarrelmanLexer("")
        assert lexer.validate_spacing(":: valid line", 1) is None
        assert lexer.validate_spacing(":^: valid line", 2) is None
        assert lexer.validate_spacing(" :^: valid line", 3) is None

    @pytest.mark.edge_case
    def test_edge_cases(self):
        """
        Test validate_spacing for edge case scenarios.
        """
        lexer = BarrelmanLexer("")
        assert lexer.validate_spacing("::  :: invalid spacing", 4) == "[Line 4] ERROR: Extra spacing on nested '::' block."
        assert lexer.validate_spacing("some text :^: invalid position", 5) == "[Line 5] ERROR: ':^:' must be at the start of the line or have a single space before it."
        assert lexer.validate_spacing("::", 6) is None  # Edge case: minimal valid '::' line
        assert lexer.validate_spacing(":^:", 7) is None  # Edge case: minimal valid ':^:' line
        assert lexer.validate_spacing("", 8) is None  # Edge case: empty line        assert lexer.validate_spacing(":^:", 7) is None  # Edge case: minimal valid ':^:' line
        assert lexer.validate_spacing("", 8) is None  # Edge case: empty line