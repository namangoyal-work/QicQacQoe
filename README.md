# Qic Qac Qoe

**Tic Tac Toe, except every square is a real (simulated) qubit.**

[![CI](https://github.com/namangoyal-work/QicQacQoe/actions/workflows/ci.yml/badge.svg)](https://github.com/namangoyal-work/QicQacQoe/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)
[![Qiskit](https://img.shields.io/badge/built%20on-Qiskit%20%2B%20Aer-6929c4.svg)](https://www.ibm.com/quantum/qiskit)

## Overview

This is a quantum version of the classic two-player game, Tic Tac Toe. The game
is played on a 3x3 grid where each square is a qubit initialized to the state:

<img src="https://latex.codecogs.com/svg.image?|\psi_0\rangle=\frac{1}{\sqrt{2}}(|0\rangle&plus;|1\rangle)" title="|\psi_0\rangle=\frac{1}{\sqrt{2}}(|0\rangle+|1\rangle)" />

One player wins with 0's ("O"), the other with 1's ("X") — but until a square is
*measured*, it isn't an O or an X. It's a live quantum state you can rotate,
entangle with other squares, swap, and even teleport across the board. Every
move you make is appended to a real Qiskit circuit, and every measurement is a
genuine simulated wavefunction collapse in Aer. The board on screen is only a
mirror; **the circuit is the ground truth.**

## Install and play

```bash
git clone https://github.com/namangoyal-work/QicQacQoe.git
cd QicQacQoe
python3 -m venv .venv && source .venv/bin/activate
pip install .
qicqacqoe
```

Useful flags:

```bash
qicqacqoe --seed 42            # pin the simulator seed: every collapse is reproducible
qicqacqoe --shots 101          # majority-vote measurement (default 1 shot = one true collapse)
qicqacqoe --log game.json      # export the full move history as JSON when the game ends
```

`python -m qicqacqoe` and the legacy `python main.py` also work.

## The moves

Upon each turn, a player may perform one of six possible moves:

#### 1) Measurement

The player measures any state on the board in the <img src="https://latex.codecogs.com/svg.image?\{|0\rangle,|1\rangle\}" title="\{|0\rangle,|1\rangle\}" /> basis. The state on the board hence collapses into the measured state. If the square was entangled with others, its partners collapse with it — instantly, across the whole board. Once measured, a square is locked: no further actions may be performed on it.

Additionally, the player may apply single-qubit gates on a particular quantum state:

#### 2) Hadamard gate

The player selects one qubit and applies

<img src="https://latex.codecogs.com/svg.image?H&space;=&space;\frac{1}{\sqrt{2}}\begin{bmatrix}1&space;&&space;1&space;\\&space;1&space;&&space;-1\end{bmatrix}" title="H = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1 \\ 1 & -1\end{bmatrix}" />

Since every square starts in |+⟩, this deterministically steers it to |0⟩. It is represented by the "plus → O" gate in the game.

#### 3) Z gate followed by Hadamard gate

The player selects one qubit and applies

<img src="https://latex.codecogs.com/svg.image?H\sigma_z&space;=&space;\frac{1}{\sqrt{2}}\begin{bmatrix}1&space;&&space;-1&space;\\&space;1&space;&&space;1\end{bmatrix}" title="H\sigma_z = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & -1 \\ 1 & 1\end{bmatrix}" />

Z|+⟩ = |−⟩ and H|−⟩ = |1⟩, so this deterministically steers a fresh square to |1⟩. It is represented by the "plus → X" gate in the game.

#### 4) Controlled NOT gate

The player selects two qubits, and applies

<img src="https://latex.codecogs.com/svg.image?CNOT&space;=&space;\begin{bmatrix}1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0\end{bmatrix}" title="CNOT = \begin{bmatrix}1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0\end{bmatrix}" />

This may result in the two states becoming entangled with each other. Entangled squares are shown in a shared color — measure one and its partner collapses too.

#### 5) SWAP gate

<img src="https://latex.codecogs.com/svg.image?SWAP&space;=&space;\begin{bmatrix}1&0&0&0\\0&0&1&0\\0&1&0&0\\0&0&0&1\end{bmatrix}" title="SWAP = \begin{bmatrix}1&0&0&0\\0&0&1&0\\0&1&0&0\\0&0&0&1\end{bmatrix}" />

Finally, to showcase the full range of the capabilities of quantum computation, the player may also teleport a quantum state across the board:

#### 6) Quantum teleportation

Each player carries an ancillary qubit m, which can be used to form an EPR pair with another state on the grid j and teleport an existing state at square i to j. A CNOT gate is applied to qubit i and m (i is the control qubit and m is the target qubit). After applying Hadamard to qubit i, we measure both qubits i and m, then apply the classically-controlled X and Z corrections to j.

Such a move would not be possible with classical bits.

## Gameplay

Gameplay begins by running `qicqacqoe`, upon which the players will see an initialized board, with buttons for each action that may be performed on the qubits.

<img src="https://user-images.githubusercontent.com/36899444/151707898-f3802d94-4efb-49a3-8b3c-efc35ef1d69c.png" width="200" >

The player may then select a qubit and a possible operation on the qubit from the selection menu.

<img src="https://user-images.githubusercontent.com/36899444/151708033-9edd71f7-ff19-4f60-97af-f4cccc249fe4.png" width="200" >

Each player takes turns, performing actions on the qubits.

<img src="https://user-images.githubusercontent.com/36899444/151708161-5fcb9572-ef5a-4a6f-a8a9-5d10fabf7e43.png" width="200" >

The winner is the first player to own a fully-measured line of three matching
symbols. Once a state has been measured, no further actions may be performed on
it. After 20 moves the entire board is measured automatically and the game is
settled as a win or a draw (to prevent infinite gameplay).

## How it works

```
click ──► game.py (pygame UI)  ──►  gates log  ──►  backend.py (Qiskit)
              │                    (the move                │
              │                     history)                ▼
        board mirror  ◄──────  measurement  ◄──────  AerSimulator
        (what you see)          results              (the ground truth)
```

- **`qicqacqoe/game.py`** — the pygame front end. It never computes a quantum
  outcome itself; every move appends an instruction to the `gates` log.
- **`qicqacqoe/backend.py`** — builds a 13-qubit Qiskit circuit (9 board
  squares + ancillas) from the gate log and runs it on `AerSimulator`,
  including mid-circuit measurement and classically-controlled corrections
  (`if_test`) for teleportation. On every measurement the *entire game so far*
  is replayed, so entanglement between any set of squares is always honored.
- **`qicqacqoe/rules.py`** — the classical layer: win lines and the move cap.
  Imports neither qiskit nor pygame, so it is trivially testable.

Why these decisions were made — and what breaks if you change them — is
documented, decision by decision, in **[DESIGN_RATIONALE.md](DESIGN_RATIONALE.md)**.

## Repository layout

```
qicqacqoe/          the game package
  backend.py        quantum layer: circuit building + simulation
  game.py           pygame front end + CLI entry point
  rules.py          classical rules: win lines, move cap
  assets/           board and button sprites
tests/              deterministic quantum + rules test suite
docs/               historical iQuHACK 2022 challenge instructions
.github/            CI workflow, CODEOWNERS, issue/PR templates
```

## Development

```bash
pip install -e ".[dev]"
pytest            # deterministic quantum test suite
ruff check .      # lint
```

Every push runs the same gates in CI across Python 3.10–3.13. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the quality gates and design ground
rules, and [SECURITY.md](SECURITY.md) for the security policy.

## Resources

This game is inspired by

M. Nagy and N. Nagy, "Quantum Tic-Tac-Toe: A Genuine Probabilistic Approach," Applied Mathematics, Vol. 3 No. 11A, 2012, pp. 1779-1786. doi: 10.4236/am.2012.331243.

In this project, I have extended their ideas and implemented additional gates and actions. The project began at the IonQ + Microsoft joint challenge at MIT iQuHACK 2022 (the original challenge brief is preserved in [docs/iquhack-2022-instructions.md](docs/iquhack-2022-instructions.md)) and has since been reworked for modern Qiskit.

## License

[MIT](LICENSE) © Naman Goyal
