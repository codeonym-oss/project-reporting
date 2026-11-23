---
name: report
description: Write a short report of a project's finished work for a week, a month, a sprint or any period - what it was before, what it is now, what it brings, and a demo - in the project's own format and languages. Use when the person asks for a weekly or monthly report, a sprint review, a client summary, or what was delivered between two dates.
---

# Write a report

Read `<skill-dir>/../../references/structure.md` and `writing.md`. Without `.tracking/config.md`, offer
`/project-reporting:init` and stop.

1. **Period and format:** `tracking.py period <what was asked>`; the format asked for, or the config's default. If its
   template is missing, make it with `<skill-dir>/../../references/template-questions.md`. If the report exists, ask
   before rewriting it.
2. **Collect** (`/project-reporting:collect`) when the period wasn't collected yet, or when work landed since.
3. **Choose the items.** Read the items that landed or were released in the period, and the earlier `items.md` of the
   same kind of period. Propose the table of `items.md`, grouped as the template says: key, what it is in five words,
   `as`, and its demo. Say what you would merge, shorten or leave out, and why. Write `items.md` after the person agrees.
4. **Demos.** List the demo items without one and say which deserve a video, and which are better explained. For each
   video the person says yes to, hand the item's Context to `/flow-reel:reel` as the brief, when flow-reel is there;
   say first that composing takes several minutes. Never start one without a yes. Screenshots: from the demo folder,
   from the person, or taken in the running app after a yes.
5. **Write the lead language,** following the template and `writing.md`, in `<format>.<lang>.md`.
6. **Check:** `tracking.py check <period folder> --format <format>`. Fix what it reports in the text or in `items.md`,
   never by changing an item's dates to make it pass. Run it until it passes; if the person accepts a problem, say so.
7. **Show the report** and take corrections. A correction of fact also goes into the item's Context. After approval,
   write the other languages and check again.
8. **Publish only if asked or configured, and only after a yes.** Show the title, the place and the attachments first.
   With no connector, list what to attach by hand. Save the link under `published` in `items.md`.
   Other file formats (HTML, PDF, slides, a short message) are made in `exports/` on request, from the approved report.

End with the report's path, and the open Gaps that the person may want to settle. Gaps stay out of the report.
