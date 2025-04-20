import io
import sys

import pytest

from src.lexer import BarrelmanLexer, BarrelmanToken


@pytest.fixture
def setup_lexer():
    """Fixture to set up a BarrelmanLexer instance with no tokens."""
    return BarrelmanLexer("")

@pytest.mark.happy_path
class TestBarrelmanLexerHighlight:
    def test_highlight_with_full_token(self, setup_lexer):
        """Test highlight with a token having all zones filled."""
        lexer = setup_lexer
        lexer.tokens = [
            BarrelmanToken(
                line="test line",
                zone_1_declaration="declare",
                zone_1_relation="relate",
                zone_2_modifier="modify",
                zone_3_trigger="trigger",
                zone_4_outcome="outcome"
            )
        ]
        # Capture the output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        lexer.highlight()
        sys.stdout = sys.__stdout__
        
        # Check that output contains expected elements
        output = captured_output.getvalue()
        assert "BARRELMAN HIGHLIGHTED SYNTAX" in output
        assert "relate" in output
        assert "modify" in output
        assert "trigger" in output

    def test_highlight_with_partial_token(self, setup_lexer):
        """Test highlight with a token having some zones filled."""
        lexer = setup_lexer
        lexer.tokens = [
            BarrelmanToken(
                line="test line",
                zone_1_declaration="declare",
                zone_1_relation="relate",
                zone_2_modifier=None,
                zone_3_trigger="trigger",
                zone_4_outcome=None
            )
        ]
        # Capture the output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        lexer.highlight()
        sys.stdout = sys.__stdout__
        
        # Check that output contains expected elements
        output = captured_output.getvalue()
        assert "BARRELMAN HIGHLIGHTED SYNTAX" in output
        assert "relate" in output
        assert "trigger" in output

@pytest.mark.edge_case
class TestBarrelmanLexerHighlightEdgeCases:
    def test_highlight_with_empty_tokens(self, setup_lexer):
        """Test highlight with no tokens."""
        lexer = setup_lexer
        lexer.tokens = []
        # Capture the output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        lexer.highlight()
        sys.stdout = sys.__stdout__
        
        # Check that output contains expected elements
        output = captured_output.getvalue()
        assert "BARRELMAN HIGHLIGHTED SYNTAX" in output
        # No tokens, so just the header should be present

    def test_highlight_with_none_values(self, setup_lexer):
        """Test highlight with tokens having None for all zones."""
        lexer = setup_lexer
        lexer.tokens = [
            BarrelmanToken(
                line="test line",
                zone_1_declaration=None,
                zone_1_relation=None,
                zone_2_modifier=None,
                zone_3_trigger=None,
                zone_4_outcome=None
            )
        ]
        # Capture the output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        lexer.highlight()
        sys.stdout = sys.__stdout__
        
        # Check that output contains expected elements
        output = captured_output.getvalue()
        assert "BARRELMAN HIGHLIGHTED SYNTAX" in output
        assert "//" in output  # The // separator is always present

    def test_highlight_with_mixed_none_and_values(self, setup_lexer):
        """Test highlight with tokens having a mix of None and values."""
        lexer = setup_lexer
        lexer.tokens = [
            BarrelmanToken(
                line="test line",
                zone_1_declaration=None,
                zone_1_relation="relate",
                zone_2_modifier=None,
                zone_3_trigger="trigger",
                zone_4_outcome=None
            )
        ]
        # Capture the output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        lexer.highlight()
        sys.stdout = sys.__stdout__
        
        # Check that output contains expected elements
        output = captured_output.getvalue()
        assert "BARRELMAN HIGHLIGHTED SYNTAX" in output
        assert "relate" in output
