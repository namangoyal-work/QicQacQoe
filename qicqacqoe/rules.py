# Classical rules of the game, kept free of qiskit and pygame so they can be
# tested without a simulator or a display.

# Every line on the 3x3 grid that wins the game
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Cols
    (0, 4, 8), (2, 4, 6),             # Diags
]

# After this many moves the whole board is measured and the game ends,
# to prevent infinite gameplay.
MOVE_CAP = 20


def find_winner(results, measured):
    # results is a list of 9 ints (0 or 1), one per square.
    # measured is the set of square indices that have collapsed.
    # A line only counts if all three of its squares are measured.
    for a, b, c in LINES:
        if a in measured and b in measured and c in measured:
            if results[a] == results[b] == results[c]:
                return "o" if results[a] == 0 else "x"
    return None
