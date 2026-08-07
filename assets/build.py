#!/usr/bin/env python3
"""Generate the animated SVG art used by the profile README.

Self-hosted on purpose: no image services, no webfonts, no JavaScript.
Motion is CSS + SMIL only — what GitHub's <img> context actually runs.

    python3 assets/build.py
"""

from __future__ import annotations

import random
from pathlib import Path

OUT = Path(__file__).parent

MONO = "ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
MONO_ADVANCE = 0.6

THEMES = {
    "dark": {
        "name": "#f0f6fc",
        "muted": "#8b949e",
        "faint": "#30363d",
        "accent": "#58a6ff",
        "nebula": 0.09,
        "star_min": 0.2,
        "star_max": 0.7,
    },
    "light": {
        "name": "#0d1117",
        "muted": "#59636e",
        "faint": "#d0d7de",
        "accent": "#0969da",
        "nebula": 0.07,
        "star_min": 0.18,
        "star_max": 0.55,
    },
}

PHRASES = [
    "builds systems that reason",
    "agents · markets · simulations",
    "first principles, then code",
    "small surfaces · honest defaults",
]


def pct(value: float) -> str:
    return f"{round(value, 3):g}%"


def header(theme: dict[str, str | float]) -> str:
    """One composition: ambient field + identity + cycling subtitle."""
    rnd = random.Random(42)
    w, h = 900, 228
    cx = w / 2
    cycle = 16.0
    slot = cycle / len(PHRASES)
    size = 14.5
    sub_y = 168

    # Soft ambient — sparse field that stays behind the type.
    stars = []
    for i in range(38):
        # Keep the center band clearer so the name stays crisp.
        x = rnd.uniform(0, w)
        y = rnd.choice(
            [
                rnd.uniform(8, 48),
                rnd.uniform(178, h - 8),
                rnd.uniform(8, h - 8) if rnd.random() < 0.35 else rnd.uniform(8, 48),
            ]
        )
        r = rnd.uniform(0.4, 1.35)
        base = rnd.uniform(float(theme["star_min"]), float(theme["star_max"]))
        dur = rnd.uniform(2.8, 6.0)
        delay = rnd.uniform(-7, 0)
        stars.append(
            f'    <circle class="star" cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" '
            f'style="--b:{base:.2f};animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"/>'
        )

    phrases = []
    for i, phrase in enumerate(PHRASES):
        text_w = len(phrase) * size * MONO_ADVANCE
        caret_x = cx + text_w / 2 + 5
        delay = i * slot
        phrases.append(
            f'  <g class="phrase" style="animation-delay:{delay:g}s">\n'
            f'    <text x="{cx:g}" y="{sub_y}" class="sub">{phrase}</text>\n'
            f'    <rect class="caret" x="{caret_x:.1f}" y="{sub_y - 11}" '
            f'width="1.7" height="14" rx="0.85"/>\n'
            f"  </g>"
        )

    hold = (slot - 0.55) / cycle * 100
    phrase_kf = (
        "@keyframes cycle{"
        f"0%{{opacity:0}}1.5%{{opacity:1}}{pct(hold)}{{opacity:1}}"
        f"{pct(slot / cycle * 100)}{{opacity:0}}100%{{opacity:0}}"
        "}"
    )

    kicker = "SAHAJPATEL123"
    tracking = 1.8
    kicker_w = len(kicker) * (11 * MONO_ADVANCE + tracking)
    unit_w = 6 + 10 + kicker_w
    row_left = cx - unit_w / 2
    dot_x = row_left + 3
    kicker_x = row_left + 6 + 10 + kicker_w / 2
    rule_y = h - 18

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Sahaj Patel — builds systems that reason">
  <title>Sahaj Patel</title>
  <defs>
    <radialGradient id="nebL">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity="{theme['nebula']}"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" gradientUnits="userSpaceOnUse" x1="{cx - 200:g}" y1="0" x2="{cx + 200:g}" y2="0">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{theme['accent']}" stop-opacity="0.75"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    .star {{ fill: {theme['accent']}; opacity: var(--b, 0.4); animation: twinkle 3.2s ease-in-out infinite; }}
    @keyframes twinkle {{ 0%, 100% {{ opacity: var(--b, 0.4) }} 50% {{ opacity: calc(var(--b, 0.4) * 0.2) }} }}
    .neb {{ animation: drift 28s ease-in-out infinite alternate; }}
    .neb.r {{ animation-duration: 36s; animation-direction: alternate-reverse; }}
    @keyframes drift {{ from {{ transform: translateX(-14px) }} to {{ transform: translateX(14px) }} }}
    .kicker {{ font-family: {MONO}; font-size: 11px; letter-spacing: {tracking}px; fill: {theme['muted']}; text-anchor: middle; }}
    .name {{ font-family: {SANS}; font-size: 54px; font-weight: 600; letter-spacing: -1.4px; fill: {theme['name']}; text-anchor: middle; }}
    .sub {{ font-family: {MONO}; font-size: {size:g}px; fill: {theme['muted']}; text-anchor: middle; }}
    .caret {{ fill: {theme['accent']}; animation: blink 1.1s steps(2, start) infinite; }}
    .phrase {{ opacity: 0; animation: cycle {cycle:g}s linear infinite; }}
    .rise {{ animation: rise 0.85s cubic-bezier(0.2, 0.7, 0.2, 1) both; }}
    .fade {{ animation: rise 0.85s cubic-bezier(0.2, 0.7, 0.2, 1) 0.2s both; }}
    .draw {{ stroke-dasharray: 400; stroke-dashoffset: 400; animation: draw 1.5s cubic-bezier(0.3, 0.8, 0.2, 1) 0.35s both; }}
    .dot {{ animation: beat 2.8s ease-in-out infinite; }}
    {phrase_kf}
    @keyframes blink {{ 0%, 100% {{ opacity: 1 }} 50% {{ opacity: 0 }} }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px) }} to {{ opacity: 1; transform: none }} }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0 }} }}
    @keyframes beat {{ 0%, 100% {{ opacity: 1 }} 50% {{ opacity: 0.35 }} }}
    @media (prefers-reduced-motion: reduce) {{
      .star, .neb, .phrase, .caret, .rise, .fade, .draw, .dot {{ animation: none }}
      .phrase {{ opacity: 0 }}
      .phrase:first-of-type {{ opacity: 1 }}
      .draw {{ stroke-dashoffset: 0 }}
      .star {{ opacity: var(--b, 0.4) }}
    }}
  </style>

  <ellipse class="neb" cx="160" cy="56" rx="140" ry="36" fill="url(#nebL)"/>
  <ellipse class="neb r" cx="740" cy="190" rx="150" ry="38" fill="url(#nebL)"/>
  <g>
{chr(10).join(stars)}
  </g>

  <g class="fade">
    <circle cx="{dot_x:.1f}" cy="42" r="2.8" fill="{theme['accent']}" class="dot"/>
    <circle cx="{dot_x:.1f}" cy="42" r="2.8" fill="none" stroke="{theme['accent']}" stroke-width="1">
      <animate attributeName="r" values="2.8;11" dur="2.8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.45;0" dur="2.8s" repeatCount="indefinite"/>
    </circle>
    <text x="{kicker_x:.1f}" y="46" class="kicker">{kicker}</text>
  </g>

  <g class="rise">
    <text x="{cx:g}" y="112" class="name">Sahaj Patel</text>
  </g>

