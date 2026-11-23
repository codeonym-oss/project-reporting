# 002: Three skills: init, collect, report

**Date:** 2026-11-23 (grilling, Q2; agreed: "lets go with c and that name … the init skill helps set up the default reporting format")

**Question:** what is the plugin called, and which skills does it have?

**Decision:** **`project-reporting`, with three skills.**

- `init`: run once per project. Detects the forge, tracker, planning and demo folders; asks a few questions (report format, languages, whether the files are tracked in git, integrations); writes `config.md` and the default template.
- `collect`: reads the sources into `.work/`.
- `report [period] [--format name]`: writes a report from `.work/`, running `collect` first when the period has not been collected.

- **Why:** one collection feeds several reports, and the items can be corrected before any prose is written from them. `report` alone is still enough.
- **Not chosen:** one skill doing everything (a mistake means redoing evidence and prose together); two skills without `collect`.
