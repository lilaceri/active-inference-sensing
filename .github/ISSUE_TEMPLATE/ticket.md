---
name: Ticket
about: A unit of work with checkable acceptance criteria, graded by the judge
title: "AIS-0xx: "
labels: []
---

<!-- Attach this issue as a sub-issue of its epic (E0-E8), add an area label, and add a row to CHECKLIST.md. -->

What to build, and where (`src/aisense/...`).

## Acceptance criteria
<!-- Each criterion must be objectively checkable by the judge: a test, a command, or a file. -->
- [ ] AC1:
- [ ] AC2:

## Definition of done
- [ ] Tests written first and seen failing (RED), committed separately from the implementation
- [ ] `uv run pre-commit run --all-files` and `uv run pytest` green
- [ ] Records updated as required by the table in AGENTS.md
- [ ] Judge verdict PASS in `docs/reviews/AIS-0xx.md`
