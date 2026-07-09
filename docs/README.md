# Documentation

This repository powers the GitHub profile of [@thatobabusi](https://github.com/thatobabusi) — the `README.md` at the root renders on [github.com/thatobabusi](https://github.com/thatobabusi).

🌍 **Website:** [thatobabusi.co.za](https://thatobabusi.co.za)

## Repository structure

| Path | Purpose |
|:-----|:--------|
| `README.md` | The profile page itself |
| `assets/` | Committed SVGs: code cards, travel map, travel wishlist |
| `scripts/generate_code_cards.py` | Generator for the themed code-card SVGs in `assets/` |
| `.github/workflows/metrics.yml` | Daily job that builds `github-metrics.svg` (stats dashboard) |
| `.github/workflows/snake.yml` | Twice-daily job that builds the contribution snake on the `output` branch |
| `docs/` | This documentation |
| `docs/RELEASES.md` | Versioning approach and release history |

## Theme

Everything follows one palette so the profile reads as a single design:

| Token | Value | Used for |
|:------|:------|:---------|
| Gradient | `#1e3a8a → #2563eb → #38bdf8` | Banner, footer wave, card accent strips |
| Card background | `#1a1b27` (Tokyo Night) | Code cards, badge labels, stats cards |
| Card border | `#2f334d` | Code card outlines |
| Accent blue | `#2563eb` | Badges, contribution calendar |

## Updating the code cards

The "About Me" code blocks are pre-rendered SVGs, not markdown fences, so they
keep their syntax colors in every GitHub theme.

1. Edit the snippet in the `SNIPPETS` dict at the bottom of
   [`scripts/generate_code_cards.py`](../scripts/generate_code_cards.py)
2. Run `python scripts/generate_code_cards.py` (no dependencies, Python 3.8+)
3. Commit the regenerated `assets/code-*.svg` files

## Stats & graphs

External services used by the README (all verified working as of 2026-07-09):

- **shields.io** — follower/stars/repo badges
- **streak-stats.demolab.com** — contribution streak card
- **ghchart.rshah.org** — 12-month contribution calendar
- **skillicons.dev** — tech stack icons
- **capsule-render** / **readme-typing-svg** — banner and typing animation

Self-hosted via GitHub Actions (no third-party server at render time):

- `github-metrics.svg` — committed to `main` by the Metrics workflow
- `github-snake.svg` — committed to the `output` branch by the Snake workflow

Both workflows can be run manually from the **Actions** tab. If the Metrics
workflow fails with a token/permissions error, create a classic PAT with no
scopes and save it as a repo secret named `METRICS_TOKEN`.

> Avoided on purpose: `github-readme-stats.vercel.app` (chronically
> rate-limited), `github-profile-summary-cards` (too slow for GitHub's image
> proxy), `github-profile-trophy` and `github-contributor-stats` (now paid),
> `github-readme-activity-graph` (broken fetch).
