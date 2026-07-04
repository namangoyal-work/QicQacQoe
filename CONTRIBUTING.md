# Contributing to Qic Qac Qoe

Thanks for wanting to make quantum tic-tac-toe better. This document tells you
how to set up a development environment, what the quality gates are, and what a
good pull request looks like here.

## Development setup

```bash
git clone https://github.com/namangoyal-work/QicQacQoe.git
cd QicQacQoe
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the game:

```bash
qicqacqoe                      # or: python -m qicqacqoe
qicqacqoe --seed 42            # reproducible collapses
qicqacqoe --log game.json      # export the move history on exit
```

Run the checks (the same ones CI runs):

```bash
pytest          # deterministic quantum test suite
ruff check .    # lint
```

## Quality gates

Every pull request must pass all of these before merge. They run automatically
in GitHub Actions on every push and PR:

| Gate | Command | What it protects |
| --- | --- | --- |
| Tests | `pytest` | The quantum backend and the classical rules. Tests must stay **deterministic**: use circuits with probability-1 outcomes, or pin the Aer seed. A flaky quantum test is a bug in the test. |
| Lint | `ruff check .` | Consistent, readable Python across the project. |
| Headless import | `SDL_VIDEODRIVER=dummy python -c "import qicqacqoe.game"` | The GUI module must stay importable without a display, so CI can catch import-time regressions. |
| Python matrix | CI runs 3.10–3.13 | The game keeps working on every supported Python. |

If you add a feature, add a test. If you fix a bug, add the test that would
have caught it — that is how the teleportation Bell-pair bug was found, and the
test that caught it now guards the fix forever.

## Design ground rules

A few invariants that PRs must not break (the full reasoning lives in
[DESIGN_RATIONALE.md](DESIGN_RATIONALE.md)):

1. **The circuit is the ground truth.** The GUI `board` is only a *mirror* for
   drawing; every game-changing action must append to the `gates` move log, and
   outcomes must come from replaying that log through the simulator. Never
   compute a quantum outcome in the front end.
2. **The rules layer stays classical.** `qicqacqoe/rules.py` must import
   neither qiskit nor pygame, so it stays trivially testable.
3. **The backend stays display-free.** `qicqacqoe/backend.py` must not import
   pygame, so it runs headless in tests and CI.
4. **Determinism is a feature.** Anything that touches randomness must respect
   `--seed`; a seeded game must replay identically.

## Style

- Match the existing code: plain, procedural Python with descriptive names and
  comments that explain *why*, not *what*.
- Keep functions small and single-purpose; the move functions
  (`plus2o`, `cnot`, `teleport`, …) are the pattern to follow.
- `ruff` settings live in `pyproject.toml`; run `ruff check --fix .` before
  pushing.

## Commits and pull requests

- Write commit messages with a short imperative subject line and a body that
  explains the why. The git history of this repo is the model.
- One logical change per commit; one topic per PR.
- Fill in the PR template, including the "How was this tested?" section.
- CODEOWNERS automatically requests review from the maintainer; expect review
  feedback on anything touching `backend.py` — the quantum layer is where
  subtle bugs hide.

## Reporting bugs and proposing features

Use the issue templates. For bugs, a `--seed` value plus the `--log` JSON of
the offending game makes your report exactly reproducible, which usually cuts
the fix time from days to minutes.

## Security

Please do not open public issues for security-sensitive reports; see
[SECURITY.md](SECURITY.md).

## Code of conduct

Everyone interacting in this project's spaces is expected to follow the
[Code of Conduct](CODE_OF_CONDUCT.md).
