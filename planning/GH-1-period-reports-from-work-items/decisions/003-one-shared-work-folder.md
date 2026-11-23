# 003: One shared .work/, periods select from it

**Date:** 2026-11-23 (grilling, Q3; agreed: "ok")

**Question:** is there one `.work/` per project, or one per period?

**Decision:** **one per project.** A work item has one folder, nested like the tracker, and grows over time; a period selects items by date.

```
.tracking/
├── config.md
├── presented-before.md           optional, see 012
├── templates/                    report formats (010)
├── .work/<KEY>-<slug>/item.md    children nested inside their parent's folder
├── weeks/2026/week-47-from-2026-11-16-to-2026-11-22/
│   ├── items.md                  what the period includes, and why
│   ├── notes.md                  optional (011)
│   ├── assets/                   screenshots
│   ├── exports/                  other formats, on request (008)
│   └── <format>.<lang>.md        the report
├── months/2026/11-november/
└── periods/<from>-to-<to>-<name>/
```

Weeks are ISO weeks. A written report is never regenerated unless asked; `items.md` keeps what it included.

- **Why:** the context is written once, a month selects from what weeks already collected, and dated facts make the selection checkable.
- **Not chosen:** one `.work/` per period: self-contained, but the same item is collected and described again in every period it touches.
