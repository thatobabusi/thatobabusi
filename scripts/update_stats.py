"""Refresh the Impact Stats table in README.md (between the STATS markers).

Usage:  python scripts/update_stats.py

Auto-derived rows come from the GitHub API and the synced article list;
hand-maintained rows live in MANUAL_ROWS below — edit them there.
"""

import json
import os
import re
import urllib.request
from datetime import date

from _common import ROOT, UA, replace_between

USER = "thatobabusi"
CAREER_START = date(2013, 7, 8)  # work anniversary
README = ROOT / "README.md"
ARTICLES = ROOT / "docs" / "ARTICLES.md"

MANUAL_ROWS = [
    ("💻 Active Projects", "10+ (win12, IPTV, Full-Stack Upskilling, +7 more)"),
    ("📊 Portfolio Projects", "9 public/notable projects showcased"),
    ("🌍 Industries Served",
     "Aviation & Auditing, Transport & Logistics, HRM, Media, Research"),
    ("🏆 BBBEE Status", "Level 1 - 100% Black-owned"),
    ("🛠️ Tech Stack", "14+ technologies (PHP, Laravel, Python, Docker, Azure, +10 more)"),
    ("🎓 Certifications",
     "Staffordshire University, Asia Pacific University, Mater Spei College"),
]


def github_user():
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com/users/{USER}", headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    user = github_user()
    years = (date.today() - CAREER_START).days // 365

    article_count = None
    if ARTICLES.exists():
        article_count = len(re.findall(r"^\| \[", ARTICLES.read_text(encoding="utf-8"),
                                       re.M))

    rows = [
        ("⭐ Experience", f"{years}+ years systems development across 5 industries"),
        ("📦 Public Repos", f"{user['public_repos']} on GitHub"),
        ("👥 GitHub Followers", str(user["followers"])),
    ]
    if article_count:
        rows.append(("📝 Published Articles",
                     f"{article_count} articles on [thatobabusi.co.za](https://thatobabusi.co.za/blog)"))
    rows.extend(MANUAL_ROWS)

    body = ["| Metric | Value |", "|--------|-------|"]
    body += [f"| {k} | {v} |" for k, v in rows]
    changed = replace_between(README, "<!-- STATS:START -->", "<!-- STATS:END -->",
                              "\n".join(body))
    print(f"stats table: {len(rows)} rows ({'updated' if changed else 'unchanged'})")


if __name__ == "__main__":
    main()