{chr(10).join(phrases)}

  <line x1="{cx - 200:g}" y1="{rule_y:g}" x2="{cx + 200:g}" y2="{rule_y:g}" stroke="url(#rule)" stroke-width="1.3" stroke-linecap="round" class="draw"/>
</svg>
"""


def divider(theme: dict[str, str | float]) -> str:
    """A single quiet rule used once between major sections."""
    w, h = 900, 28
    cx = w / 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-hidden="true">
  <defs>
    <linearGradient id="d" gradientUnits="userSpaceOnUse" x1="{cx - 160:g}" y1="0" x2="{cx + 160:g}" y2="0">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{theme['accent']}" stop-opacity="0.45"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <line x1="{cx - 160:g}" y1="{h / 2:g}" x2="{cx + 160:g}" y2="{h / 2:g}" stroke="url(#d)" stroke-width="1" stroke-linecap="round">
    <animate attributeName="opacity" values="0.55;1;0.55" dur="4.5s" repeatCount="indefinite"/>
  </line>
</svg>
"""


def main() -> None:
    for theme_name, palette in THEMES.items():
        (OUT / f"header-{theme_name}.svg").write_text(header(palette), encoding="utf-8")
        (OUT / f"divider-{theme_name}.svg").write_text(divider(palette), encoding="utf-8")
    for stale in list(OUT.glob("stars-*.svg")) + list(OUT.glob("orbit-*.svg")) + list(OUT.glob("loop-*.svg")):
        stale.unlink()
    print("wrote", *(p.name for p in sorted(OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
