import pytest

from src.lexer import BarrelmanLexer


@pytest.mark.parametrize(
    "modifier, trigger, expected",
    [
        # Happy path tests
        ("mod1", "trig1", "Outcome inferred from % mod1 -> trig1"),
        ("mod2", None, "Modifier only outcome: mod2"),
        (None, "trig2", "Trigger only outcome: trig2"),
        (None, None, None),
    ],
)
@pytest.mark.happy_path
def test_infer_outcome_happy_paths(modifier, trigger, expected):
    """
    Test infer_outcome method for typical cases with various combinations of modifier and trigger.
    """
    lexer = BarrelmanLexer("")
    result = lexer.infer_outcome(modifier, trigger)
    assert result == expected


@pytest.mark.parametrize(
    "modifier, trigger, expected",
    [
        # Edge case tests
        ("", "trig3", "Trigger only outcome: trig3"),  # Empty modifier
        ("mod3", "", "Modifier only outcome: mod3"),  # Empty trigger
        ("", "", None),  # Both empty
        (
            "mod4",
            "trig4",
            "Outcome inferred from % mod4 -> trig4",
        ),  # Both non-empty but valid
    ],
)
@pytest.mark.edge_case
def test_infer_outcome_edge_cases(modifier, trigger, expected):
    """
    Test infer_outcome method for edge cases, including empty strings and both parameters being empty.
    """
    lexer = BarrelmanLexer("")
    result = lexer.infer_outcome(modifier, trigger)
    assert result == expected


class TestBarrelmanLexerInferOutcome:
    """
    Test class for BarrelmanLexer.infer_outcome method.
    """

    @pytest.mark.happy_path
    def test_infer_outcome_both_present(self):
        """
        Test when both modifier and trigger are present.
        """
        lexer = BarrelmanLexer("")
        result = lexer.infer_outcome("mod1", "trig1")
        assert result == "Outcome inferred from % mod1 -> trig1"

    @pytest.mark.happy_path
    def test_infer_outcome_modifier_only(self):
        """
        Test when only modifier is present.
        """
        lexer = BarrelmanLexer("")
        result = lexer.infer_outcome("mod2", None)
        assert result == "Modifier only outcome: mod2"

    @pytest.mark.happy_path
    def test_infer_outcome_trigger_only(self):
        """
        Test when only trigger is present.
        """
        lexer = BarrelmanLexer("")
        result = lexer.infer_outcome(None, "trig2")
        assert result == "Trigger only outcome: trig2"

    @pytest.mark.happy_path
    def test_infer_outcome_none(self):
        """
        Test when both modifier and trigger are None.
        """
        lexer = BarrelmanLexer("")
        result = lexer.infer_outcome(None, None)
        assert result is None

    @pytest.mark.edge_case
    def test_infer_outcome_empty_modifier(self):
        """
        Test when modifier is an empty string and trigger is present.
        """
        lexer = BarrelmanLexer("")
        result = lexer.infer_outcome("", "trig3")
        assert result == "Trigger only outcome: trig3"

    @pytest.mark.edge_case
    def test_infer_outcome_empty_trigger(self):
        """
        Test when trigger is an empty string and modifier is present.
        """
        lexer = BarrelmanLexer("")
        result = lexer.infer_outcome("mod3", "")
        assert result == "Modifier only outcome: mod3"

    @pytest.mark.edge_case
    def test_infer_outcome_both_empty(self):
        """
        Test when both modifier and trigger are empty strings.
        """
        lexer = BarrelmanLexer("")
        result = lexer.infer_outcome("", "")
        assert result is None

    @pytest.mark.edge_case
    def test_infer_outcome_both_non_empty(self):
        """
        Test when both modifier and trigger are non-empty strings.
        """
        lexer = BarrelmanLexer("")
        result = lexer.infer_outcome("mod4", "trig4")
        assert result == "Outcome inferred from % mod4 -> trig4"
