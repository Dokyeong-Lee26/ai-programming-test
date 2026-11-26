import pytest

from week11.bug3_logic import count_pass, find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([70, 85, 60, 95], 95),
        ([42], 42),
        ([-8, -3, -10], -3),
        ([5, 9, 9, 2], 9),
        ([1, 2, 30], 30),
    ],
)
def test_find_max_returns_largest_score(scores, expected):
    assert find_max(scores) == expected


def test_find_max_raises_index_error_for_empty_scores():
    with pytest.raises(IndexError):
        find_max([])


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([70, 85, 60, 95], 4),
        ([59, 60, 61], 2),
        ([0, 59, 60], 1),
        ([], 0),
    ],
)
def test_count_pass_includes_scores_at_cutoff(scores, expected):
    assert count_pass(scores) == expected


def test_count_pass_uses_custom_cutoff_inclusively():
    assert count_pass([69, 70, 71], cutoff=70) == 2