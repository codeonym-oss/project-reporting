# 006: The default client template

**Date:** 2026-11-23 (grilling, Q6; agreed: "ok")

**Question:** what does the default report look like?

**Decision:** **At a glance, then demo items by product area, then "Also delivered" and "Now in production".** `init` adapts it.

- At a glance: three to four lines, results only.
- A demo item: a title in the reader's words; Before, Now, Gain, one sentence each, 60 words at most; one line with demo, keys and production status.
- Small fixes: one line each. Work the reader cannot perceive is left out, unless it protects them.
- About eight demo items for a week at most; beyond that, `report` proposes which to merge or demote.
- No implementation words (services, libraries, tables, queues, classes). No hours, commit counts or per-person numbers.
- Grouped by product area, listed in the config; `collect` proposes an item's area and the person corrects it.

- **Why:** a reader should grasp what changed and what they gain without knowing how it is built.
- **Not chosen:** grouping by epic: planning words, and bugs often have no epic.
