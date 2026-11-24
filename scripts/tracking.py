#!/usr/bin/env python3
"""The exact part of project-reporting: period bounds, what landed in git, and checking a report.

    tracking.py period [week | month | 2026-W47 | 2026-11 | 2026-11-01..2026-11-15] [--name sprint-6] [--today DATE]
    tracking.py window FROM TO [--no-fetch]
    tracking.py check PERIOD_DIR [--format client]

A period is [from, to): the start day is included, the end day is excluded. Needs git and nothing else.
Structure of the files it reads: references/structure.md.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

MONTHS = ("january february march april may june july august september october november december").split()
MR_PATTERNS = (r"Merge pull request #(\d+)", r"See merge request \S*!(\d+)", r"\(#(\d+)\)\s*$")
PRESENTED = {"demo", "line", "update", "with"}
ROW_KINDS = PRESENTED | {"production", "left-out"}


class Failure(Exception):
    """A problem to show the person as one line."""


# --- files ---------------------------------------------------------------------------------------------------------


def front_matter(path: Path) -> dict:
    """The flat `key: value` header of a Markdown file. A comment starts with two spaces or more, then `# `."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise Failure(f"cannot read {path}: {error.strerror}")
    if not lines or lines[0].strip() != "---":
        raise Failure(f"{path} has no front matter")
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        name, colon, value = line.partition(":")
        if colon:
            fields[name.strip()] = re.sub(r"(^|\s+)#\s.*$", "", value.strip()).strip().strip('"')
    raise Failure(f"{path}: the front matter is not closed")


def split_list(value: str) -> list:
    return [part.strip() for part in (value or "").split(",") if part.strip()]


def to_date(text: str) -> date:
    try:
        return date.fromisoformat(text.strip())
    except ValueError:
        raise Failure(f"not a date (YYYY-MM-DD): {text!r}")


def load_config(tracking: Path) -> dict:
    config = front_matter(tracking / "config.md")
    for name in ("integration-branch", "production-branch", "remote"):
        if config.get(name, "").startswith("-"):
            raise Failure(f"config.md: {name} cannot start with '-'")
    if not config.get("integration-branch"):
        raise Failure("config.md: integration-branch is missing")
    config.setdefault("remote", "origin")
    try:
        config["zone"] = ZoneInfo(config["time-zone"]) if config.get("time-zone") else timezone.utc
    except (ZoneInfoNotFoundError, ValueError):
        raise Failure(f"config.md: unknown time-zone {config['time-zone']!r}")
    try:
        config["keys"] = re.compile(config["key-pattern"]) if config.get("key-pattern") else None
    except re.error as error:
        raise Failure(f"config.md: key-pattern is not a valid expression: {error}")
    return config


# --- period --------------------------------------------------------------------------------------------------------


