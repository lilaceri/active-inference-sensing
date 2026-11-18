# Active Inference Sensing - Agent Instructions

This file gives AI coding agents the technical context and rules for this repository. Read all of it before acting.

**Canonical sources**

- **Tickets and acceptance criteria:** GitHub issues. Each epic is a parent issue, and its tickets are sub-issues. [CHECKLIST.md](CHECKLIST.md) maps each AIS ID to its issue number.
- **Model specification:** [docs/model.md](docs/model.md)
- **Human documentation:** [README.md](README.md)
- **Judge procedure:** [.claude/skills/judge/SKILL.md](.claude/skills/judge/SKILL.md)

## Purpose of the Repository

This is a from-scratch NumPy implementation of a discrete-state **active inference** agent for **active sensing**. The agent must identify a hidden object (car, pedestrian, cyclist, background) under a hidden condition (clear or fog). Each step it chooses to query one of several noisy sensors (camera, lidar, radar), each with its own cost, or to commit to a label. It chooses by minimising expected free energy.

The repository is a **portfolio piece**. The maintainer writes every line of implementation and test code, so the work is demonstrably theirs.

## Agent Responsibilities

Agents have exactly two roles here. Neither role includes writing project code.

1. **Judge** (primary role). When asked to judge a ticket (`/judge AIS-0xx`), follow [.claude/skills/judge/SKILL.md](.claude/skills/judge/SKILL.md) exactly:
    - grade the work against the acceptance criteria in the ticket's GitHub issue and the rubric
    - give a verdict of **PASS** or **CHANGES REQUESTED**
    - record it in `docs/reviews/`, and post a summary on the ticket's PR

2. **Tutor**, on request only.
    - Explain concepts (variational free energy, expected free energy, epistemic value, message passing), derive equations, and point to references.
    - Answer with explanations, maths, pseudocode in prose, or questions that lead the maintainer to the answer.
    - Do not hand over working code for a ticket.

### Forbidden actions for agents

- Never create or modify files in `src/`, `tests/`, `experiments/` or `notebooks/`. This holds even when asked to "just fix it", unless the maintainer explicitly overrides this rule in the current message and names the file.
- Never paste a complete implementation of a stubbed function into chat, a review or a comment.
- Never weaken, skip, mark as `xfail` or delete a test.
- Never tick an acceptance criterion in a ticket's issue without a PASS verdict recorded in `docs/reviews/` for that ticket.
- Never close, reopen, merge, or edit the title or acceptance criteria of an issue or PR. Ticking boxes after a PASS and posting verdict comments are the only GitHub writes allowed.
- Never create issues unless the maintainer asks.
- Never round a verdict up. If the evidence is incomplete, the item is PARTIAL or FAIL.

### Files agents may edit

- `docs/reviews/AIS-*.md` (judge verdicts)
- on GitHub: a verdict comment on the ticket's PR, and, only after a PASS, the AC and Definition-of-done checkboxes in the ticket's issue body
- documentation outside `src/` and `tests/` (README, `docs/`, CHANGELOG, this file), only when the maintainer asks

## Build & Development Environment

### Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create the virtual environment with all dependency groups
uv sync --all-groups

# Install the git hooks (once per clone)
uv run pre-commit install
```

### Dependency information

- **Python:** 3.11+
- **Runtime:** `numpy`, `matplotlib`. Nothing else. Keep the core dependency-free beyond NumPy. No `pymdp`, `torch` or `jax` in `src/`.
- **Groups:**
    - `tests`: pytest, pytest-cov, hypothesis
    - `typing`: mypy
    - `dev`: pre-commit, ruff
- Adding any runtime dependency is a material decision. It needs an ADR under `docs/decisions/`.

## Testing

### Commands

```bash
# Full suite with coverage (mirrors CI)
uv run pytest

# A single test by node ID
uv run pytest 'tests/test_maths.py::test_softmax_sums_to_one'

