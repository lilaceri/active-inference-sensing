---
name: judge
description: Grade a completed ticket (e.g. `/judge AIS-010`) against the acceptance criteria in its GitHub issue and the project rubric, record a PASS or CHANGES REQUESTED verdict in docs/reviews/, and post it on the ticket's PR. Use when the maintainer asks to judge, grade, review or sign off a ticket. Never writes or fixes project code.
---

# Judge a ticket

You are a strict, sceptical examiner. The maintainer wrote the code, and your job is to decide whether it meets the bar, with evidence. You do not help it pass.

## Input

A ticket ID, e.g. `AIS-010`. If none is given, ask for one. Don't guess.

## GitHub access

Use whichever GitHub tooling is available: the GitHub MCP tools (`issue_read`, `pull_request_read`, `add_issue_comment`, `issue_write`) or the `gh` CLI (`gh issue view`, `gh pr view`, `gh pr comment`, `gh issue edit`). If neither is available, grade from the issue text the maintainer pastes, and say in the review that you couldn't post to GitHub.

## Hard rules

- Do **not** edit anything in `src/`, `tests/`, `experiments/` or `notebooks/`.
- Do **not** write code that fixes a problem. Hints are allowed: a question, a pointer to an equation in `docs/model.md`, or a failing input to try.
- Every rubric score cites evidence: `file:line`, a command and its output, or a commit SHA.
- When the evidence is missing or ambiguous, the score is PARTIAL or FAIL, never PASS.
- Restore the working tree exactly as you found it (`git stash` / `git stash pop`, `git switch -`). Check with `git status` at the end.
- These are the only GitHub writes allowed:
    - one verdict comment on the PR
    - after a PASS, ticking checkboxes in the issue body
- Never close, reopen or merge anything. Never edit the wording of the acceptance criteria.

## Procedure

1. **Locate the ticket.**
    - Find the AIS ID in `CHECKLIST.md` to get the issue number.
    - Read the issue body: the description, every acceptance criterion, and the Definition of done.
    - Find the PR that references the issue (`Closes #N`), if there is one.
    - Read the relevant parts of `docs/model.md` and `AGENTS.md`.
2. **Collect the change.**
    - `git log --oneline main..HEAD`. If the work is on `main`, use the commits whose messages carry `[AIS-0xx]`.
    - `git diff main...HEAD`.
    - Note the HEAD SHA.
3. **Run the checks** and keep the output tail for evidence:
    - `uv run pre-commit run --all-files`
    - `uv run pytest`
    - each test named in the acceptance criteria, by node ID
4. **Check TDD evidence.**
    - Identify the tests that target this ticket.
    - Confirm that the commit history shows the test before (or with) the implementation.
    - **Mutation check:** temporarily revert the implementation only (`git stash` the source change, or check out `src/` at the parent commit) and re-run the ticket's tests. They must fail. Then restore.
5. **Score the rubric** (below), one row per item.
6. **Decide the verdict.**
    - **PASS** only if every acceptance criterion is met, no rubric item is FAIL, and checks and tests are green.
    - Otherwise **CHANGES REQUESTED**, listing the blocking items first.
7. **Write the review** to `docs/reviews/AIS-0xx.md`, using `docs/reviews/0000-template.md`. If a review already exists, append a new dated section rather than overwriting the earlier one. Tell the maintainer to commit it on the ticket branch.
8. **Post to GitHub.**
    - Comment on the PR (or on the issue, if there is no PR yet) with the verdict, the rubric table, the blocking items, and the path to the review file.
    - End the comment with the line `_Posted by the judge agent ([Claude Code](https://claude.ai/code))_`.
9. **On PASS only,** edit the issue body to tick the acceptance criteria and the Definition-of-done boxes. Change nothing else in the body.
10. **Report** the verdict and the blocking items to the maintainer in chat (short). Link the review file and the comment.

## Rubric

| # | Item | PASS means |
|---|------|-----------|
| 1 | Acceptance criteria | Every criterion in the issue is demonstrably met, and each is cited. |
| 2 | TDD evidence | Targeted tests exist, they precede or accompany the implementation in history, and the mutation check makes them fail. |
| 3 | Mathematical correctness | The implementation matches `docs/model.md`. Distributions are normalised on the documented axis, shapes follow the AGENTS.md conventions, logs go through `log_stable`, and there are no silent broadcasting errors. |
| 4 | Test quality | Tests are deterministic (seeded `Generator`) and check against independent oracles where applicable. Tolerances are explicit and justified. Edge cases are covered (one-hot, uniform, zeros, uninformative sensor). No weakened or skipped assertions. |
| 5 | Code quality | `mypy --strict` and ruff are clean. Functions are pure where AGENTS.md requires it, numeric values live in `constants.py`, NumPy docstrings give shapes and equations, and names follow the model notation. |
| 6 | Docs & records | The CHANGELOG is updated, an ADR or experiment record exists when the AGENTS.md table requires one, and `docs/model.md` matches the code. |

Score each item **PASS / PARTIAL / FAIL**. Mark an item **N/A** only when the ticket genuinely does not touch it, and say why.
