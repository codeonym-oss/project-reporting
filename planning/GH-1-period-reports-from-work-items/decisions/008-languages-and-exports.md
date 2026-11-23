# 008: Languages and exports

**Date:** 2026-11-23 (grilling, Q8; agreed: "ok")

**Question:** in which languages and forms is a report delivered?

**Decision:** **the person reviews the lead language; the report's Markdown file is the export.**

- The config lists the languages and the lead. The others are written from the same items after approval, not translated sentence by sentence; a correction to the lead is carried to them.
- `.work/` uses one configured language. Tracker titles are kept verbatim.
- HTML, PDF, slides or a short message are made in `exports/` only on request, from the approved report.
- Publishing is optional: the config may hold a destination. `report` shows the title, location and attachments and waits for a yes. Without a connector, it lists what to attach by hand.
- The published link is saved in `items.md`.

- **Why:** one text to review, and no copies that drift.
- **Not chosen:** a separate export file per destination; publishing without asking.
