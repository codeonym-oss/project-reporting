# 001: A plugin in its own repository

**Date:** 2026-11-23 (grilling, Q1; agreed: "lets choose C, it will be easy to share, maintain")

**Question:** where does the skill live?

**Decision:** **a Claude Code plugin in its own repository, installed from the codeonym-oss marketplace.** It works alone, and uses groundwork and flow-reel when they are present. Nothing project-specific is built in; a project's data stays in that project.

- **Why:** one command installs it, and versions, fixes and the changelog live in one place.
- **Not chosen:** a personal skill (not shareable); a skill inside one repository (only that project gets it).
