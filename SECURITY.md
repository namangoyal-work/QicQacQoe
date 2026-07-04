# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| 1.x (current `main`) | ✅ |
| anything earlier | ❌ |

## Reporting a vulnerability

Please report security issues privately via
[GitHub private vulnerability reporting](https://github.com/namangoyal-work/QicQacQoe/security/advisories/new)
rather than opening a public issue. You can expect an acknowledgement within a
week. Please include reproduction steps; a `--seed` value and a `--log` JSON
file make reports exactly reproducible.

## Threat model — what this project is and is not

Qic Qac Qoe is a **local, offline desktop game**. It opens no network sockets,
runs no server, executes no untrusted input, and stores no credentials or
personal data. The realistic security surface is small and worth stating
honestly:

**In scope:**
- **Dependency supply chain.** The game executes qiskit, qiskit-aer, and
  pygame. Dependencies are declared with lower bounds in `pyproject.toml` and
  installed from PyPI; a compromised or vulnerable dependency is the most
  plausible real risk, and dependency-related reports are welcome.
- **File writes.** `--log PATH` writes a JSON file to a user-supplied path.
  It writes exactly one file, to exactly the path given, and never executes
  its content.
- **Anything that makes the game execute unexpected code** — e.g. through a
  crafted asset file or a malicious game-log path.

**Out of scope:**
- Cheating at quantum tic-tac-toe. The game trusts both players at the same
  keyboard; there is no anti-cheat and none is planned.
- Denial of service against your own machine (e.g. absurd `--shots` values
  make the simulator slow — that is the physics working as intended).
- The hackathon-era Azure workspace identifiers preserved in
  `docs/iquhack-2022-instructions.md`. These are historical event-instruction
  artifacts from iQuHACK 2022, not live credentials of this project.

## Disclosure

Confirmed vulnerabilities are fixed on `main`, noted in `CHANGELOG.md`, and
credited to the reporter unless anonymity is requested.
