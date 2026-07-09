# .github/workflows/

The automation behind the profile. All bots commit as `github-actions[bot]`
with `[skip ci]` where appropriate; commits made with the built-in token
never retrigger workflows, so there are no loops.

| Workflow | Trigger | What it does |
|:---------|:--------|:-------------|
| `metrics.yml` | daily 06:00 SAST + manual | Builds `github-metrics.svg` (stats dashboard) and commits it to `main` |
| `snake.yml` | twice daily + manual | Builds the contribution snake and publishes it to the `output` branch |
| `changelog.yml` | every push to `main` + manual | Regenerates `docs/CHANGELOG.md` from git history |
| `docs-automation.yml` | daily 06:30 SAST + manual | Blog sync, project inventory, stats refresh, docs index, link health; opens a `link-health` issue when README links break |
| `release.yml` | manual (Actions tab form) | One-click release: updates `docs/RELEASES.md`, commits, tags `vX.Y.Z`, publishes the GitHub Release |
| `code-cards.yml` | push touching the card generator + manual | Regenerates the SVG code cards in `assets/` if they drifted |

The scripts these workflows call live in [`scripts/`](../../scripts/README.md);
process documentation lives in [`docs/`](../../docs/README.md).

> **Why is there no `.github/README.md`?** GitHub gives `.github/README.md`
> display priority over the root `README.md`, which would replace the profile
> page content. This file lives one level deeper on purpose.
