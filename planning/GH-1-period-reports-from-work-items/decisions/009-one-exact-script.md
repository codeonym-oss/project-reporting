# 009: One script for what must be exact, read-only everywhere

**Date:** 2026-11-23 (grilling, Q9; agreed: "lets go with c and these rules")

**Question:** how does `collect` read the sources?

**Decision:** **one standard-library Python script needing only git, and instructions for the other sources.**

- `window <from> <to>`: fetches, then lists what landed on the integration and production branches: first-parent merges and direct commits, with keys, people, dates and unkeyed work.
- `check <period>`: verifies a report: every item landed in the period, none was presented before, keys exist, demos point to real files, word limits hold.
- Forge: `gh` or `glab` for merge dates and descriptions, else git's dates. Tracker: whatever connector or CLI the session has, else the gap is recorded. Planning: groundwork's tree, else a configured folder.
- Nothing is ever written to the tracker or the forge.
- Only items touched in the period, and their parents, are read.
- Periods are `[from, to)` in the project's time zone; folder names show the last included day.

- **Why:** two runs must select the same items; a tracker client per vendor is not worth maintaining.
- **Not chosen:** instructions only (not repeatable); scripts for every source (credentials and one client per tracker).
