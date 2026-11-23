# Plugin skeleton, structure reference and the window/check script

## Problem

There is no plugin yet, and nothing decides exactly what landed in a period.

## Change

- The plugin's manifest, licence, tests and release setup, following groundwork's.
- `references/structure.md`: the `.tracking/` tree, `config.md`, `item.md`, `items.md` (decisions 003, 004).
- `scripts/tracking.py` with `window` and `check` (decision 009), standard library only.

## Out of scope

The skills themselves.

## Done when

- Tests pass on throwaway repositories covering: merge, squash and rebase history; a hotfix on the production branch only; a stale local branch; commits without a key; ISO week 1 spanning two years; period bounds (start included, end excluded).
- `check` fails, with a clear message, on an item outside the period, one already presented, an unknown key, a missing demo file and an item over its word limit.
