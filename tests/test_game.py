# Game-level tests, run headless against a dummy SDL display. They drive
# the same module-level move functions the mouse handlers call, so the
# board mirror, the gate log, and the simulator are all exercised together.

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from qicqacqoe import game  # noqa: E402


def setup_game(seed):
    game.load_display()
    game.game_initiating_window()
    game.seed = seed
    game.shots = 1
    game.log_path = None
    game.board[:] = [["ox", (255, 255, 255)] for _ in range(9)]
    game.gates.clear()
    game.steps = 0
    game.game_over = False
    game.color = 1


def symbol_bit(sym):
    return 0 if sym == "o" else 1


def test_bell_measurement_pins_both_partners():
    setup_game(seed=7)

    # Square 1 -> |0>, then CNOT with square 0 (still |+>) as control:
    # that is a Bell pair, so the two squares must collapse together.
    game.plus2o(1)
    game.cnot(1, 0)
    game.measure(0)

    assert game.board[0][1] == game.MEASURE_COLOR
    assert game.board[1][1] == game.MEASURE_COLOR
    assert game.board[0][0] == game.board[1][0]  # Bell correlation

    # Both halves of the pair must be pinned in the move log, so a later
    # replay can never re-roll them.
    forced = {g[1]: g[2] for g in game.gates if g[0] == "force"}
    assert forced[0] == symbol_bit(game.board[0][0])
    assert forced[1] == symbol_bit(game.board[1][0])


def test_partner_outcome_survives_later_measurements():
    setup_game(seed=11)

    game.plus2o(1)
    game.cnot(1, 0)
    game.measure(0)
    partner_symbol = game.board[1][0]

    # Measuring an unrelated square replays the whole circuit; the pinned
    # partner must come out of the replay unchanged.
    game.measure(4)
    assert game.board[1][0] == partner_symbol
