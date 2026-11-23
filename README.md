# project-reporting

**Short reports of finished work, that their readers understand.** project-reporting is a plugin for Claude Code and
Codex. It reads what a period really delivered (git, the tracker, plans, demos, meeting notes), keeps one short file
per work item, and writes a report in your own format and languages.

```
/project-reporting:init                    set a project up: branches, sources, languages, report template
/project-reporting:collect                 what happened → .tracking/.work/, one file per work item
/project-reporting:report                  last week's report, in the default format
/project-reporting:report month
/project-reporting:report 2026-09-21..2026-10-19 as "sprint 6", format team
```

An entry of the default report:

```markdown
### The cart follows you when you sign in
**Before:** signing in emptied the cart, and customers filled it again.
**Now:** the cart follows the customer when they sign in.
**Gain:** no lost cart, and fewer support calls.
▶ [Video](../../../../demos/exports/SHOP-12-cart.mp4) · 1:20 · SHOP-12 · in production
```

## How it works

- **Only what landed, once.** An item belongs to the period it was merged in. Dates come from git, and a script checks
  every report: nothing outside the period, nothing presented twice, no unknown ticket, no missing demo, no text over
  its limit.
- **The reason is kept with the work.** Each item says why, before, now, gain and how, and every line rests on a dated
  finding. What no source says is `not found`, and you are asked; it is never invented.
- **Your formats.** A report format is one Markdown file that `init` writes from your answers and you edit. Any format
  works for a week, a month, a sprint or any dates.
- **Read-only.** Trackers and forges are never written to. Publishing a report or making a video waits for your yes.
- **Any stack.** It needs git and Python 3.10 or later. It uses Jira, Linear, GitHub or GitLab when your session can
  reach them, and works without.

It works well with [groundwork](https://github.com/codeonym-oss/groundwork), whose decisions give each item its
reasons, and [flow-reel](https://github.com/codeonym-oss/flow-reel), which makes the demo videos. Neither is needed.

## Install

**Claude Code:**

```
/plugin marketplace add codeonym-oss/claude-plugins
/plugin install project-reporting@codeonym-oss
```

**Codex:**

```bash
codex plugin marketplace add codeonym-oss/claude-plugins
codex plugin add project-reporting@codeonym-oss
```

Then run `init` in your project.

## What it writes

Everything goes in `.tracking/` ([the structure](references/structure.md)):

```
.tracking/
├── config.md          settings
├── templates/         report formats
├── .work/             one folder per work item
├── weeks/  months/  periods/
└── presented-before.md
```

`init` asks whether to keep it in git. `.work/` holds internal findings: think twice in a public repository.

**Coming from another report?** List what was already presented in `presented-before.md`, one `- KEY: YYYY-MM-DD` per
line, so the first weekly reports don't repeat it.

## Contributing

Issues and pull requests are welcome. `make test`, then `claude plugin validate .`; try a change with
`claude --plugin-dir /path/to/project-reporting`. See [AGENTS.md](AGENTS.md) for the rules.

## License

[MIT](LICENSE)
