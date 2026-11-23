# Reports for any period, written from collected work items

## Goal

Turn a period's finished work into a short report its readers understand: what it was like before, what it is now,
what they gain, and a demo. It works on any stack, with any tracker or none.

## What it delivers

- `/project-reporting:init`: sets a project up and writes its own report template (decision 002).
- `/project-reporting:collect`: reads git, the forge, the tracker, planning, demos and meeting notes into one file per
  work item (decisions 003, 004, 009, 011).
- `/project-reporting:report`: writes a week, a month or any period, in any format and language (decisions 006, 008,
  010).

It works alone. With groundwork, an item's reasons come from its decisions; with flow-reel, missing demos can be made
(decision 007).

## Rules every ticket keeps

- Only what landed in the period is presented, once (decisions 005, 010).
- Every statement rests on a finding; what is not found is said, never invented (decision 004).
- Sources are read-only. Publishing, making a video and writing outside `.tracking/` wait for a yes (decisions 007 to
  009).
- Nothing project-specific in the plugin; a report changes by editing a template (decisions 001, 010).
- Short: skills under about 100 lines, reports within their limits (decisions 006, 013).

## Tickets, in order

1. Plugin skeleton, structure reference and the window/check script
2. init and collect
3. report
4. Docs, marketplace entry and v0.1.0

## Out of scope

Scheduled runs, dashboards, hours or cost reports, meeting recaps, converting old reports.

## Done when

Every ticket is done, and a real project's week and month have been reported with it and shown to a reader.
