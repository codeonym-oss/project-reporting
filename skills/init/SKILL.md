---
name: init
description: Set a project up for project-reporting - detect its branches, forge, tracker, plans and demos, ask a few questions about the reports wanted, and write .tracking/config.md and the default report template. Use when the person wants to start reporting on a project with this plugin, or to change its settings.
---

# Set a project up

Read `<skill-dir>/../../references/structure.md` and `template-questions.md`.

1. **If `.tracking/config.md` exists,** show it, ask what to change, and change only that. If `.tracking/` holds other
   files, list them and ask what to do with them; never move or delete anything without a yes.
2. **Detect, without asking:**
   - the branches: the remote's default branch, and a production branch when finished work is merged elsewhere first;
   - the forge (`gh` or `glab`, from the remote's address) and whether you are signed in;
   - the key pattern, from recent commit subjects and branch names;
   - the tracker connector or CLI this session has;
   - a groundwork planning tree (`groundwork.md`), a folder of demo videos, flow-reel;
   - the machine's time zone, and product areas from the project's navigation or documentation.
   Show what you found in one short list and ask what is wrong in it.
3. **Ask, one question at a time,** each with your recommendation:
   - the languages of the reports, and which one leads;
   - the product areas, if they weren't confirmed;
   - whether `.tracking/` is kept in git: all of it, the reports without `.work/`, or none;
   - where finished reports go (a wiki space, a file, nowhere), if anywhere;
   - the template questions, for the default format;
   - any project rule the skills should follow.
4. **Show `config.md` and the template,** and write them after a yes. Write an ignore rule only if the answer needs
   one, and ask first: it is the person's file. Before anything is kept in git, say that `.work/` holds internal
   findings, and that a public repository would publish them.
5. **Check:** run `tracking.py period`, then `tracking.py window` on the last complete week. If what landed looks wrong
   to the person, fix the settings before going on.
6. Offer `/project-reporting:report`.

Suggest groundwork (plans and their reasons) and flow-reel (demo videos) once, if they are missing. Neither is needed.
