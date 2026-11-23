# project-reporting: notes for coding agents

- Public plugin `project-reporting` (skills `init`, `collect`, `report`). Read `references/structure.md` first, then
  the decisions in `planning/`.
- **Nothing from a real project** in code, tests, docs or issues: examples use the invented Acme Shop.
- Short: a `SKILL.md` stays under 100 lines. A rule lives in one place, `references/`.
- `scripts/tracking.py` is standard-library Python and needs only git. Every rule it enforces has a test.
- `main` is protected: branch `<n>-short-name`, pull request with a conventional-commit title and `Fixes #<n>`. Never
  edit `VERSION` or the manifests' version by hand after 0.1.0 (release-please does).
- Tests: `make test`; manifest and skills: `claude plugin validate .`.
- Commits and pull requests carry no AI attribution.
