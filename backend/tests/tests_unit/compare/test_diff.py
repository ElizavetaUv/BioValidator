import pytest

from src.errors import BioValidatorInternalError


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("3.14", 3.14),
        ("42", 42.0),
        ("not a number", None),
        (3.14, 3.14),
        (None, None),
        ("\n3.14\t", 3.14),
    ]
)
def test_try_float(input_value, expected):
    from src.services.metric_sample import try_float
    assert try_float(input_value) == expected

@pytest.mark.parametrize(
    "value, ndigits, expected",
    [
        (3.14159, 2, "3.14"),
        (3.145, 2, "3.15"),
        (-2.71828, 3, "-2.718"),
    ]
)
def test_strround(value, ndigits, expected):
    from src.services.metric_sample import _strround
    assert _strround(value, ndigits) == expected

@pytest.mark.parametrize(
    "curval, comval, ndigits, eps, expected",
    [
        # Case: Both values are None
        (None, None, 3, 0.001, pytest.raises(BioValidatorInternalError, match="There is an error with algorithm")),

        # Case: curval is not None, comval is None
        ("42", None, 3, 0.001, "42 (deleted)"),

        # Case: curval is None, comval is not None
        (None, "42", 3, 0.001, "42 (added)"),

        # Case: curval and comval are equal strings
        ("42", "42", 3, 0.001, "42 (unchanged)"),

        # Case: curval and comval are equal numbers as strings

        ("3.140", "3.140", 3, 0.001, "3.140 (unchanged)"),

        # Case: curval and comval differ significantly
        ("3.140", "3.150", 3, 0.001, "+0.01"),

        # Case: curval and comval differ but within epsilon
        ("3.140", "3.1405", 3, 0.001, "3.140 (unchanged)"),

        # Case: curval and comval are invalid for float conversion
        ("invalid", "invalid", 3, 0.001, "invalid (unchanged)"),
        ("invalid", "42", 3, 0.001, "invalid (42)"),
        ("42", "invalid", 3, 0.001, "42 (invalid)"),

        # Case: Signs in the difference
        ("42", "40", 2, 0.001, "-2.0"),
        ("40", "42", 2, 0.001, "+2.0"),

        # Case: Edge cases with None and invalid strings
        (None, "invalid", 3, 0.001, "invalid (added)"),
        ("invalid", None, 3, 0.001, "invalid (deleted)"),
    ]
)
def test_get_diff(curval, comval, ndigits, eps, expected, mock_dramatiq_broker):
    from src.services.metric_sample import get_diff
    if isinstance(expected, str):
        assert get_diff(curval, comval, ndigits, eps) == expected
    else:
        with expected:
            get_diff(curval, comval, ndigits, eps)
