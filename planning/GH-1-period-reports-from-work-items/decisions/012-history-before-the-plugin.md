# 012: Work presented before the plugin is listed, not rebuilt

**Date:** 2026-11-23 (grilling, Q12; agreed: "ok")

**Question:** what happens to reports made before the plugin?

**Decision:** **their keys go in an optional `presented-before.md` (key, date), which `check` reads.** Old reports are not converted and `.work/` is not backfilled.

- **Why:** it prevents repeats at almost no cost.
- **Not chosen:** converting old reports.
