"""Generate Tokyo Night themed SVG code cards for the profile README.

Usage:  python scripts/generate_code_cards.py
Output: assets/code-*.svg

Edit the SNIPPETS dict below, re-run, commit the regenerated SVGs.
"""

import re
from pathlib import Path

# ---------------------------------------------------------------- theme ----
BG = "#1a1b27"
BORDER = "#2f334d"
FG = "#a9b1d6"
LINENO = "#3b4261"
STRING = "#9ece6a"
CLASS = "#7dcfff"
METHOD = "#7aa2f7"
KEYWORD = "#bb9af7"
CONST = "#ff9e64"
OPERATOR = "#89ddff"
TITLE = "#565f89"
DOTS = ("#f7768e", "#e0af68", "#9ece6a")
GRADIENT = ("#1e3a8a", "#2563eb", "#38bdf8")

FONT = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
FONT_SIZE = 14
LINE_H = 22
CHAR_W = 8.45          # approx monospace advance at 14px
CHROME_H = 44
PAD_X = 24
PAD_Y = 22
GUTTER_W = 36          # line-number column
WIDTH = 900

KEYWORDS = {"if", "return", "for", "foreach", "while", "new", "function"}
BOOLS = {"true", "false", "null"}

TOKEN_RE = re.compile(
    r"""('(?:[^'\\]|\\.)*')   # 1 string
      | (->|::|=>)            # 2 operator
      | ([A-Za-z_][A-Za-z0-9_]*) # 3 identifier
      | (\s+)                 # 4 whitespace
      | (.)                   # 5 anything else (punctuation)
    """,
    re.VERBOSE,
)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def highlight_line(line: str) -> str:
    """Return the line as colored <tspan> markup."""
    out = []
    prev_op = False  # previous significant token was -> or ::
    for m in TOKEN_RE.finditer(line):
        string, op, ident, ws, punct = m.groups()
        if string is not None:
            out.append(f'<tspan fill="{STRING}">{esc(string)}</tspan>')
            prev_op = False
        elif op is not None:
            out.append(f'<tspan fill="{OPERATOR}">{esc(op)}</tspan>')
            prev_op = True
        elif ident is not None:
            if ident in KEYWORDS:
                color = KEYWORD
            elif ident in BOOLS:
                color = CONST
            elif prev_op and ident.isupper():
                color = CONST                      # ResponsesEnum::PERFECT
            elif prev_op:
                color = METHOD                     # ->method() / ::method()
            elif ident[0].isupper():
                color = CLASS                      # Developer, Stack, ...
            else:
                color = FG
            out.append(f'<tspan fill="{color}">{esc(ident)}</tspan>')
            prev_op = False
        elif ws is not None:
            out.append(esc(ws))
        else:
            out.append(f'<tspan fill="{FG}">{esc(punct)}</tspan>')
            prev_op = False
    return "".join(out)


