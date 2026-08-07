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
        "faint": "#30363d",
        "accent": "#58a6ff",
        "live": "#3fb950",
        "nebula": 0.08,
        "rule_mid": 0.70,
        "dot_pulse": 0.40,
    },
    "light": {
        "name": "#1f2328",
        "muted": "#656d76",
        "faint": "#d0d7de",
        "accent": "#0969da",
        "live": "#1a7f37",
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


def intro(theme: dict[str, float | str]) -> str:
    """Animated triad: models → markets → contracts, with a live currently line.

    A pulse travels the wires so the section feels alive without reading as a
    flowchart. Soft node halos light as the pulse arrives.
    """
    w, h = 900, 236
    cy = 78.0
    nodes = [
        ("models", "coordinate", 150.0),
        ("markets", "price uncertainty", 450.0),
        ("contracts", "become legible", 750.0),
    ]
    box_w, box_h = 148.0, 36.0
    cycle = 7.2  # seconds for a full pulse lap

    # Timeline: dwell on node, travel, dwell, travel, dwell, return pause.
    dwell, travel = 0.9, 1.5
    # 3 dwells + 2 travels = 5.7; pad to cycle with a soft reset.
    node_windows = []
    segments = []
    t = 0.0
    for i in range(3):
        node_windows.append((t, t + dwell))
        t += dwell
        if i < 2:
            segments.append((t, t + travel))
            t += travel

    # Paths between node edges.
    edges = []
    for i in range(2):
        x0 = nodes[i][2] + box_w / 2 + 10
        x1 = nodes[i + 1][2] - box_w / 2 - 10
        edges.append(f"M {x0:.1f} {cy} L {x1:.1f} {cy}")

    node_markup = []
    halo_css = []
    keyframes = []
    for i, (label, verb, cx) in enumerate(nodes):
        x = cx - box_w / 2
        lo, hi = node_windows[i][0] / cycle * 100, node_windows[i][1] / cycle * 100
        keyframes.append(
            f"@keyframes n{i}{{"
            f"0%{{opacity:0}}{pct(max(lo - 3, 0))}{{opacity:0}}{pct(lo)}{{opacity:1}}"
            f"{pct(hi)}{{opacity:1}}{pct(min(hi + 5, 100))}{{opacity:0}}100%{{opacity:0}}"
            "}"
        )
        halo_css.append(f".h{i} {{ animation: n{i} {cycle:g}s linear infinite }}")
        node_markup.append(
            f'  <g class="node">\n'
            f'    <rect x="{x:.1f}" y="{cy - box_h / 2:g}" width="{box_w:g}" height="{box_h:g}" rx="{box_h / 2:g}"/>\n'
            f'    <rect class="halo h{i}" x="{x:.1f}" y="{cy - box_h / 2:g}" width="{box_w:g}" height="{box_h:g}" rx="{box_h / 2:g}" opacity="0"/>\n'
            f'    <text class="label" x="{cx:g}" y="{cy + 4.5:g}">{label}</text>\n'
            f'    <text class="verb" x="{cx:g}" y="{cy + 32:g}">{verb}</text>\n'
            f"  </g>"
        )

    pulse_markup = []
    for i, path in enumerate(edges):
        start, end = segments[i]
        lo, hi = start / cycle * 100, end / cycle * 100
        keyframes.append(
            f"@keyframes p{i}{{"
            f"0%{{opacity:0}}{pct(max(lo - 0.5, 0))}{{opacity:0}}"
            f"{pct(min(lo + 2, hi))}{{opacity:1}}{pct(max(hi - 2, lo))}{{opacity:1}}"
            f"{pct(hi)}{{opacity:0}}100%{{opacity:0}}"
            "}"
        )
        halo_css.append(f".p{i} {{ animation: p{i} {cycle:g}s linear infinite }}")
        pulse_markup.append(
            f'  <circle class="pulse p{i}" r="3.2" opacity="0">\n'
            f'    <animateMotion dur="{cycle:g}s" repeatCount="indefinite" calcMode="linear"\n'
            f'      keyTimes="0;{start / cycle:.4f};{end / cycle:.4f};1" keyPoints="0;0;1;1"\n'
            f'      path="{path}"/>\n'
            f"  </circle>"
        )

    wires = "\n".join(f'  <path class="wire" d="{p}"/>' for p in edges)
    arrows = []
    for i in range(2):
        tip = nodes[i + 1][2] - box_w / 2 - 10
        arrows.append(
            f'  <path class="arrow" d="M {tip - 5:.1f} {cy - 3.4:g} L {tip:.1f} {cy} L {tip - 5:.1f} {cy + 3.4:g}"/>'
        )

    # Currently: two rotating focus lines.
    focus = [
        "Condura · local conductor",
        "poly-maker · regime machine",
    ]
    focus_cycle = 8.0
    focus_slot = focus_cycle / len(focus)
    focus_hold = (focus_slot - 0.5) / focus_cycle * 100
    keyframes.append(
        "@keyframes focus{"
        f"0%{{opacity:0}}2%{{opacity:1}}{pct(focus_hold)}{{opacity:1}}"
        f"{pct(focus_slot / focus_cycle * 100)}{{opacity:0}}100%{{opacity:0}}"
        "}"
    )
    focus_lines = []
    for i, line in enumerate(focus):
        focus_lines.append(
            f'  <text class="focus" x="258" y="212" style="animation-delay:{i * focus_slot:g}s">{line}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Models coordinate, markets price uncertainty, contracts become legible">
  <title>models · markets · contracts</title>
  <defs>
    <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="wash">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="seam" gradientUnits="userSpaceOnUse" x1="220" y1="0" x2="680" y2="0">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{theme['accent']}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    .node rect {{ fill: none; stroke: {theme['faint']}; stroke-width: 1.2; }}
    .halo {{ fill: none; stroke: {theme['accent']}; stroke-width: 1.4; }}
    .label {{ font-family: {MONO}; font-size: 13px; fill: {theme['name']}; text-anchor: middle; }}
    .verb {{ font-family: {MONO}; font-size: 11px; fill: {theme['muted']}; text-anchor: middle; }}
    .wire {{ fill: none; stroke: {theme['faint']}; stroke-width: 1.2; stroke-dasharray: 3 5; stroke-linecap: round; }}
    .arrow {{ fill: none; stroke: {theme['faint']}; stroke-width: 1.2; stroke-linecap: round; stroke-linejoin: round; }}
    .pulse {{ fill: {theme['accent']}; filter: url(#glow); }}
    .lede {{ font-family: {SANS}; font-size: 15px; fill: {theme['name']}; text-anchor: middle; }}
    .meta {{ font-family: {MONO}; font-size: 12px; fill: {theme['muted']}; text-anchor: middle; }}
    .now {{ font-family: {MONO}; font-size: 11px; letter-spacing: 1.4px; fill: {theme['muted']}; }}
    .focus {{ font-family: {MONO}; font-size: 12px; fill: {theme['muted']}; opacity: 0; animation: focus {focus_cycle:g}s linear infinite; }}
    .live {{ fill: {theme['live']}; animation: beat 2.2s ease-in-out infinite; }}
    .wash {{ animation: drift 30s ease-in-out infinite alternate; }}
    .wash.r {{ animation-duration: 38s; animation-direction: alternate-reverse; }}
    {chr(10).join('    ' + k for k in keyframes)}
    {chr(10).join('    ' + c for c in halo_css)}
    @keyframes beat {{ 0%, 100% {{ opacity: 1 }} 50% {{ opacity: 0.35 }} }}
    @keyframes drift {{ from {{ transform: translateX(-12px) }} to {{ transform: translateX(12px) }} }}
    @media (prefers-reduced-motion: reduce) {{
      .pulse, .halo, .focus, .live, .wash {{ animation: none }}
      .pulse {{ opacity: 0 }}
      .h0 {{ opacity: 1 }}
      .focus {{ opacity: 0 }}
      .focus:first-of-type {{ opacity: 1 }}
    }}
  </style>

  <ellipse class="wash" cx="200" cy="70" rx="160" ry="42" fill="url(#wash)"/>
  <ellipse class="wash r" cx="720" cy="90" rx="150" ry="40" fill="url(#wash)"/>

{wires}
{chr(10).join(arrows)}
{chr(10).join(node_markup)}
{chr(10).join(pulse_markup)}

  <text class="lede" x="450" y="148">I build software where these three have to stay honest.</text>
  <text class="meta" x="450" y="172">TypeScript · Python · Go — usually deployed · usually measured</text>

  <line x1="220" y1="188" x2="680" y2="188" stroke="url(#seam)" stroke-width="1" stroke-linecap="round"/>

  <circle class="live" cx="150" cy="208" r="3.2"/>
  <circle cx="150" cy="208" r="3.2" fill="none" stroke="{theme['live']}" stroke-width="1">
    <animate attributeName="r" values="3.2;9" dur="2.2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.45;0" dur="2.2s" repeatCount="indefinite"/>
  </circle>
  <text class="now" x="164" y="212">CURRENTLY</text>
  <text class="now" x="244" y="212" fill="{theme['faint']}">·</text>
{chr(10).join(focus_lines)}
</svg>
"""


def main() -> None:
    for theme_name, palette in THEMES.items():
        (OUT / f"header-{theme_name}.svg").write_text(header(palette), encoding="utf-8")
        (OUT / f"intro-{theme_name}.svg").write_text(intro(palette), encoding="utf-8")
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
