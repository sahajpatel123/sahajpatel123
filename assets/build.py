#!/usr/bin/env python3
"""Generate the animated SVG art used by the profile README.

Self-hosted: no image services, no webfonts, no JavaScript.
Motion is CSS + SMIL only — what GitHub's <img> context runs.

    python3 assets/build.py
"""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).parent

MONO = "ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
MONO_ADVANCE = 0.6

THEMES = {
    "dark": {
        "name": "#f0f6fc",
        "muted": "#8b949e",
        "accent": "#58a6ff",
        "nebula": 0.08,
        "rule_mid": 0.70,
        "dot_pulse": 0.40,
    },
    "light": {
        "name": "#1f2328",
        "muted": "#656d76",
        "accent": "#0969da",
        "nebula": 0.06,
        "rule_mid": 0.55,
        "dot_pulse": 0.35,
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


def header(theme: dict[str, float | str]) -> str:
    """One composition: faint nebula wash + identity + cycling subtitle."""
    w, h = 900, 220
    cx = 450.0
    cycle = 16.0
    slot = cycle / len(PHRASES)
    size = 14.5
    sub_y = 158

    phrases = []
    for i, phrase in enumerate(PHRASES):
        text_w = len(phrase) * size * MONO_ADVANCE
        caret_x = cx + text_w / 2 + 5
        delay = i * slot
        phrases.append(
            f'  <g class="phrase" style="animation-delay:{delay:g}s">\n'
            f'    <text x="{cx:g}" y="{sub_y}" class="sub">{phrase}</text>\n'
            f'    <rect class="caret" x="{caret_x:.1f}" y="{sub_y - 11}" '
            f'width="1.7" height="13" rx="0.85"/>\n'
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

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Sahaj Patel — builds systems that reason">
  <title>Sahaj Patel</title>
  <defs>
    <radialGradient id="neb">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity="{theme['nebula']}"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" gradientUnits="userSpaceOnUse" x1="250" y1="0" x2="650" y2="0">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{theme['accent']}" stop-opacity="{theme['rule_mid']}"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    .neb {{ animation: drift 28s ease-in-out infinite alternate; }}
    .neb.b {{ animation-duration: 36s; animation-direction: alternate-reverse; }}
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
      .neb, .phrase, .caret, .rise, .fade, .draw, .dot {{ animation: none }}
      .phrase {{ opacity: 0 }}
      .phrase:first-of-type {{ opacity: 1 }}
      .draw {{ stroke-dashoffset: 0 }}
    }}
  </style>

  <ellipse class="neb" cx="148" cy="48" rx="132" ry="34" fill="url(#neb)"/>
  <ellipse class="neb b" cx="752" cy="182" rx="142" ry="36" fill="url(#neb)"/>

  <g class="fade">
    <circle cx="{dot_x:.1f}" cy="38" r="2.8" fill="{theme['accent']}" class="dot"/>
    <circle cx="{dot_x:.1f}" cy="38" r="2.8" fill="none" stroke="{theme['accent']}" stroke-width="1">
      <animate attributeName="r" values="2.8;10" dur="2.8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="{theme['dot_pulse']};0" dur="2.8s" repeatCount="indefinite"/>
    </circle>
    <text x="{kicker_x:.1f}" y="42" class="kicker">{kicker}</text>
  </g>

  <g class="rise">
    <text x="{cx:g}" y="106" class="name">Sahaj Patel</text>
  </g>

{chr(10).join(phrases)}

  <line x1="250" y1="198" x2="650" y2="198" stroke="url(#rule)" stroke-width="1.2" stroke-linecap="round" class="draw"/>
</svg>
"""


def main() -> None:
    for theme_name, palette in THEMES.items():
        (OUT / f"header-{theme_name}.svg").write_text(header(palette), encoding="utf-8")
    for stale in (
        list(OUT.glob("divider-*.svg"))
        + list(OUT.glob("stars-*.svg"))
        + list(OUT.glob("orbit-*.svg"))
        + list(OUT.glob("loop-*.svg"))
    ):
        stale.unlink()
    print("wrote", *(p.name for p in sorted(OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
