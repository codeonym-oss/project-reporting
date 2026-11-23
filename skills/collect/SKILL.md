---
name: collect
description: Gather what happened on a project in a period - read git, the forge, the tracker, plans, demos and meeting notes, and keep one short file per work item saying why, before, now, gain and how, with dated findings. Use before writing a report, or to refresh the collected work items.
---

# Collect the work

Read `<skill-dir>/../../references/structure.md` and `sources.md`. Without `.tracking/config.md`, offer
`/project-reporting:init` and stop.

1. **Period:** `tracking.py period <what was asked>` (the last complete week by default). Say the bounds in words. If
   `complete` is false, say the period isn't over yet.
2. **What landed:** `tracking.py window FROM TO`. Show its warnings.
3. **Read the other sources** for those keys and their parents, plus what moved in the tracker or the plans in the
   period. Say which sources couldn't be read.
4. **Write each `item.md`,** nested like the tracker. Create missing parents. For an item that exists: add new findings,
   update its dates, move its folder if its parent changed, and leave a corrected Context alone.
   - `landed` and `released` come from `window`, or from a closing day the person confirmed. Never from a guess.
   - Work that hasn't landed is collected the same way, with `landed` empty.
   - Propose an `area` from the config's list.
5. **Settle what the sources don't say,** one question at a time, with your recommendation:
   - unkeyed work: name it, attach it or leave it out;
   - tickets closed without a commit: do they count?
   - a Why, Before or Gain that is `not found`, for work worth presenting.
   Ask about the work that matters and leave the rest `not found`.
6. **Report in the conversation,** shortly: the items that landed as a tree, one line each, what is `not found`, and
   the Gaps. Ask the person to correct the Contexts before a report is written from them.

Nothing is written outside `.tracking/`.
