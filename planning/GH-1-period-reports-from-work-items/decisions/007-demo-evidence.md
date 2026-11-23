# 007: Demo evidence: video, screenshots, explained or none

**Date:** 2026-11-23 (grilling, Q7; agreed: "lets go with these rules")

**Question:** how does each item get its demo, and where do the files live?

**Decision:** **the best available of four kinds:** a video matching the item's key or its parent's; one or two screenshots; an explained scenario for what cannot be shown; none for one-line items.

- `collect` only finds what exists, by key, in the configured demo folder, and reads a reel's transcript as a source.
- `report` lists items without a demo and says which deserve a video. For each yes, it hands the item's context to `/flow-reel:reel` as the brief. It never starts one alone. Without flow-reel: screenshots or explained.
- Screenshots are kept in the period's `assets/`. Videos are linked, never copied.
- A click path no reel or screenshot supports is written as explained, never as an instruction.

- **Why:** composing a video is slow and videos are large; a wrong click path in a live meeting is worse than none.
- **Not chosen:** composing missing reels automatically; copying videos into each period.
