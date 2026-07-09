"""Insert a new version section at the top of docs/RELEASES.md history.

Usage:  python scripts/prepare_release.py 2.2.0 "Short summary" "- bullet one
- bullet two"

Used by the one-click Release workflow; can also be run locally.
"""

import re
import sys
from datetime import date

from _common import ROOT

RELEASES = ROOT / "docs" / "RELEASES.md"


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("usage: prepare_release.py <version> <summary> [notes]")
    version = sys.argv[1].lstrip("v")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit(f"bad version: {version!r} (expected X.Y.Z)")
    summary = sys.argv[2].strip()
    notes = sys.argv[3].strip() if len(sys.argv) > 3 else ""

    text = RELEASES.read_text(encoding="utf-8")
    if f"### v{version} " in text:
        raise SystemExit(f"v{version} already in RELEASES.md")

    section = f"### v{version} — {date.today().isoformat()}\n\n{summary}\n"
    if notes:
        section += f"\n{notes}\n"

    anchor = "## Release history\n"
    if anchor not in text:
        raise SystemExit("'## Release history' heading not found")
    text = text.replace(anchor, anchor + "\n" + section, 1)
    RELEASES.write_text(text, encoding="utf-8")
    print(f"added v{version} section to docs/RELEASES.md")


if __name__ == "__main__":
    main()
