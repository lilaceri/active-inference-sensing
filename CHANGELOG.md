# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Project scaffold:
    - package stubs
    - tooling (uv, ruff, mypy, pre-commit, CI)
    - AGENTS.md, with the agent-as-judge workflow
    - CHECKLIST.md
    - documentation templates
- Tickets tracked as GitHub issues: epics #1–#9, with tickets #10–#33 as sub-issues. `CHECKLIST.md` is now an index of them.
- Issue template (Ticket) and pull request template.
- The judge now reads acceptance criteria from the ticket's issue and posts its verdict on the PR.
