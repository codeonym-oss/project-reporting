# 005: An item counts when it lands

**Date:** 2026-11-23 (grilling, Q5; agreed: "lets go with a and these rules")

**Question:** when does an item count as accomplished in a period?

**Decision:** **when it is merged into the integration branch, or directly into the production branch (a hotfix).**

- Presented once (refined by 010): earlier `items.md` files are checked.
- Production is a status on the item. One already presented that reaches production later gets one line under "Now in production".
- A parent appears as soon as one child lands, covering only the children that landed in the period.
- Work closed in the tracker with no commits counts on its closing date, once the person confirms it.
- Commits without a ticket become one `untracked` item per merge; the person names it, attaches it or leaves it out.
- Work that has not landed stays in `.work/`. No "in progress" and no roadmap by default; a template may add a "Next" section of three lines at most.

- **Why:** landing is a dated fact; tracker states often lag behind it.
- **Not chosen:** released (late, and batched); closed in the tracker (moved by hand); worked on (not an accomplishment).
