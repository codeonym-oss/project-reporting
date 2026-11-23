# 010: Formats are template files, independent of the period

**Date:** 2026-11-23 (grilling, Q10; agreed: "lets go with these rules")

**Question:** how do different formats and period lengths work?

**Decision:** **a format is one Markdown file in `.tracking/templates/`** saying who reads it, what it includes and leaves out, its grouping and limits, with the skeleton to fill.

- `client` ships by default (006). Asking for a format that does not exist makes `report` ask the same questions and write it.
- Any format works for any period. With nothing given: the last complete week, default format.
- Named periods (sprints) go under `periods/`, with dates given or read from the tracker.
- A report is `<format>.<lang>.md`.
- Longer periods keep the same overall length: main results by area, one line for the rest.
- **Refines 005:** "presented once" compares periods of the same kind and format.

Not in version 1: scheduled runs, dashboards, hours or cost reports.

- **Why:** a report changes by editing a file; without the refinement a monthly report would be empty.
- **Not chosen:** formats built into the skill.