def render_card(title: str, code: str) -> str:
    lines = code.strip("\n").split("\n")
    height = CHROME_H + PAD_Y + len(lines) * LINE_H + PAD_Y
    code_x = PAD_X + GUTTER_W

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" font-family="{FONT}">',
        "<defs>",
        '<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0%" stop-color="{GRADIENT[0]}"/>',
        f'<stop offset="50%" stop-color="{GRADIENT[1]}"/>',
        f'<stop offset="100%" stop-color="{GRADIENT[2]}"/>',
        "</linearGradient>",
        f'<clipPath id="card"><rect width="{WIDTH}" height="{height}" rx="12"/></clipPath>',
        "</defs>",
        # card body + border
        f'<rect width="{WIDTH}" height="{height}" rx="12" fill="{BG}"/>',
        '<g clip-path="url(#card)">',
        f'<rect width="{WIDTH}" height="4" fill="url(#accent)"/>',
        "</g>",
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="12" '
        f'fill="none" stroke="{BORDER}"/>',
    ]

    # window chrome
    for i, dot in enumerate(DOTS):
        parts.append(f'<circle cx="{PAD_X + i * 20}" cy="{CHROME_H // 2 + 2}" r="6" fill="{dot}"/>')
    parts.append(
        f'<text x="{WIDTH / 2}" y="{CHROME_H // 2 + 7}" text-anchor="middle" '
        f'font-size="13" fill="{TITLE}">{esc(title)}</text>'
    )
    parts.append(
        f'<line x1="0" y1="{CHROME_H}" x2="{WIDTH}" y2="{CHROME_H}" stroke="{BORDER}"/>'
    )

    # code lines
    y = CHROME_H + PAD_Y + FONT_SIZE
    last_len = 0
    for n, line in enumerate(lines, start=1):
        parts.append(
            f'<text x="{PAD_X + GUTTER_W - 14}" y="{y}" text-anchor="end" '
            f'font-size="{FONT_SIZE}" fill="{LINENO}">{n}</text>'
        )
        if line.strip():
            parts.append(
                f'<text x="{code_x}" y="{y}" font-size="{FONT_SIZE}" fill="{FG}" '
                f'xml:space="preserve">{highlight_line(line)}</text>'
            )
        last_len = len(line)
        y += LINE_H

    # blinking cursor after the last line
    cursor_x = code_x + last_len * CHAR_W + 4
    cursor_y = y - LINE_H - FONT_SIZE + 2
    parts.append(
        f'<rect x="{cursor_x:.0f}" y="{cursor_y}" width="8" height="{FONT_SIZE + 3}" '
        f'fill="{GRADIENT[2]}"><animate attributeName="opacity" values="1;0;1" '
        'dur="1.4s" repeatCount="indefinite"/></rect>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


# ------------------------------------------------------------- snippets ----
SNIPPETS = {
    "code-specialties": ("Specialties.php", """
Developer::specializesIn()
    ->apiDesign('RESTful', 'scalable architecture')
    ->laravelEcosystem('packages', 'advanced patterns')
    ->databaseOptimization('MySQL', 'MariaDB', 'performance tuning')
    ->devOpsDeployment('Docker', 'Azure', 'CI/CD pipelines')
    ->selfHostedSolutions('infrastructure', 'automation')
    ->aiAugmentedEngineering('agentic workflows', 'human-led quality')
    ->domainExpertise(['Real Estate', 'FinTech', 'Media', 'Aviation'])
    ->systemModernization('legacy migration', 'maintainability')
    ->codeQuality('security audits', 'performance analysis');
"""),
    "code-currently": ("CurrentlyBusyWith.php", """
Developer::currently()
    ->buildingApisFor('Enterprise solutions')
    ->shippingOpenSource([
        'win12 - a Windows-style web desktop (PWA, i18n, themes)',
        'Laravel packages & starter kits'
    ])
    ->upskilling([
        'automated engineering workflows',
        'Cloud infrastructure',
        'System design patterns'
    ])
    ->seekingCollaboration('Digital professionals')
    ->collaboratingWith('trusted developers in my network');
"""),
    "code-ideal-work-day": ("IdealWorkDay.php", """
if(Day::hasIdealWorkDay(
    IdealWorkDay::start()
        ->remoteWork(true)
        ->coffee('dark', 'sweet')
        ->withMusic('Lo-Fi', 'Chillstep')
        ->withoutCalls()
)) {
    return ResponsesEnum::PERFECT;
}
"""),
    "code-daily-drivers": ("DailyDrivers.php", """
Stack::daily()
    ->languages(['PHP', 'JavaScript', 'Python', 'SQL'])
    ->frameworks(['Laravel', 'Bootstrap', 'MySQL'])
    ->tools(['Docker', 'Postman', 'Git', 'PHPStorm', 'WebStorm', 'Claude Code'])
    ->databases(['MySQL', 'MariaDB', 'SQLite']);
"""),
    "code-infrastructure": ("Infrastructure.php", """
Infrastructure::preferred()
    ->cloud('Azure', 'Docker containers')
    ->deployment('CI/CD pipelines', 'automated testing')
    ->local('Laravel Herd', 'Docker Compose')
    ->monitoring('Laravel Telescope', 'custom dashboards');
"""),
    "code-services": ("Services.php", """
Services::available()
    ->consulting('System Architecture', 'Technical Audits', 'Performance Analysis')
    ->development('Custom Solutions', 'API Design', 'Full-Stack Applications')
    ->modernization('Legacy System Migration', 'Code Quality Improvement', 'DevOps Integration')
    ->codeReview('Security Audits', 'Performance Optimization', 'Best Practices')
    ->mentorship('Laravel Ecosystem', 'System Design', 'Scalable Architecture');

Collaboration::open()
    ->for(['startups', 'agencies', 'enterprises'])
    ->offering('flexible engagement', 'realistic timelines', 'transparent communication')
    ->contactMe('thatobabusi.co.za/contact')
    ->schedule('LinkedIn or Website booking')
    ->availability('Full-time, Part-time, Contract, Advisory');
"""),
}


def main() -> None:
    out_dir = Path(__file__).resolve().parent.parent / "assets"
    out_dir.mkdir(exist_ok=True)
    for name, (title, code) in SNIPPETS.items():
        path = out_dir / f"{name}.svg"
        path.write_text(render_card(title, code), encoding="utf-8")
        print(f"wrote {path.relative_to(out_dir.parent)}")


if __name__ == "__main__":
    main()