def month_bounds(year: int, month: int) -> tuple:
    if not 1 <= month <= 12:
        raise Failure(f"not a month: {month}")
    return date(year, month, 1), date(year + month // 12, month % 12 + 1, 1)


def resolve_period(text: str, today: date, name: str = "") -> dict:
    monday = today - timedelta(days=today.weekday())
    week = re.fullmatch(r"(\d{4})-W(\d{1,2})", text)
    month = re.fullmatch(r"(\d{4})-(\d{2})", text)
    if text == "week":
        kind, start, end = "weeks", monday - timedelta(days=7), monday
    elif week:
        try:
            start = date.fromisocalendar(int(week[1]), int(week[2]), 1)
        except ValueError as error:
            raise Failure(str(error))
        kind, end = "weeks", start + timedelta(days=7)
    elif text == "month":
        end = today.replace(day=1)
        kind, start = "months", (end - timedelta(days=1)).replace(day=1)
    elif month:
        kind, (start, end) = "months", month_bounds(int(month[1]), int(month[2]))
    elif ".." in text:
        first, _, last = text.partition("..")
        kind, start, end = "periods", to_date(first), to_date(last)
    else:
        raise Failure(f"not a period: {text!r} (week, month, 2026-W47, 2026-11 or 2026-11-01..2026-11-15)")
    if end <= start:
        raise Failure("the period is empty: the end day is excluded and must come after the start")
    last_day = end - timedelta(days=1)
    if kind == "weeks":
        iso = start.isocalendar()
        folder = f"weeks/{iso.year}/week-{iso.week:02d}-from-{start}-to-{last_day}"
    elif kind == "months":
        folder = f"months/{start.year}/{start.month:02d}-{MONTHS[start.month - 1]}"
    else:
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        folder = f"periods/{start}-to-{last_day}" + (f"-{slug}" if slug else "")
    return {"kind": kind, "from": str(start), "to": str(end), "last_day": str(last_day), "folder": folder,
            "complete": end <= today}


# --- window --------------------------------------------------------------------------------------------------------


class Git:
    def __init__(self, repo: Path):
        self.repo = repo

    def run(self, *args: str) -> str:
        done = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
        if done.returncode:
            raise Failure(f"git {args[0]}: {done.stderr.strip() or 'failed'}")
        return done.stdout

    def log(self, *args: str) -> list:
        text = self.run("log", "-z", "--format=%H%x1f%P%x1f%ct%x1f%aN%x1f%B", *args)
        commits = []
        for record in text.split("\0"):
            if record.strip():
                sha, parents, when, author, message = record.split("\x1f", 4)
                commits.append({"hash": sha.strip(), "parents": parents.split(), "time": int(when),
                                "author": author, "message": message.strip()})
        return commits

    def resolve(self, remote: str, branch: str, warnings: list) -> str:
        """The remote branch, so that a stale local one never hides work; the local one only if there is no other."""
        for ref in (f"refs/remotes/{remote}/{branch}", f"refs/heads/{branch}"):
            try:
                self.run("rev-parse", "--verify", "--quiet", ref)
            except Failure:
                continue
            if ref.startswith("refs/heads/"):
                warnings.append(f"{branch}: no branch on {remote}, the local one was read")
            return ref
        raise Failure(f"no branch {branch!r}, on {remote} or here")


def headline(message: str) -> str:
    """The subject and the first paragraph after it. Keys further down are mentions of other work."""
    paragraphs = [p for p in re.split(r"\n\s*\n", message.strip()) if p.strip()]
    return "\n".join(paragraphs[:2])


def work_keys(commit: dict, own: list, pattern) -> tuple:
    """The keys the work is for, and those only mentioned in it.

    The title (a branch name, a squash subject) says it best, then the first paragraph, then each commit's first key.
    """
    if not pattern:
        return [], []
    subjects = [c["message"].split("\n")[0] for c in own]
    title = pattern_keys(pattern, commit["message"].split("\n")[0])
    everything = title | pattern_keys(pattern, headline(commit["message"]), *subjects)
    keys = title or pattern_keys(pattern, headline(commit["message"])) or {
        match.group(0) for match in map(pattern.search, subjects) if match}
    return sorted(keys), sorted(everything - keys)


def pattern_keys(pattern, *texts: str) -> set:
    return {match.group(0) for text in texts for match in pattern.finditer(text)}


def describe(git: Git, commit: dict, config: dict) -> dict:
    inside = []
    if len(commit["parents"]) > 1:
        inside = git.log(*commit["parents"][1:], f"^{commit['parents'][0]}")
    own = [c for c in inside if len(c["parents"]) < 2] or [commit]
    keys, mentions = work_keys(commit, own, config["keys"])
    mr = next((m.group(1) for p in MR_PATTERNS
               for m in [re.search(p, commit["message"].split("\n")[0] if p.endswith("$") else commit["message"])]
               if m), None)
    return {"hash": commit["hash"][:10], "date": local_day(commit["time"], config), "subject":
            commit["message"].split("\n")[0], "mr": mr, "keys": keys, "mentions": mentions, "people": sorted({c["author"] for c in own}),
            "commits": len(own), "_inside": {c["hash"] for c in inside}}


def local_day(timestamp: int, config: dict) -> str:
    return str(datetime.fromtimestamp(timestamp, config["zone"]).date())


def window(repo: Path, config: dict, start: date, end: date, fetch: bool = True) -> dict:
    if end <= start:
        raise Failure("the period is empty: the end day is excluded and must come after the start")
    git, warnings, remote = Git(repo), [], config["remote"]
    fetched = False
    if fetch:
        try:
            git.run("fetch", "--quiet", remote)
            fetched = True
        except Failure as error:
            warnings.append(f"not fetched, recent work may be missing: {error}")
    integration = config["integration-branch"]
    production = config.get("production-branch") or integration
    main_line = git.log("--first-parent", git.resolve(remote, integration, warnings))
    main_hashes = {c["hash"] for c in main_line}
    prod_line = [] if production == integration else git.log(
        "--first-parent", git.resolve(remote, production, warnings))
    prod_only = {c["hash"] for c in prod_line} - main_hashes

    def in_period(commit):
        return str(start) <= local_day(commit["time"], config) < str(end)

    landed, syncs, hotfixes, releases = [], [], [], []
    for commit in filter(in_period, main_line):
        entry = describe(git, commit, config)
        (syncs if entry["_inside"] & prod_only else landed).append(entry)

    known = set()
    if config["keys"]:
        for commit in main_line:
            known |= pattern_keys(config["keys"], headline(commit["message"]))
    for commit in filter(in_period, prod_line):
        if commit["hash"] in main_hashes:
            continue  # shared history, or a fast-forward: git keeps no date for it
        entry = describe(git, commit, config)
        if entry["_inside"]:
            is_release = bool(entry["_inside"] & main_hashes)
        else:
            is_release = bool(entry["keys"]) and set(entry["keys"]) <= known
        if is_release and entry["_inside"]:
            # A release's title rarely names everything in it: its keys are those of the work it brings.
            brought = [describe(git, c, config) for c in main_line if c["hash"] in entry["_inside"]]
            entry["keys"] = sorted({key for work in brought for key in work["keys"]} | set(entry["keys"]))
            entry["mentions"] = sorted(set(entry["mentions"]) - set(entry["keys"]))
        (releases if is_release else hotfixes).append(entry)
    if prod_line and prod_line[0]["hash"] in main_hashes:
        warnings.append(f"{production} follows {integration} by fast-forward: release dates are not in git")

    keys = {}
    for entry in landed + hotfixes:
        for key in entry["keys"]:
            keys.setdefault(key, {"landed": [], "released": None})["landed"].append(entry["date"])
    for entry in hotfixes:
        for key in entry["keys"]:
            keys[key]["released"] = entry["date"]
    for entry in releases:
        for key in entry["keys"]:
            keys.setdefault(key, {"landed": [], "released": None})["released"] = entry["date"]
    for fact in keys.values():
        fact["landed"] = sorted(set(fact["landed"]))
    unkeyed = [e["hash"] for e in landed + hotfixes if not e["keys"]]
    for entry in landed + syncs + hotfixes + releases:
        entry.pop("_inside")
    return {"from": str(start), "to": str(end), "fetched": fetched, "warnings": warnings, "keys": keys,
            "landed": landed, "hotfixes": hotfixes, "releases": releases, "unkeyed": unkeyed, "syncs": syncs}


# --- check ---------------------------------------------------------------------------------------------------------


def load_items(tracking: Path) -> dict:
    items = {}
    for path in sorted((tracking / ".work").rglob("item.md")):
        fields = front_matter(path)
        key = fields.get("key")
        if not key:
            raise Failure(f"{path} has no key")
        if key in items:
            raise Failure(f"{key} is described twice: {items[key]['path']} and {path}")
        items[key] = {**fields, "path": path}
    for key, item in items.items():
        item["ancestors"] = []
        parent = item.get("parent")
        while parent and parent != key and parent not in item["ancestors"]:
            item["ancestors"].append(parent)
            parent = items.get(parent, {}).get("parent")
    return items


def load_rows(path: Path) -> list:
    """The table of an items.md: key, landed, format, as, note."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not line.strip().startswith("|") or len(cells) < 4 or cells[0] == "key" or set(cells[0]) <= set("-: "):
            continue
        how, _, host = cells[3].partition(" ")
        rows.append({"key": cells[0], "format": cells[2], "as": how, "host": host.strip()})
    return rows


def presented_earlier(tracking: Path, period_dir: Path, kind: str, start: str, name: str) -> dict:
    """Keys shown before, in a period of the same kind and format."""
    seen = {}
    before = tracking / "presented-before.md"
    if before.is_file() and kind == "weeks":
        for line in before.read_text(encoding="utf-8").splitlines():
            match = re.match(r"-\s+(\S+):\s*(\S+)", line)
            if match and match[2] < start:
                seen[match[1]] = f"presented-before.md ({match[2]})"
    for path in sorted((tracking / kind).rglob("items.md")):
        if path.parent.resolve() == period_dir.resolve() or front_matter(path).get("from", "") >= start:
            continue
        for row in load_rows(path):
            if row["format"] == name and row["as"] in PRESENTED:
                seen[row["key"]] = str(path.parent.relative_to(tracking))
    return seen


def context_lines(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return dict(re.findall(r"^- \*\*(\w+):\*\*\s*(.*)$", text, re.M))


def words(text: str) -> int:
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return len(re.findall(r"[^\W_]+(?:['’.-][^\W_]+)*", text))


def check_report(path: Path, limits: dict, keys, rows: list, items: dict) -> list:
    text, errors, label = path.read_text(encoding="utf-8"), [], path.name
    allowed, shown = set(), [r for r in rows if r["as"] != "left-out"]
    for row in shown:
        allowed |= {row["key"], *items.get(row["key"], {}).get("ancestors", [])}
    if keys:
        found = pattern_keys(keys, text)
        errors += [f"{label}: {key} is in the report but not in items.md" for key in sorted(found - allowed)]
        for row in shown if found else []:
            names = {row["key"], row["host"], *items.get(row["key"], {}).get("ancestors", [])}
            if keys.fullmatch(row["key"]) and not names & found:
                errors.append(f"{label}: {row['key']} is in items.md but not in the report")
    for target in re.findall(r"!?\[[^\]]*\]\(<?([^)>]+)>?\)", text):
        if not re.match(r"[a-z][a-z0-9+.-]*:|#", target, re.I) and not (path.parent / target).exists():
            errors.append(f"{label}: no such file: {target}")

    sections = re.split(r"^### ", text, flags=re.M)[1:]
    sections = [re.split(r"^#{1,2} ", section, flags=re.M)[0] for section in sections]
    if limits.get("max-items") and len(sections) > int(limits["max-items"]):
        errors.append(f"{label}: {len(sections)} demo items, the limit is {limits['max-items']}")
    if limits.get("item-words"):
        for section in sections:
            lines = [line for line in section.splitlines() if line.strip()]
            title, body = lines[0], [line for line in lines[1:] if not line.startswith(("▶", "!["))]
            count = words("\n".join(body))
            if count > int(limits["item-words"]):
                errors.append(f"{label}: \"{title}\" has {count} words, the limit is {limits['item-words']}")
    if limits.get("glance-lines"):
        intro = re.split(r"^## ", text, flags=re.M)[0]
        bullets = len(re.findall(r"^[-*] ", intro, re.M))
        if bullets > int(limits["glance-lines"]):
            errors.append(f"{label}: {bullets} lines at a glance, the limit is {limits['glance-lines']}")
    prose = re.sub(r"\]\([^)]*\)", "]", text)
    for term in split_list(limits.get("avoid", "")):
        if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", prose, re.I):
            errors.append(f"{label}: \"{term}\" is a word this format avoids")
    return errors


def check(tracking: Path, period_dir: Path, name: str, config: dict) -> list:
    if not (period_dir / "items.md").is_file():
        raise Failure(f"{period_dir} has no items.md")
    head = front_matter(period_dir / "items.md")
    start, end = head.get("from", ""), head.get("to", "")
    if to_date(start) >= to_date(end):
        raise Failure("items.md: the period is empty")
    try:
        kind = period_dir.resolve().relative_to(tracking.resolve()).parts[0]
    except (ValueError, IndexError):
        raise Failure(f"{period_dir} is not inside {tracking}")
    template = tracking / "templates" / f"{name}.md"
    limits = front_matter(template)
    items = load_items(tracking)
    rows = [row for row in load_rows(period_dir / "items.md") if row["format"] == name]
    seen = presented_earlier(tracking, period_dir, kind, start, name)
    errors, listed = [], set()
    if not rows:
        errors.append(f"items.md has no row for the format {name}")
    for row in rows:
        key, how = row["key"], row["as"]
        if key in listed:
            errors.append(f"{key}: listed twice")
        listed.add(key)
        if how not in ROW_KINDS:
            errors.append(f"{key}: \"{how}\" is not one of {', '.join(sorted(ROW_KINDS))}")
            continue
        item = items.get(key)
        if not item:
            errors.append(f"{key}: no such item in .work/")
            continue
        host = next((r for r in rows if r["key"] == row["host"]), None)
        if how == "with" and (host is None or host["as"] not in PRESENTED - {"with"}):
            errors.append(f"{key}: is presented with {row['host'] or 'nothing'}, which is not itself presented")
        landed = split_list(item.get("landed", ""))
        if how in PRESENTED and not any(start <= day < end for day in landed):
            errors.append(f"{key}: did not land in the period (landed: {', '.join(landed) or 'never'})")
        if how in PRESENTED - {"update"} and key in seen:
            errors.append(f"{key}: already presented in {seen[key]}; use \"update\" if new work landed")
        if how == "production" and not start <= item.get("released", "") < end:
            errors.append(f"{key}: did not reach production in the period")
        if how == "demo":
            context = context_lines(item["path"])
            for line in ("Before", "Now", "Gain"):
                value = context.get(line, "")
                parents = [context_lines(items[a]["path"]).get(line, "") for a in item["ancestors"] if a in items]
                if not any(v and "not found" not in v.lower() for v in [value, *parents]):
                    errors.append(f"{key}: nothing is known for \"{line}\", so it cannot be a demo item")
            demo = item.get("demo", "")
            if demo and not re.match(r"[a-z][a-z0-9+.-]*:", demo, re.I) and not (tracking.parent / demo).exists():
                errors.append(f"{key}: its demo is missing: {demo}")
    reports = sorted(period_dir.glob(f"{name}.*.md"))
    if not reports:
        errors.append(f"no report {name}.<language>.md in {period_dir.name}")
    for report in reports:
        errors += check_report(report, limits, config["keys"], rows, items)
    return errors


# --- command line --------------------------------------------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", type=Path, default=Path("."), help="the project's root (default: here)")
    parser.add_argument("--tracking", type=Path, help="the tracking folder (default: <repo>/.tracking)")
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("period", help="a period's bounds and folder")
    p.add_argument("period", nargs="?", default="week")
    p.add_argument("--name", default="", help="names a from..to period, such as sprint-6")
    p.add_argument("--today", help="the day to count from (default: today)")
    p = commands.add_parser("window", help="what landed between two days")
    p.add_argument("start", metavar="from")
    p.add_argument("end", metavar="to", help="excluded")
    p.add_argument("--no-fetch", action="store_true")
    p = commands.add_parser("check", help="verify a period's report")
    p.add_argument("period_dir", type=Path)
    p.add_argument("--format", default="", help="default: the config's default-format")
    args = parser.parse_args(argv)
    tracking = args.tracking or args.repo / ".tracking"
    try:
        config = load_config(tracking)
        if args.command == "period":
            today = to_date(args.today) if args.today else datetime.now(config["zone"]).date()
            print(json.dumps(resolve_period(args.period, today, args.name), indent=2))
        elif args.command == "window":
            result = window(args.repo, config, to_date(args.start), to_date(args.end), not args.no_fetch)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            name = args.format or config.get("default-format") or "client"
            errors = check(tracking, args.period_dir, name, config)
            for error in errors:
                print(f"- {error}")
            print(f"{len(errors)} problem(s)" if errors else "The report passes.")
            return 1 if errors else 0
    except Failure as failure:
        print(f"error: {failure}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
