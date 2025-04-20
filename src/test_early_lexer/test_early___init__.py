import pytest

from src.lexer import BarrelmanLexer


@pytest.mark.usefixtures("setup_lexer")
class TestBarrelmanLexerInit:
    @pytest.fixture
    def setup_lexer(self):
        """Fixture to set up the lexer instance."""
        self.source_code = "zone_1: declaration\nzone_2: modifier"
        self.lexer = BarrelmanLexer(self.source_code)

    @pytest.mark.happy_path
    def test_initialization_with_valid_source(self):
        """Test that the lexer initializes correctly with valid source code."""
        assert self.lexer.source == ["zone_1: declaration", "zone_2: modifier"]
        assert self.lexer.tokens == []

    @pytest.mark.happy_path
    def test_initialization_with_empty_source(self):
        """Test that the lexer initializes correctly with an empty source string."""
        lexer = BarrelmanLexer("")
        assert lexer.source == []
        assert lexer.tokens == []

    @pytest.mark.edge_case
    def test_initialization_with_whitespace_source(self):
        """Test that the lexer handles a source string with only whitespace correctly."""
        lexer = BarrelmanLexer("   \n  \t\n")
        assert lexer.source == []
        assert lexer.tokens == []

    @pytest.mark.edge_case
    def test_initialization_with_multiline_source(self):
        """Test that the lexer correctly splits a multiline source string."""
        multiline_source = "line 1\nline 2\nline 3"
        lexer = BarrelmanLexer(multiline_source)
        assert lexer.source == ["line 1", "line 2", "line 3"]
        assert lexer.tokens == []

    @pytest.mark.edge_case
    def test_initialization_with_trailing_newlines(self):
        """Test that the lexer handles trailing newlines in the source string."""
        source_with_trailing_newlines = "line 1\nline 2\n\n"
        lexer = BarrelmanLexer(source_with_trailing_newlines)
        assert lexer.source == ["line 1", "line 2"]
        assert lexer.tokens == []

    @pytest.mark.edge_case
    def test_initialization_with_leading_newlines(self):
        """Test that the lexer handles leading newlines in the source string."""
        source_with_leading_newlines = "\n\nline 1\nline 2"
        lexer = BarrelmanLexer(source_with_leading_newlines)
        assert lexer.source == ["line 1", "line 2"]
        assert lexer.tokens == []


# To run these tests, use the command: pytest -v --tb=short
# To run these tests, use the command: pytest -v --tb=short
