# 0001: Implement active inference from scratch in NumPy, judged by an agent

- **Date:** 2026-11-18
- **Status:** Accepted
- **Ticket(s):** AIS-001

## Context

This project is a portfolio piece meant to show a recruiter a working understanding of active inference. The implementation has to be readable in one sitting and demonstrably the maintainer's own work.

## Options considered

1. **Use `pymdp`.**
    - Pro: fast to build, and the standard library.
    - Con: it hides the maths that the project is meant to show.
2. **JAX or PyTorch.**
    - Pro: differentiable, and scales to larger models.
    - Con: a heavy dependency for a small discrete model, and it distracts from the core ideas.
3. **NumPy from scratch.**
    - Pro: every equation is visible, there are few dependencies, and it's easy to test against brute-force oracles.
    - Con: more code to write, and it won't scale to large state spaces.

## Decision

Option 3. Runtime dependencies are limited to `numpy` and `matplotlib`.

Also decided: AI agents do not write code in this repository. They act as a **judge**, grading each ticket against its acceptance criteria and a fixed rubric (see `.claude/skills/judge/SKILL.md`), and as a tutor on request.

## Rationale and trade-offs

- The value of the project is in the clarity of the maths and the rigour of the tests, not in scale.
- An independent judge adds an external quality bar, and leaves an auditable review trail in `docs/reviews/`.

## Consequences

- Any new runtime dependency needs a superseding ADR.
- Every ticket ends with a recorded judge verdict.
