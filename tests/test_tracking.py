"""scripts/tracking.py, on throwaway repositories and tracking folders."""
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import tracking as t  # noqa: E402

CONFIG = """---
integration-branch: develop
production-branch: main
time-zone: Europe/Paris
key-pattern: SHOP-\\d+
default-format: client
---
"""


class Repo:
    """A remote and a clone; every commit has an explicit date."""

    def __init__(self, root: Path):
        self.remote, self.path = root / "remote.git", root / "clone"
        self._git(root, "init", "-q", "--bare", "-b", "develop", str(self.remote))
        self._git(root, "init", "-q", "-b", "develop", str(self.path))
        self.git("remote", "add", "origin", str(self.remote))
        (self.path / ".tracking").mkdir()
        (self.path / ".tracking/config.md").write_text(CONFIG)
        self.n = 0
        self.commit("start", "2026-01-01T10:00:00+01:00")
        self.git("branch", "main")
        self.push()

    def _git(self, cwd, *args, when=None, author="Ana"):
        env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
               "GIT_AUTHOR_NAME": author, "GIT_AUTHOR_EMAIL": "a@example.com",
               "GIT_COMMITTER_NAME": author, "GIT_COMMITTER_EMAIL": "a@example.com"}
        if when:
            env.update(GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
        subprocess.run(["git", *args], cwd=cwd, env=env, check=True, capture_output=True)

    def git(self, *args, **kw):
        self._git(self.path, *args, **kw)

    def commit(self, message, when, author="Ana"):
        self.n += 1
        (self.path / f"file{self.n}").write_text(message)
        self.git("add", f"file{self.n}")
        self.git("commit", "-q", "-m", message, when=when, author=author)

    def merge(self, branch, message, when):
        self.git("merge", "-q", "--no-ff", "-m", message, branch, when=when)

    def push(self):
        self.git("push", "-q", "--all", "origin")

    def window(self, start, end, fetch=True):
        config = t.load_config(self.path / ".tracking")
        return t.window(self.path, config, date.fromisoformat(start), date.fromisoformat(end), fetch)


class Temp(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)


class PeriodTest(unittest.TestCase):
    def period(self, text, today="2026-11-23", name=""):
        return t.resolve_period(text, date.fromisoformat(today), name)

    def test_the_last_complete_week(self):
        for today in ("2026-11-23", "2026-11-25", "2026-11-29"):
            found = self.period("week", today)
            self.assertEqual((found["from"], found["to"]), ("2026-11-16", "2026-11-23"))
            self.assertEqual(found["folder"], "weeks/2026/week-47-from-2026-11-16-to-2026-11-22")

    def test_week_one_spans_two_years(self):
        found = self.period("2026-W01")
        self.assertEqual(found["folder"], "weeks/2026/week-01-from-2025-12-29-to-2026-01-04")
        self.assertEqual(self.period("week", "2026-01-05")["folder"], found["folder"])

    def test_week_53_belongs_to_its_iso_year(self):
        self.assertEqual(self.period("2026-W53")["folder"], "weeks/2026/week-53-from-2026-12-28-to-2027-01-03")
        with self.assertRaises(t.Failure):
            self.period("2025-W53")

    def test_months(self):
        self.assertEqual(self.period("month")["folder"], "months/2026/10-october")
        self.assertEqual(self.period("month", "2026-01-10")["folder"], "months/2025/12-december")
        december = self.period("2026-12")
        self.assertEqual((december["from"], december["to"]), ("2026-12-01", "2027-01-01"))
        self.assertFalse(december["complete"])

    def test_a_range_excludes_its_end_and_takes_a_name(self):
        found = self.period("2026-09-21..2026-10-19", name="Sprint 6")
        self.assertEqual(found["folder"], "periods/2026-09-21-to-2026-10-18-sprint-6")

    def test_what_is_not_a_period(self):
        for text in ("soon", "2026-13", "2026-11-02..2026-11-02", "2026-11-31..2026-12-02"):
            with self.subTest(text), self.assertRaises(t.Failure):
                self.period(text)


class WindowTest(Temp):
    def setUp(self):
        super().setUp()
        self.repo = Repo(self.root)

    def feature(self, name, commits, when, message, author="Ana"):
        self.repo.git("checkout", "-q", "-b", name)
        for text in commits:
            self.repo.commit(text, when, author)
        self.repo.git("checkout", "-q", "develop")
        self.repo.merge(name, message, when)

    def test_a_merge_lists_its_keys_people_and_request(self):
        self.feature("feature/SHOP-7-cart", ["SHOP-7 Feat: cart", "SHOP-7 Fix: total"], "2026-11-17T10:00:00+01:00",
                     "Merge branch 'feature/SHOP-7-cart' into 'develop'\n\nSHOP-7 Cart\n\nSee SHOP-99 too.\n\n"
                     "See merge request acme/shop!41", author="Bo")
        self.repo.push()
        found = self.repo.window("2026-11-16", "2026-11-23")
        self.assertEqual(list(found["keys"]), ["SHOP-7"])
        entry, = found["landed"]
        self.assertEqual((entry["mr"], entry["people"], entry["commits"]), ("41", ["Bo"], 2))

    def test_a_key_only_mentioned_does_not_count_as_landed(self):
        self.feature("feature/SHOP-7-cart", ["SHOP-7 Feat: cart", "SHOP-5 Test: adapt an old check"],
                     "2026-11-17T10:00:00+01:00", "Merge branch 'feature/SHOP-7-cart' into 'develop'")
        self.repo.push()
        found = self.repo.window("2026-11-16", "2026-11-23")
        self.assertEqual(list(found["keys"]), ["SHOP-7"])
        self.assertEqual(found["landed"][0]["mentions"], ["SHOP-5"])

    def test_a_merge_without_a_key_in_its_title_takes_its_commits_keys(self):
        self.feature("cart", ["SHOP-7 Feat: cart, after SHOP-2", "SHOP-8 Feat: total"], "2026-11-17T10:00:00+01:00",
                     "Merge branch 'cart' into 'develop'")
        self.repo.push()
        self.assertEqual(set(self.repo.window("2026-11-16", "2026-11-23")["keys"]), {"SHOP-7", "SHOP-8"})

    def test_squash_and_rebase_histories(self):
        self.repo.commit("SHOP-8 Feat: search (#12)", "2026-11-18T10:00:00+01:00")
        self.repo.commit("SHOP-9 Feat: one", "2026-11-18T11:00:00+01:00")
        self.repo.commit("SHOP-9 Feat: two", "2026-11-19T11:00:00+01:00")
        self.repo.push()
        found = self.repo.window("2026-11-16", "2026-11-23")
        self.assertEqual(found["keys"]["SHOP-9"]["landed"], ["2026-11-18", "2026-11-19"])
        self.assertIn("12", [entry["mr"] for entry in found["landed"]])

    def test_the_start_is_included_and_the_end_excluded_in_the_project_time_zone(self):
        self.repo.commit("SHOP-1 first minute", "2026-11-15T23:00:00+00:00")  # 16 November 00:00 in Paris
        self.repo.commit("SHOP-2 last minute", "2026-11-22T22:59:00+00:00")
        self.repo.commit("SHOP-3 next week", "2026-11-22T23:00:00+00:00")
        self.repo.push()
        self.assertEqual(set(self.repo.window("2026-11-16", "2026-11-23")["keys"]), {"SHOP-1", "SHOP-2"})

    def test_unkeyed_work_is_listed(self):
        self.repo.commit("tidy the docs", "2026-11-18T10:00:00+01:00")
        self.repo.push()
        found = self.repo.window("2026-11-16", "2026-11-23")
        self.assertEqual(found["unkeyed"], [found["landed"][0]["hash"]])

    def test_a_stale_local_branch_hides_nothing(self):
        self.repo.commit("SHOP-4 from elsewhere", "2026-11-18T10:00:00+01:00")
        self.repo.push()
        self.repo.git("reset", "-q", "--hard", "HEAD~1")
        self.repo.git("update-ref", "refs/remotes/origin/develop", "HEAD")
        self.assertEqual(self.repo.window("2026-11-16", "2026-11-23", fetch=False)["keys"], {})
        self.assertIn("SHOP-4", self.repo.window("2026-11-16", "2026-11-23")["keys"])

    def test_no_remote_warns_and_reads_the_local_branch(self):
        self.repo.commit("SHOP-5 local", "2026-11-18T10:00:00+01:00")
        self.repo.git("remote", "remove", "origin")
        found = self.repo.window("2026-11-16", "2026-11-23")
        self.assertIn("SHOP-5", found["keys"])
        self.assertFalse(found["fetched"])
        self.assertTrue(found["warnings"])

    def test_release_hotfix_and_back_merge(self):
        self.feature("feature/a", ["SHOP-7 Feat: cart"], "2026-11-10T10:00:00+01:00", "Merge branch 'feature/a'")
        self.repo.git("checkout", "-q", "main")
        self.repo.merge("develop", "Merge branch 'develop' into 'main'", "2026-11-17T10:00:00+01:00")
        self.repo.git("checkout", "-q", "-b", "hotfix/b")
        self.repo.commit("SHOP-20 Fix: leak", "2026-11-18T10:00:00+01:00")
        self.repo.git("checkout", "-q", "main")
        self.repo.merge("hotfix/b", "Merge branch 'hotfix/b' into 'main'", "2026-11-18T11:00:00+01:00")
        self.repo.git("checkout", "-q", "develop")
        self.repo.merge("main", "Merge branch 'main' into 'develop'", "2026-11-19T10:00:00+01:00")
        self.repo.push()
        found = self.repo.window("2026-11-16", "2026-11-23")
        self.assertEqual(found["keys"]["SHOP-7"], {"landed": [], "released": "2026-11-17"})
        self.assertEqual(found["keys"]["SHOP-20"], {"landed": ["2026-11-18"], "released": "2026-11-18"})
        self.assertEqual((len(found["hotfixes"]), len(found["releases"]), len(found["syncs"])), (1, 1, 1))
        self.assertEqual(found["landed"], [])

    def test_a_release_whose_title_names_one_key_still_brings_them_all(self):
        self.feature("feature/a", ["SHOP-7 Feat: cart"], "2026-11-10T10:00:00+01:00", "Merge branch 'feature/a'")
        self.feature("feature/b", ["SHOP-8 Feat: total"], "2026-11-11T10:00:00+01:00", "Merge branch 'feature/b'")
        self.repo.git("checkout", "-q", "main")
        self.repo.merge("develop", "Merge branch 'develop' into 'main'\n\nRelease: SHOP-7 and more",
                        "2026-11-17T10:00:00+01:00")
        self.repo.push()
        found = self.repo.window("2026-11-16", "2026-11-23")
        self.assertEqual(found["releases"][0]["keys"], ["SHOP-7", "SHOP-8"])

    def test_a_squashed_release_is_not_a_hotfix(self):
        self.repo.commit("SHOP-7 Feat: cart", "2026-11-10T10:00:00+01:00")
        self.repo.git("checkout", "-q", "main")
        self.repo.commit("Release: SHOP-7", "2026-11-17T10:00:00+01:00")
        self.repo.push()
        found = self.repo.window("2026-11-16", "2026-11-23")
        self.assertEqual((found["hotfixes"], found["keys"]["SHOP-7"]["released"]), ([], "2026-11-17"))

    def test_a_branch_named_like_an_option_is_refused(self):
        config = self.repo.path / ".tracking/config.md"
        config.write_text(CONFIG.replace("develop", "--output=x"))
        with self.assertRaises(t.Failure):
            t.load_config(config.parent)

    def test_a_missing_branch_is_one_clear_failure(self):
        config = self.repo.path / ".tracking/config.md"
        config.write_text(CONFIG.replace("develop", "trunk"))
        with self.assertRaisesRegex(t.Failure, "no branch 'trunk'"):
            self.repo.window("2026-11-16", "2026-11-23")


class CheckTest(Temp):
    def setUp(self):
        super().setUp()
        self.tracking = self.root / ".tracking"
        self.write("config.md", CONFIG)
        self.write("templates/client.md", "---\nitem-words: 20\nmax-items: 2\nglance-lines: 2\navoid: queue\n---\n")
        self.item("SHOP-1", landed="2026-11-18", demo="demos/cart.mp4")
        self.item("SHOP-2", landed="2026-11-19", folder="SHOP-1/SHOP-2", parent="SHOP-1")
        (self.root / "demos").mkdir()
        (self.root / "demos/cart.mp4").write_text("")
        self.week = self.tracking / "weeks/2026/week-47-from-2026-11-16-to-2026-11-22"
        self.rows("SHOP-1 demo", "SHOP-2 line")
        self.report()

    def write(self, path, text):
        target = self.tracking / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def item(self, key, landed="", folder=None, parent="", released="", demo="", before="It was slow."):
        self.write(f".work/{folder or key}/item.md",
                   f"---\nkey: {key}\nparent: {parent}\nlanded: {landed}\nreleased: {released}\ndemo: {demo}\n---\n"
                   f"## Context\n- **Before:** {before}\n- **Now:** It is fast.\n- **Gain:** Time.\n")

    def rows(self, *rows, week=None, start="2026-11-16", end="2026-11-23"):
        folder = (week or self.week).relative_to(self.tracking)
        table = "".join(f"| {r.split()[0]} | | client | {' '.join(r.split()[1:])} | |\n" for r in rows)
        self.write(f"{folder}/items.md", f"---\nfrom: {start}\nto: {end}\n---\n"
                                         f"| key | landed | format | as | note |\n|---|---|---|---|---|\n{table}")

    def report(self, body="**Now:** The cart is fast.", extra=""):
        (self.week / "client.en.md").write_text(
            f"# Shop\n\n- Faster cart.\n\n## Checkout\n\n### Fast cart\n{body}\n"
            f"▶ [Video](../../../../demos/cart.mp4) · SHOP-1\n\n## Also delivered\n- Labels. SHOP-2\n{extra}")

    def check(self):
        return t.check(self.tracking, self.week, "client", t.load_config(self.tracking))

    def assertProblem(self, text):
        problems = self.check()
        self.assertTrue(any(text in p for p in problems), problems)

    def test_a_good_report_passes(self):
        self.assertEqual(self.check(), [])

    def test_an_item_outside_the_period(self):
        self.item("SHOP-1", landed="2026-11-23")
        self.assertProblem("did not land in the period")

    def test_an_item_already_presented(self):
        earlier = self.tracking / "weeks/2026/week-46-from-2026-11-09-to-2026-11-15"
        self.rows("SHOP-1 demo", week=earlier, start="2026-11-09", end="2026-11-16")
        self.assertProblem("already presented in weeks/2026/week-46")
        self.item("SHOP-1", landed="2026-11-11, 2026-11-18")
        self.rows("SHOP-1 update", "SHOP-2 line")
        self.assertEqual(self.check(), [])

    def test_another_kind_of_period_does_not_count(self):
        month = self.tracking / "months/2026/10-october"
        self.rows("SHOP-1 demo", week=month, start="2026-10-01", end="2026-11-01")
        self.assertEqual(self.check(), [])

    def test_presented_before_the_plugin(self):
        self.write("presented-before.md", "- SHOP-2: 2026-11-09\n")
        self.assertProblem("SHOP-2: already presented in presented-before.md")
        self.write("presented-before.md", "- SHOP-2: 2026-11-15\n")  # the previous week's last day
        self.assertProblem("SHOP-2: already presented in presented-before.md")

    def test_a_row_presented_with_another(self):
        self.item("SHOP-3", landed="2026-11-19", before="not found")
        self.rows("SHOP-1 demo", "SHOP-2 line", "SHOP-3 with SHOP-1")
        self.assertEqual(self.check(), [])
        self.rows("SHOP-1 left-out", "SHOP-2 line", "SHOP-3 with SHOP-1")
        self.assertProblem("SHOP-3: is presented with SHOP-1, which is not itself presented")
        self.rows("SHOP-1 demo", "SHOP-2 line", "SHOP-3 with")
        self.assertProblem("SHOP-3: is presented with nothing")

    def test_an_unknown_key(self):
        self.report(extra="- More. SHOP-77\n")
        self.assertProblem("SHOP-77 is in the report but not in items.md")
        self.rows("SHOP-1 demo", "SHOP-2 line", "SHOP-78 line")
        self.assertProblem("SHOP-78: no such item in .work/")

    def test_a_child_is_covered_by_its_parent(self):
        self.report()
        path = self.week / "client.en.md"
        path.write_text(path.read_text().replace(". SHOP-2", "."))
        self.assertEqual(self.check(), [])

    def test_a_left_out_item_stays_out(self):
        self.rows("SHOP-1 demo", "SHOP-2 left-out")
        self.assertProblem("SHOP-2 is in the report but not in items.md")

    def test_missing_demo_files(self):
        (self.root / "demos/cart.mp4").unlink()
        self.assertProblem("its demo is missing")
        self.assertProblem("no such file")

    def test_limits(self):
        self.report(body="**Now:** " + "word " * 21)
        self.assertProblem("has 22 words, the limit is 20")
        self.report(extra="### Two\nx\n### Three\nx\n")
        self.assertProblem("3 demo items, the limit is 2")
        self.report(body="The queue is fast.")
        self.assertProblem('"queue" is a word this format avoids')

    def test_an_item_nothing_is_known_about_is_not_a_demo(self):
        self.item("SHOP-1", landed="2026-11-18", before="not found")
        self.assertProblem('nothing is known for "Before"')

    def test_production_needs_a_release_in_the_period(self):
        self.rows("SHOP-1 demo", "SHOP-2 production")
        self.assertProblem("SHOP-2: did not reach production")
        self.item("SHOP-2", landed="2026-11-03", released="2026-11-20", folder="SHOP-1/SHOP-2", parent="SHOP-1")
        self.assertEqual(self.check(), [])

    def test_the_command_line_says_what_is_wrong(self):
        self.assertEqual(t.main(["--repo", str(self.root), "check", str(self.week)]), 0)
        self.report(extra="SHOP-77")
        self.assertEqual(t.main(["--repo", str(self.root), "check", str(self.week)]), 1)
        self.assertEqual(t.main(["--repo", str(self.root), "check", str(self.root)]), 2)


if __name__ == "__main__":
    unittest.main()
