import pytest

from src.lexer import BarrelmanLexer, BarrelmanToken


class TestBarrelmanLexerRenderSyntaxTree:
    @pytest.fixture
    def lexer(self):
        """Fixture to create a BarrelmanLexer instance."""
        return BarrelmanLexer("")

    @pytest.mark.happy_path
    def test_render_syntax_tree_single_token(self, lexer, capsys):
        """Test rendering a syntax tree with a single token."""
        lexer.tokens = [
            BarrelmanToken(
                line="line1",
                zone_1_declaration=None,
                zone_1_relation="relation1",
                zone_2_modifier="modifier1",
                zone_3_trigger="trigger1",
                zone_4_outcome="outcome1",
                indent_level=0,
                is_nesting_port=False,
            )
        ]
        lexer.render_syntax_tree()
        captured = capsys.readouterr().out
        expected_output = (
            "\nBARRELMAN SYNTAX TREE:\n\n"
            "├── relation1\n"
            "│   ├── Modifier: modifier1\n"
            "│   ├── Trigger: trigger1\n"
            "│   └── Outcome: outcome1\n"
        )
        assert captured == expected_output

    @pytest.mark.happy_path
    def test_render_syntax_tree_multiple_tokens(self, lexer, capsys):
        """Test rendering a syntax tree with multiple tokens."""
        lexer.tokens = [
            BarrelmanToken(
                line="line1",
                zone_1_declaration=None,
                zone_1_relation="relation1",
                zone_2_modifier="modifier1",
                zone_3_trigger=None,
                zone_4_outcome=None,
                indent_level=0,
                is_nesting_port=False,
            ),
            BarrelmanToken(
                line="line2",
                zone_1_declaration=None,
                zone_1_relation="relation2",
                zone_2_modifier=None,
                zone_3_trigger="trigger2",
                zone_4_outcome="outcome2",
                indent_level=1,
                is_nesting_port=True,
            ),
        ]
        lexer.render_syntax_tree()
        captured = capsys.readouterr().out
        expected_output = (
            "\nBARRELMAN SYNTAX TREE:\n\n"
            "├── relation1\n"
            "│   ├── Modifier: modifier1\n"
            "│   ├── relation2  [PORT]\n"
            "│   │   ├── Trigger: trigger2\n"
            "│   │   └── Outcome: outcome2\n"
        )
        assert captured == expected_output

    @pytest.mark.edge_case
    def test_render_syntax_tree_no_tokens(self, lexer, capsys):
        """Test rendering a syntax tree with no tokens."""
        lexer.tokens = []
        lexer.render_syntax_tree()
        captured = capsys.readouterr().out
        expected_output = "\nBARRELMAN SYNTAX TREE:\n\n"
        assert captured == expected_output

    @pytest.mark.edge_case
    def test_render_syntax_tree_token_with_no_relations(self, lexer, capsys):
        """Test rendering a syntax tree with a token having no relations."""
        lexer.tokens = [
            BarrelmanToken(
                line="line1",
                zone_1_declaration=None,
                zone_1_relation=None,
                zone_2_modifier=None,
                zone_3_trigger=None,
                zone_4_outcome=None,
                indent_level=0,
                is_nesting_port=False,
            )
        ]
        lexer.render_syntax_tree()
        captured = capsys.readouterr().out
        expected_output = "\nBARRELMAN SYNTAX TREE:\n\n├── None\n"
        assert captured == expected_output

    @pytest.mark.edge_case
    def test_render_syntax_tree_with_nesting_port(self, lexer, capsys):
        """Test rendering a syntax tree with a token marked as a nesting port."""
        lexer.tokens = [
            BarrelmanToken(
                line="line1",
                zone_1_declaration=None,
                zone_1_relation="relation1",
                zone_2_modifier=None,
                zone_3_trigger=None,
                zone_4_outcome=None,
                indent_level=0,
                is_nesting_port=True,
            )
        ]
        lexer.render_syntax_tree()
        captured = capsys.readouterr().out
        expected_output = "\nBARRELMAN SYNTAX TREE:\n\n├── relation1  [PORT]\n"
        assert captured == expected_output
