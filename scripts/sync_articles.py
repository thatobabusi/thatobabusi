"""Sync blog posts from thatobabusi.co.za into the profile.

Usage:  python scripts/sync_articles.py

- Scrapes the blog index for post links, fetches each post's <title>
- Writes the full list to docs/ARTICLES.md
- Updates the "Latest from the blog" block in README.md (between the
  LATEST-POSTS markers), excluding posts already in the curated table

The curated table in README.md is never touched — it stays hand-picked.
"""

import re

from _common import ROOT, fetch, replace_between

BLOG_INDEX = "https://thatobabusi.co.za/blog"
README = ROOT / "README.md"
DOC = ROOT / "docs" / "ARTICLES.md"
MAX_LATEST_IN_README = 6
MAX_POSTS_FETCHED = 15

TOPIC_RULES = [
    (r"php", "PHP"),
    (r"laravel|repository|pattern|architecture", "Architecture"),
    (r"productivity|context-switching", "Productivity"),
    (r"developer|coding|troubleshooting|programming", "Dev Life"),
    (r"review|movie|show|series|snowpiercer|star-trek|scifi|dust|hijack|apex", "Review"),
]


def slug_topic(slug: str) -> str:
    for pattern, topic in TOPIC_RULES:
        if re.search(pattern, slug):
            return topic
    return "Blog"


def slug_title(slug: str) -> str:
    return slug.replace("-", " ").title()


def post_urls(index_html: str) -> list[str]:
    urls = re.findall(r'href="(https?://thatobabusi\.co\.za/(?:blog|blog-legacy-single)/[^"#]+)"',
                      index_html)
    seen, out = set(), []
    for u in urls:
        slug = u.rstrip("/").rsplit("/", 1)[1]
        if slug and slug not in seen:
            seen.add(slug)
            out.append(u)
    return out


def page_title(url: str, slug: str) -> str:
    try:
        html = fetch(url, timeout=25)
    except Exception:
        return slug_title(slug)
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m:
        return slug_title(slug)
    title = re.sub(r"\s+", " ", m.group(1)).strip()
    # strip common "| Site" / "- Site" suffixes
    title = re.split(r"\s+[|\-–]\s+(?:Thato\s*Babusi|thatobabusi).*$", title, flags=re.I)[0]
    return title.strip() or slug_title(slug)


def main() -> None:
    index_html = fetch(BLOG_INDEX)
    posts = []
    for url in post_urls(index_html)[:MAX_POSTS_FETCHED]:
        slug = url.rstrip("/").rsplit("/", 1)[1]
        posts.append({"url": url, "slug": slug,
                      "title": page_title(url, slug), "topic": slug_topic(slug)})
    if not posts:
        raise SystemExit("no posts found on the blog index — layout changed?")

    # docs/ARTICLES.md — everything found, plus whatever the curated table has
    lines = ["# Articles",
             "",
             "All posts discovered on [thatobabusi.co.za/blog](https://thatobabusi.co.za/blog),",
             "auto-synced daily by the [Docs Automation workflow](../.github/workflows/docs-automation.yml).",
             "",
             "| 📖 Post | 🏷️ Topic |",
             "|:--------|:--------:|"]
    for p in posts:
        lines.append(f"| [{p['title']}]({p['url']}) | `{p['topic']}` |")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # README latest block — skip posts already linked anywhere else in README
    readme_text = README.read_text(encoding="utf-8")
    marker_free = re.sub(r"<!-- LATEST-POSTS:START -->.*?<!-- LATEST-POSTS:END -->",
                         "", readme_text, flags=re.S)
    fresh = [p for p in posts if p["slug"] not in marker_free][:MAX_LATEST_IN_README]
    if fresh:
        body = ["| 📖 Post | 🏷️ Topic |", "|:--------|:--------:|"]
        body += [f"| [{p['title']}]({p['url']}) | `{p['topic']}` |" for p in fresh]
        block = "\n".join(body)
    else:
        block = "_No new posts beyond the curated picks above._"
    changed = replace_between(README, "<!-- LATEST-POSTS:START -->",
                              "<!-- LATEST-POSTS:END -->", block)
    print(f"docs/ARTICLES.md: {len(posts)} posts | README latest block: "
          f"{len(fresh)} posts ({'updated' if changed else 'unchanged'})")


if __name__ == "__main__":
    main()