# Pre-commit checks (ALWAYS run before committing)
uv run pre-commit run --all-files
```

### Strict test-driven development

1. **RED.** Before writing implementation code for any feature or bug fix, write a focused pytest test that specifies the expected behaviour or reproduces the bug. Run it by node ID and confirm it fails for the expected reason. A failure from `NotImplementedError` in the stub counts as RED. A collection error, import error or typo does not.
2. **GREEN.** Make the smallest implementation change that satisfies the test. Rerun the focused test and the affected tests.
3. **REFACTOR.** Clean up while preserving behaviour. Rerun the full suite and `pre-commit` before committing.

Commit the RED test and the GREEN implementation as **separate commits** where practical (`test: ...` then `feat: ...`). The judge uses this history as TDD evidence.

### Testing principles for numerical / probabilistic code

- **Determinism.**
    - Never use the global NumPy RNG.
    - Every stochastic function takes a `numpy.random.Generator`.
    - Tests use the seeded `rng` fixture from `tests/conftest.py`.
- **Tolerances.**
    - Compare floats with `numpy.testing.assert_allclose`, with explicit `rtol`/`atol`.
    - Justify any tolerance looser than `1e-10` in a comment (e.g. Monte Carlo error ~ 1/sqrt(N)).
- **Probability invariants.** Assert them explicitly:
    - distributions are non-negative and sum to 1 along the documented axis
    - likelihood columns are normalised
    - entropies are non-negative
    - KL divergence is ≥ 0, and 0 only for identical inputs
- **Independent oracles.** Test inference and planning against a separately computed reference: brute-force Bayes over the joint, or mutual information computed from the joint distribution. Don't test them against the same formula restated.
- **Edge cases.**
    - one-hot and uniform beliefs
    - zero-probability entries (log of 0)
    - an uninformative sensor (uniform likelihood, so information gain is 0)
    - horizon 1
- **Property-based tests** with `hypothesis` are encouraged for maths utilities.
- **Behavioural tests** (the agent stops querying when confident, the epistemic ablation performs worse):
    - use fixed seeds and a small number of episodes
    - assert on aggregate statistics with a margin, not on single trajectories
    - keep benchmark-scale runs in `experiments/`, never in `tests/`
- **Forbidden:**
    - weakening an assertion to make code pass
    - `pytest.skip` or `xfail` to bypass a failure
    - deleting a failing test

## Code Quality & Linting

```bash
# Always run the full suite of hooks (not individual tools)
uv run pre-commit run --all-files
```

The hooks run `ruff check --fix`, `ruff format`, `mypy --strict` on `src/`, and whitespace/YAML checks. CI runs the same hooks. A PR with failing hooks is not reviewable.

## Project Structure

```
src/aisense/
  constants.py          # every tunable number (horizon, precision, costs, sensor accuracies)
  maths.py              # pure numerical utilities (softmax, log, entropy, KL, factor dot products)
  generative_model.py   # dataclasses + builders for A, B, C, D (the agent's beliefs about the world)
  env.py                # the generative process (the true world the agent interacts with)
  agent.py              # state inference, expected free energy, policy inference, action selection
  baselines.py          # comparison agents (random, fixed-order, pragmatic-only ablation)
