# The tracking folder

Every skill reads this first. It says where things live and what each file holds. `scripts/tracking.py` relies on
these exact names and headers.

```
.tracking/
├── config.md                     the project's settings, written by init
├── presented-before.md           optional: work presented before this plugin, one "- KEY: YYYY-MM-DD" per line
├── templates/<format>.md         report formats, yours to edit
├── .work/<KEY>-<slug>/item.md    one folder per work item; children nest inside their parent's folder
├── weeks/2026/week-47-from-2026-11-16-to-2026-11-22/
│   ├── items.md                  what the period includes, and how
│   ├── notes.md                  optional: notes of the meeting, written by the person
│   ├── assets/                   screenshots
│   ├── exports/                  other file formats, made on request
│   └── <format>.<lang>.md        the report
├── months/2026/11-november/
└── periods/<from>-to-<last day>-<name>/
```

A period is **[from, to)**: the start day is included, the end day is excluded. Folder names show the last included
day. Never work out a week number or a folder by hand: `tracking.py period` gives both.

Run the script from the project's root:

```bash
python3 <skill-dir>/../../scripts/tracking.py period [week | month | 2026-W47 | 2026-11 | FROM..TO] [--name sprint-6]
python3 <skill-dir>/../../scripts/tracking.py window FROM TO
python3 <skill-dir>/../../scripts/tracking.py check PERIOD_DIR [--format client]
```

## `config.md`

```markdown
---
project: Acme Shop
integration-branch: develop     # where finished work is merged
production-branch: main         # the same branch when there is only one
remote: origin
time-zone: Europe/Paris
key-pattern: SHOP-\d+           # empty when commits carry no ticket key
forge: github                   # github | gitlab | none
tracker: jira                   # jira | linear | github | gitlab | none, with what is needed to query it
tracker-project: SHOP
planning: planning              # a groundwork planning root, or any folder of plans; empty if none
demos: demos/exports            # where demo videos are; empty if none
languages: en, fr
lead-language: en               # the one the person reviews
work-language: en               # the language of .work/
areas: Checkout, Catalogue, Account
default-format: client
publish-to:                     # optional: where a finished report may be published
---

# Project rules

- Plain sentences, followed as written.
```

## `item.md`

```markdown
---
key: SHOP-12                    # or untracked-<slug>
title: Keep the cart after signing in
kind: ticket                    # epic | story | ticket | bug | untracked
parent: SHOP-10
people: Ana, Bo
area: Checkout
started: 2026-11-13
landed: 2026-11-18              # each day work of this item was merged, separated by commas
released:                       # the day it reached production
demo: demos/exports/SHOP-12-cart.mp4
---

## Context
- **Why:** signing in emptied the cart, the most frequent complaint to support.
- **Before:** the customer had to fill the cart again.
- **Now:** the cart follows the customer when they sign in.
- **Gain:** no lost cart, fewer support calls.
- **How:** the visitor's cart is joined to the account's cart.

## Findings
### Planning
- 2026-11-13 decision 004: the newest quantity wins. Not chosen: adding both. (planning/SHOP-12-cart/decisions/004…)
### Git
- 2026-11-18 merged into develop, !41
### Tracker
- 2026-11-12 created under SHOP-10, In Progress since 2026-11-13
### Demo
- Video SHOP-12-cart, 1:20
### Notes
- 2026-11-09 the client asked for this in the weekly meeting

## Gaps
- Merged, but the tracker still says In Progress.
```

- **Context:** these five lines at most, one sentence each, in plain words. Every line rests on a finding. When no
  source says it, write `not found` and ask the person. Never guess a reason or a gain.
- **Findings:** dated facts, one line each, with where they come from. Leave out a source that said nothing.
- **Gaps:** mismatches between sources. Internal: never in a report.
- **A parent's** Context covers the whole; a child's holds only what is its own.
- **A Context the person corrected** is never rewritten. If a new finding contradicts it, say so.

## `items.md`

```markdown
---
from: 2026-11-16
to: 2026-11-23                  # excluded
published:                      # links, once published
---

| key | landed | format | as | note |
|---|---|---|---|---|
| SHOP-12 | 2026-11-18 | client | demo | |
| SHOP-14 | 2026-11-19 | client | line | small fix |
| SHOP-9 | 2026-11-10 | client | production | presented in week 46 |
| SHOP-15 | 2026-11-19 | client | left-out | planning only |
```

One row per item and format, for items that landed themselves (a parent only when work landed under its own key).
`as` is:

- `demo`: a demo item, presented for the first time;
- `line`: one line, presented for the first time;
- `update`: presented before, but new work landed in this period; one line;
- `production`: presented before, reached production in this period; one line;
- `left-out`: not in the report; the note says why.

A written report is never regenerated unless the person asks.
