"""Generate docs/PROJECTS.md — live inventory of public repos via the GitHub API.

Usage:  python scripts/generate_projects.py
Uses GITHUB_TOKEN from the environment when present (CI); anonymous otherwise.
Forks are excluded by default; repos sorted by last push.

GitHub's `fork` flag is ancestry, not content — a repo started from a
template or upstream scaffold stays flagged `fork: true` forever even
after it's been rebuilt into an original product (e.g. win12 grew from a
web-desktop template; the boom-bap-producer-*-public repos share a common
public-repo scaffold across the product family). Blanket-excluding forks
silently drops genuinely original, actively-maintained work. INCLUDE_FORKS
below is the manual allowlist for exactly that case — same pattern as
MANUAL_ROWS in update_stats.py. Leave off anything that really is just a
kept-current mirror of someone else's project (those stay excluded).
"""

import json
import os
import urllib.request
from datetime import datetime, timezone

from _common import ROOT, UA

USER = "thatobabusi"
DOC = ROOT / "docs" / "PROJECTS.md"

INCLUDE_FORKS = {
    "win12",
    "win12-locales",
    "boom-bap-producer-pads-public",
    "boom-bap-producer-decks-public",
    "adminlte-laravel",
    "laravel-installer",
    "iseed",
    "php-vanilla-oop-login",
}


def api(url: str):
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers),
                                timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    repos = api(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed")
    repos = [r for r in repos if not r["fork"] or r["name"] in INCLUDE_FORKS]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = ["# Projects",
             "",
             f"Public repositories of [@{USER}](https://github.com/{USER})",
             "(originals, plus a few substantially-rebuilt forks — see `INCLUDE_FORKS`",
             "in the generator), sorted by most recent push. Auto-generated daily by the",
             "[Docs Automation workflow](../.github/workflows/docs-automation.yml).",
             "",
             f"**Last generated:** {now} — {len(repos)} repositories",
             "",
             "| Repository | Description | Language | ⭐ | Last push |",
             "|:-----------|:------------|:---------|:--:|:----------|"]
    for r in repos:
        desc = (r["description"] or "—").replace("|", "\\|")
        lang = r["language"] or "—"
        pushed = r["pushed_at"][:10]
        lines.append(f"| [{r['name']}]({r['html_url']}) | {desc} | {lang} "
                     f"| {r['stargazers_count']} | {pushed} |")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote docs/PROJECTS.md ({len(repos)} repos)")


if __name__ == "__main__":
    main()
