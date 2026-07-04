## What does this PR do?

<!-- One or two sentences. Link the issue it closes, if any. -->

## Why?

<!-- The motivation. If it changes gameplay or quantum behavior, explain the
     physics/rules reasoning, not just the code change. -->

## How was this tested?

- [ ] `pytest` passes locally
- [ ] `ruff check .` passes locally
- [ ] New behavior is covered by a new or updated test
- [ ] If it touches the GUI: played at least one full game locally

## Checklist

- [ ] The circuit stays the ground truth (no quantum outcomes computed in the front end)
- [ ] `rules.py` still imports neither qiskit nor pygame; `backend.py` still imports no pygame
- [ ] Seeded games (`--seed`) still replay deterministically
- [ ] `CHANGELOG.md` updated under **Unreleased** (for user-visible changes)
