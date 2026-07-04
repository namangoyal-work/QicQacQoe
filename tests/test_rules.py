# Tests for the classical rules layer: pure functions, no simulator needed.

from qicqacqoe.rules import LINES, MOVE_CAP, find_winner


def test_all_eight_lines_present():
    assert len(LINES) == 8


def test_move_cap_matches_readme():
    assert MOVE_CAP == 20


def test_row_of_zeros_wins_for_o():
    results = [0, 0, 0, 1, 1, 0, 1, 0, 1]
    assert find_winner(results, {0, 1, 2}) == "o"


def test_column_of_ones_wins_for_x():
    results = [1, 0, 0, 1, 0, 0, 1, 0, 0]
    assert find_winner(results, {0, 3, 6}) == "x"


def test_diagonal_win():
    results = [0, 1, 1, 1, 0, 1, 1, 1, 0]
    assert find_winner(results, {0, 4, 8}) == "o"


def test_line_needs_all_three_squares_measured():
    # Two measured zeros and one unmeasured zero is not a win yet:
    # the third square is still in superposition.
    results = [0, 0, 0, 1, 1, 0, 1, 0, 1]
    assert find_winner(results, {0, 1}) is None


def test_no_winner_on_mixed_board():
    results = [0, 1, 0, 1, 0, 1, 1, 0, 1]
    assert find_winner(results, set(range(9))) is None
