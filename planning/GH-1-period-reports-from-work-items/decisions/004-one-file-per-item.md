# 004: One file per work item: Context, Findings, Gaps

**Date:** 2026-11-23 (grilling, Q4; agreed: "lets go with b")

**Question:** what does an item hold?

**Decision:** **one `item.md`.**

- **Header:** key, title, kind (`epic | story | ticket | bug | untracked`), parent, people, `started`, `landed`, `released`, area, demo.
- **Context** (five lines at most): Why, Before, Now, Gain, How. Every line rests on a finding; with none, it says "not found" and `collect` asks. A context the person corrected is never rewritten; a contradicting finding is reported.
- **Findings**, per source (Planning, Git, Tracker, Demo, Notes): one dated line each, with a link.
- **Gaps:** mismatches between sources. Internal, never in a report.

A parent's context covers the whole; a child holds only what is its own.

- **Why:** facts and prose stay separate, collecting again is safe, and nothing is written twice.
- **Not chosen:** a folder of per-source files per item: a story with three children would make 20 files.
