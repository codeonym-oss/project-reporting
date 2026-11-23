# init and collect

## Problem

Setting a project up and gathering its evidence are manual.

## Change

- `init`: detects what it can, asks the rest, writes `config.md`, `templates/client.md` and, if wanted, the ignore rule (decisions 002, 006, 008).
- `collect`: fills `.work/` from git, the forge, the tracker, planning, demos and notes (decisions 004, 005, 007, 009, 011).

## Out of scope

Writing reports.

## Done when

- On a real project, `.work/` is filled for one complete week and the person has corrected it.
- Collecting again changes no corrected Context.
- It still works with no tracker, no planning folder and no demos, and says what is missing.
- Nothing is written to the tracker or the forge.
