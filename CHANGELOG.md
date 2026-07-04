# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-07-04

First properly packaged release.

### Added
- Installable `qicqacqoe` package with a `qicqacqoe` console entry point;
  `python -m qicqacqoe` and the legacy `python main.py` also work.
- `--seed` flag: pins the Aer simulator seed so every collapse in a game is
  reproducible; `--shots` flag for majority-vote measurement experiments.
- `--log PATH` flag: exports the full move history, seed, and final board as
  JSON when the game ends, making any game replayable and reportable.
- Classical rules module (`qicqacqoe/rules.py`) with the win-line logic,
  importable without qiskit or pygame.
- Deterministic test suite for the quantum backend and the rules layer.
- CI quality gates: pytest on Python 3.10–3.13, ruff lint, and a headless
  import smoke test on every push and pull request.
- Open-source governance: CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md,
  CODEOWNERS, issue and PR templates, and this changelog.
- `DESIGN_RATIONALE.md`: a line-by-line interrogation-style defense of every
  design decision in the codebase.

### Changed
- The 20-move cap described in the README is now enforced: when reached, the
  whole board is measured and the game settles as a win or a draw.
- Measured squares are now locked against further actions, matching the
  documented rule.
- Assets moved to `qicqacqoe/assets/` and are loaded relative to the package,
  so the game runs from any working directory.

### Fixed
- **Quantum teleportation now actually teleports.** The Bell pair was being
  prepared with a Hadamard on *both* qubits before the CNOT, producing the
  unentangled state |++⟩ instead of an EPR pair — the destination square
  collapsed 50/50 regardless of the teleported state. Caught by the new
  deterministic test suite.
- **Entangled partners now display their real measured value.** Measuring a
  square only measured the *clicked* qubit in the simulation, so a collapsed
  partner's classical bit was never written and read back as its default 0 —
  partners (and, on later replays, previously measured squares) always
  displayed as "O". Every collapsed square is now measured in each run.
- **Collapsed partners are pinned in the move log.** Only the clicked square
  received a `force` instruction, so a partner's outcome could re-roll — and
  silently flip on screen — when a later measurement replayed the circuit.
  All squares that collapse are now pinned to the outcome they showed.

## Pre-1.0 history

The game was originally built for the IonQ + Microsoft joint challenge at
MIT iQuHACK 2022 (see `docs/iquhack-2022-instructions.md`) and later reworked
for modern Qiskit (2.x primitives, `if_test` classical control, AerSimulator).

[Unreleased]: https://github.com/namangoyal-work/QicQacQoe/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/namangoyal-work/QicQacQoe/releases/tag/v1.0.0