tests/                  # mirrors src/aisense/, one test module per source module
experiments/            # CLI scripts producing results/ figures and CSVs
docs/model.md           # the mathematical specification; code must match it
docs/decisions/         # ADRs
docs/experiments/       # experiment records
docs/reviews/           # judge verdicts, one file per ticket
results/                # committed figures and small CSVs only
```

## Architecture & Conventions

### Key patterns

- **Functional core, thin shell.**
    - Everything in `maths.py`, `generative_model.py` and `agent.py` is a pure function of arrays and dataclasses.
    - State lives only in `env.py` and in experiment loops.
- **Generative model vs generative process.** Keep these separate.
    - `generative_model.py` is what the agent *believes*.
    - `env.py` is what is *true*.
    - They may share sensor specs, but code in `agent.py` must never read from `env.py`.
- **Array conventions** (document every deviation in a docstring):
    - `A[m]` has shape `(num_obs[m], *num_states)`, and normalises over axis 0.
    - `B[f]` has shape `(num_states[f], num_states[f], num_actions)`, laid out as `B[next, prev, action]`, and normalises over axis 0.
    - `C[m]` has shape `(num_obs[m],)` and holds log-preferences (nats).
    - `D[f]` has shape `(num_states[f],)`.
    - Beliefs are lists of 1-D arrays, one per state factor (mean-field).
- **Log space.**
    - Use `maths.log_stable` (clipped log) everywhere instead of `np.log`, to avoid `-inf` on zero entries.
    - Use `maths.softmax` with max-subtraction.
- **Constants.** No magic numbers in `src/`. Every tunable value lives in `constants.py`, and tests import it from there.
- **Notation.** Variable names follow `docs/model.md`: `qs` (posterior over states), `G` (expected free energy), `gamma` (policy precision), `E` (habit prior). Equations in docstrings use the same symbols.

### Type hints & docstrings

- `mypy --strict` must pass on `src/`. Use `numpy.typing.NDArray[np.float64]` for arrays.
- Every public function has a NumPy-style docstring with:
    - Parameters (with shapes)
    - Returns (with shapes)
    - the equation implemented, in plain text or LaTeX
    - Raises
- Keep docstrings in sync with the implementation and with `docs/model.md`.

### File header

None required.

## Documentation Required for Each Change

Keep documentation in the same PR as the change.

| Record | When to update it | What to include |
| --- | --- | --- |
| Changelog | Any user-visible change: behaviour, API, configuration, dependencies | An entry under `[Unreleased]` in `CHANGELOG.md` (Added / Changed / Fixed / Removed). |
| Decision log | A material choice about model structure, inference scheme, planning horizon, evaluation design or dependencies | A dated ADR in `docs/decisions/NNNN-title.md` from the template, with context, options, rationale, trade-offs, consequences and status. Link superseded ADRs. |
| Experiment log | Any run used to support a claim in the README | A dated record in `docs/experiments/` from the template, with hypothesis, baseline, commit SHA, config and seeds, exact command, metrics, conclusion and limitations. Record failed and inconclusive runs too. |
| Model spec | Any change to the generative model, inference or planning maths | Update `docs/model.md` so code and maths agree. |
| Review | Every completed ticket | The judge verdict in `docs/reviews/AIS-0xx.md`. |

## Common Workflows

### Working a ticket

1. Find the ticket's issue number in `CHECKLIST.md`, and read its acceptance criteria in the issue.
2. Branch: `git switch -c feat/AIS-0xx-short-name`.
3. RED → GREEN → REFACTOR (see above), committing tests and implementation separately.
4. Update the records required by the table above.
5. Run `uv run pre-commit run --all-files` and `uv run pytest`.
6. Open a PR from the template, with `Closes #N` in the description.
7. Ask the judge: `/judge AIS-0xx`.
8. On CHANGES REQUESTED, address the blocking items and re-judge. On PASS, merge. The issue closes automatically, and the epic's progress bar updates.

### Adding a ticket

Use the **Ticket** issue template, attach the issue as a sub-issue of its epic, add an area label, and add a row to `CHECKLIST.md`. Every acceptance criterion must be objectively checkable.

### Commit messages

Use Conventional Commits with the ticket ID:

- `test(maths): softmax normalisation [AIS-010]`
- `feat(maths): implement softmax [AIS-010]`

### Security considerations

There are no secrets in this repository. Don't commit large artifacts: keep files in `results/` under ~1 MB each.

## CI/CD Workflows

`.github/workflows/ci.yml` runs on every push and PR:

1. `uv sync --all-groups`
2. `pre-commit run --all-files`
3. `pytest` with coverage

All three must be green before merge.

---

**Note:** This file is for AI agents. For the project overview see README.md. For the work plan see the GitHub issues, indexed in CHECKLIST.md.
