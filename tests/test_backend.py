# Tests for the quantum backend. Every test here is deterministic: it
# either uses a circuit whose outcome is certain (probability 1), or it
# pins the Aer seed so the collapse is reproducible.

from qiskit_aer import AerSimulator

from qicqacqoe.backend import (
    extract_measured_states,
    get_measured_qubit,
    get_the_final_state,
    instruction,
)


def run(seq, shots=50, seed=123):
    backend = AerSimulator()
    qc = instruction(seq, backend)
    marginals = qc.simulate(shots, seed)
    return get_the_final_state(marginals)


# --- Single-qubit gates ---

def test_hadamard_collapses_to_o():
    # Every square starts in |+>. A second Hadamard sends it back to |0>,
    # so measuring must give 0 ("o") with probability 1.
    res = run([("hadamard", 0), ("measure", 0)])
    assert res[0] == 0


def test_sigmaz_hadamard_collapses_to_x():
    # Z|+> = |->, and H|-> = |1>, so the "plus -> X" move must give 1
    # with probability 1.
    res = run([("sigmaz", 0), ("hadamard", 0), ("measure", 0)])
    assert res[0] == 1


def test_force_pins_a_qubit():
    res = run([("force", 0, 1), ("force", 1, 0), ("measure", 0), ("measure", 1)])
    assert res[0] == 1
    assert res[1] == 0


# --- Two-qubit gates ---

def test_cnot_flips_target_when_control_is_one():
    res = run([("force", 0, 1), ("force", 1, 0), ("cnot", 0, 1), ("measure", 1)])
    assert res[1] == 1


def test_cnot_leaves_target_when_control_is_zero():
    res = run([("force", 0, 0), ("force", 1, 0), ("cnot", 0, 1), ("measure", 1)])
    assert res[1] == 0


def test_swap_exchanges_states():
    res = run([("force", 0, 1), ("force", 1, 0), ("swap", 0, 1),
               ("measure", 0), ("measure", 1)])
    assert res[0] == 0
    assert res[1] == 1


def test_entangled_pair_is_correlated():
    # Build a Bell pair and measure both halves in a single shot: the
    # outcomes must always agree, whichever way the pair collapses.
    for seed in range(10):
        res = run([("force", 0, 0), ("hadamard", 0), ("force", 1, 0),
                   ("cnot", 0, 1), ("measure", 0), ("measure", 1)],
                  shots=1, seed=seed)
        assert res[0] == res[1]


def test_teleport_moves_the_state():
    # Teleport |1> from square 0 to square 1. The mid-circuit corrections
    # make the protocol deterministic, whatever the Bell measurement gave.
    for seed in range(5):
        res = run([("force", 0, 1), ("teleport", 0, 1), ("measure", 1)],
                  shots=1, seed=seed)
        assert res[1] == 1


# --- Bookkeeping helpers ---

def test_check_measure_tracks_measured_qubits():
    backend = AerSimulator()
    qc = instruction([("hadamard", 0), ("measure", 0)], backend)
    assert qc.check_measure(0) == "measured"
    assert qc.check_measure(1) == "not measured"


def test_get_measured_qubit():
    backend = AerSimulator()
    qc = instruction([("measure", 2), ("measure", 7)], backend)
    assert get_measured_qubit(qc) == [2, 7]


def test_get_the_final_state_majority_vote():
    marginals = [{"0": 30, "1": 20} if i % 2 == 0 else {"0": 20, "1": 30}
                 for i in range(9)]
    assert get_the_final_state(marginals) == [0, 1, 0, 1, 0, 1, 0, 1, 0]


def test_extract_measured_states():
    record = [1, 0, 1, 0, 1, 0, 1, 0, 1]
    assert extract_measured_states(record, [0, 3, 8]) == {"0": 1, "3": 0, "8": 1}
