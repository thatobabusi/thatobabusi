# scripts/

Plain-Python generators and checkers behind the profile automation.
**Zero dependencies** — standard library only, Python 3.8+.

| Script | What it does | Run by |
|:-------|:-------------|:-------|
| `_common.py` | Shared helpers: `fetch()`, marker-based `replace_between()` | (imported by the others) |
| `generate_code_cards.py` | Renders the About Me snippets as themed SVG code cards into `assets/` | [Code Cards workflow](../.github/workflows/code-cards.yml) on generator changes |
| `generate_changelog.py` | Rebuilds `docs/CHANGELOG.md` from git history, grouped by month | [Changelog workflow](../.github/workflows/changelog.yml) on every push |
| `sync_articles.py` | Scrapes the blog, writes `docs/ARTICLES.md`, fills the README "Latest from the blog" block | [Docs Automation](../.github/workflows/docs-automation.yml) daily |
| `generate_projects.py` | GitHub API repo inventory → `docs/PROJECTS.md` | Docs Automation daily |
| `update_stats.py` | Refreshes the README Impact Stats table (live GitHub numbers + manual rows in `MANUAL_ROWS`) | Docs Automation daily |
| `generate_docs_index.py` | Regenerates the file index in `docs/README.md` | Docs Automation daily |
| `check_links.py` | Checks every external URL in the README → `docs/LINK-HEALTH.md` | Docs Automation daily |
| `prepare_release.py` | Prepends a version section to `docs/RELEASES.md` | [Release workflow](../.github/workflows/release.yml) (one-click) |

## Running locally

```bash
python scripts/<name>.py
```

Conventions:

- Scripts that edit `README.md` or `docs/README.md` only touch the region
  between `<!-- X:START -->` / `<!-- X:END -->` marker comments — everything
  outside the markers is hand-written and never overwritten.
- `GITHUB_TOKEN` is read from the environment when present (CI); anonymous
  API calls work locally within rate limits.
- On Windows, if you hit `SSL: CERTIFICATE_VERIFY_FAILED`, point Python at a
  current CA bundle first:
  `set SSL_CERT_FILE=C:\Python310\lib\site-packages\certifi\cacert.pem`
