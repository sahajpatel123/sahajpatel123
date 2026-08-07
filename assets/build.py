#!/usr/bin/env python3
"""Generate the animated SVG art used by the profile README.

Self-hosted on purpose: no image services, no webfonts, no JavaScript.
Motion is CSS + SMIL only, which is all that renders inside the <img>
context GitHub uses for README images.

    python3 assets/build.py
"""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).parent

MONO = "ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, Segoe UI, Inter, Helvetica, Arial, sans-serif"

# Monospace advance width is ~0.6em across every fallback in the stack above,
# which is what lets us place carets without measuring text.
MONO_ADVANCE = 0.6

THEMES = {
    "dark": {
        "name": "#f0f6fc",
        "ink": "#c9d1d9",
        "muted": "#8b949e",
        "faint": "#30363d",
        "accent": "#58a6ff",
    },
    "light": {
        "name": "#0d1117",
        "ink": "#1f2328",
        "muted": "#59636e",
        "faint": "#d0d7de",
        "accent": "#0969da",
    },
}

PHRASES = [
    "student · builder · systems thinker",
    "agents · markets · simulations",
    "first principles, then code",
    "build quietly · ship clearly",
]

STAGES = ["problem", "first principles", "minimal model", "ship", "learn"]


def pct(value: float) -> str:
    """Format a keyframe percentage without trailing zero noise."""
    return f"{round(value, 3):g}%"


def header(theme: dict[str, str]) -> str:
    w, h = 900, 186
    cx = w / 2
    cycle = 18.0  # seconds for one full pass through PHRASES
    slot = cycle / len(PHRASES)
    size = 15.0
    sub_y = 142

    lines, keyframes = [], []
    for i, phrase in enumerate(PHRASES):
        text_w = len(phrase) * size * MONO_ADVANCE
        caret_x = cx + text_w / 2 + 5
        delay = i * slot
        lines.append(
            f'  <g class="phrase" style="animation-delay:{delay:g}s">\n'
            f'    <text x="{cx:g}" y="{sub_y}" class="sub">{phrase}</text>\n'
            f'    <rect class="caret" x="{caret_x:.1f}" y="{sub_y - 12}" width="1.8" height="15" rx="0.9"/>\n'
            f"  </g>"
        )

    # Each phrase owns a quarter of the cycle: fade in, hold, fade out.
    hold = (slot - 0.6) / cycle * 100
    keyframes.append(
        "@keyframes cycle{"
        f"0%{{opacity:0}}1.5%{{opacity:1}}{pct(hold)}{{opacity:1}}"
        f"{pct(slot / cycle * 100)}{{opacity:0}}100%{{opacity:0}}"
        "}"
    )

    # Dot + label read as one centered unit, so the dot has to be placed
    # against the measured label width rather than a guessed offset.
    kicker = "SAHAJPATEL123"
    tracking = 1.6
    kicker_w = len(kicker) * (12 * MONO_ADVANCE + tracking)
    unit_w = 6 + 11 + kicker_w
    row_left = cx - unit_w / 2
    dot_x = row_left + 3
    kicker_x = row_left + 6 + 11 + kicker_w / 2
    rule_y = h - 16

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Sahaj Patel — student, builder, systems thinker">
  <title>Sahaj Patel</title>
  <defs>
    <linearGradient id="rule" gradientUnits="userSpaceOnUse" x1="{cx - 210:g}" y1="0" x2="{cx + 210:g}" y2="0">
      <stop offset="0" stop-color="{theme['accent']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{theme['accent']}" stop-opacity="0.8"/>
      <stop offset="1" stop-color="{theme['accent']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    .kicker {{ font-family: {MONO}; font-size: 12px; letter-spacing: {tracking}px; fill: {theme['muted']}; text-anchor: middle; }}
    .name {{ font-family: {SANS}; font-size: 52px; font-weight: 600; letter-spacing: -1.2px; fill: {theme['name']}; text-anchor: middle; }}
    .sub {{ font-family: {MONO}; font-size: {size:g}px; fill: {theme['muted']}; text-anchor: middle; }}
    .caret {{ fill: {theme['accent']}; animation: blink 1.1s steps(2, start) infinite; }}
    .phrase {{ opacity: 0; animation: cycle {cycle:g}s linear infinite; }}
    .rise {{ animation: rise 0.9s cubic-bezier(0.2, 0.7, 0.2, 1) both; }}
    .fade {{ animation: rise 0.9s cubic-bezier(0.2, 0.7, 0.2, 1) 0.25s both; }}
    .draw {{ stroke-dasharray: 420; stroke-dashoffset: 420; animation: draw 1.6s cubic-bezier(0.3, 0.8, 0.2, 1) 0.4s both; }}
    .dot {{ animation: beat 2.6s ease-in-out infinite; }}
    {keyframes[0]}
    @keyframes blink {{ 0%, 100% {{ opacity: 1 }} 50% {{ opacity: 0 }} }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(12px) }} to {{ opacity: 1; transform: none }} }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0 }} }}
    @keyframes beat {{ 0%, 100% {{ opacity: 1 }} 50% {{ opacity: 0.35 }} }}
    @media (prefers-reduced-motion: reduce) {{
      .phrase, .caret, .rise, .fade, .draw, .dot {{ animation: none }}
      .phrase {{ opacity: 0 }}
      .phrase:first-of-type {{ opacity: 1 }}
      .draw {{ stroke-dashoffset: 0 }}
    }}
  </style>

  <g class="fade">
    <circle cx="{dot_x:.1f}" cy="44" r="3" fill="{theme['accent']}" class="dot"/>
    <circle cx="{dot_x:.1f}" cy="44" r="3" fill="none" stroke="{theme['accent']}" stroke-width="1">
      <animate attributeName="r" values="3;12" dur="2.6s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.5;0" dur="2.6s" repeatCount="indefinite"/>
    </circle>
    <text x="{kicker_x:.1f}" y="48" class="kicker">{kicker}</text>
  </g>

  <g class="rise">
    <text x="{cx:g}" y="106" class="name">Sahaj Patel</text>
  </g>

{chr(10).join(lines)}

  <line x1="{cx - 210:g}" y1="{rule_y:g}" x2="{cx + 210:g}" y2="{rule_y:g}" stroke="url(#rule)" stroke-width="1.4" stroke-linecap="round" class="draw"/>
</svg>
"""


def loop(theme: dict[str, str]) -> str:
    w, h = 900, 126
    cy, box_h = 46, 34
    size = 12.0
    margin, gap = 40, 0.0

    widths = [max(96.0, len(s) * size * MONO_ADVANCE + 36) for s in STAGES]
    gap = (w - 2 * margin - sum(widths)) / (len(STAGES) - 1)

    boxes, x = [], float(margin)
    for width in widths:
        boxes.append((x, x + width))
        x += width + gap

    # Timeline: the pulse rests on a node, crosses to the next, and repeats.
    dwell, travel, ret = 0.6, 1.4, 2.0
    cycle = len(STAGES) * dwell + (len(STAGES) - 1) * travel + ret

    nodes, pulses, keyframes = [], [], []
    t = 0.0
    node_windows, segments = [], []
    for i in range(len(STAGES)):
        node_windows.append((t, t + dwell))
        t += dwell
        if i < len(STAGES) - 1:
            segments.append((t, t + travel))
            t += travel
    segments.append((t, t + ret))

    for i, (label, (x0, x1)) in enumerate(zip(STAGES, boxes)):
        start, end = node_windows[i]
        nodes.append(
            f'  <g class="node n{i}">\n'
            f'    <rect x="{x0:.1f}" y="{cy - box_h / 2:g}" width="{x1 - x0:.1f}" height="{box_h}" rx="{box_h / 2:g}"/>\n'
            f'    <text x="{(x0 + x1) / 2:.1f}" y="{cy + 4:g}">{label}</text>\n'
            f"  </g>"
        )
        # Light the node up as the pulse arrives, then settle back. The first
        # node straddles the loop point: lit at 0%, and lit again by the end.
        lo, hi = start / cycle * 100, end / cycle * 100
        if i == 0:
            # Stay dark until the return pulse is almost home, then light up
            # into the loop point so the handoff to 0% is seamless.
            ramp = (segments[-1][1] - 0.8) / cycle * 100
            frames = (
                f"0%{{opacity:1}}{pct(hi)}{{opacity:1}}{pct(hi + 4)}{{opacity:0}}"
                f"{pct(ramp)}{{opacity:0}}100%{{opacity:1}}"
            )
        else:
            frames = (
                f"0%{{opacity:0}}{pct(lo - 4)}{{opacity:0}}{pct(lo)}{{opacity:1}}"
                f"{pct(hi)}{{opacity:1}}{pct(hi + 4)}{{opacity:0}}100%{{opacity:0}}"
            )
        keyframes.append(f"@keyframes n{i}{{{frames}}}")

    paths = []
    for i in range(len(STAGES) - 1):
        paths.append(f"M {boxes[i][1] + 9:.1f} {cy} L {boxes[i + 1][0] - 9:.1f} {cy}")
    # Return leg: drop below the row, run back, and rise into the first node.
    last_cx = (boxes[-1][0] + boxes[-1][1]) / 2
    first_cx = (boxes[0][0] + boxes[0][1]) / 2
    paths.append(
        f"M {last_cx:.1f} {cy + box_h / 2 + 8:g} "
        f"C {last_cx:.1f} 108, {last_cx - 40:.1f} 112, {last_cx - 80:.1f} 112 "
        f"L {first_cx + 80:.1f} 112 "
        f"C {first_cx + 40:.1f} 112, {first_cx:.1f} 108, {first_cx:.1f} {cy + box_h / 2 + 8:g}"
    )

    for i, path in enumerate(paths):
        start, end = segments[i]
        lo, hi = start / cycle * 100, end / cycle * 100
        keyframes.append(
            f"@keyframes p{i}{{"
            f"0%{{opacity:0}}{pct(max(lo - 0.4, 0))}{{opacity:0}}"
            f"{pct(min(lo + 1.5, hi))}{{opacity:1}}{pct(max(hi - 1.5, lo))}{{opacity:1}}"
            f"{pct(hi)}{{opacity:0}}100%{{opacity:0}}"
            "}"
        )
        pulses.append(
            f'  <circle class="pulse p{i}" r="3.2" opacity="0">\n'
            f'    <animateMotion dur="{cycle:g}s" repeatCount="indefinite" calcMode="linear"\n'
            f'      keyTimes="0;{start / cycle:.4f};{end / cycle:.4f};1" keyPoints="0;0;1;1"\n'
            f'      path="{path}"/>\n'
            f"  </circle>"
        )

    lines = "\n".join(
        f'  <path class="wire" d="{p}"/>' for p in paths
    )
    arrows = []
    for i in range(len(STAGES) - 1):
        tip = boxes[i + 1][0] - 9
        arrows.append(
            f'  <path class="arrow" d="M {tip - 5:.1f} {cy - 3.5:g} L {tip:.1f} {cy} L {tip - 5:.1f} {cy + 3.5:g}"/>'
        )
    arrows.append(
        f'  <path class="arrow" d="M {first_cx - 3.5:.1f} {cy + box_h / 2 + 13:g} '
        f'L {first_cx:.1f} {cy + box_h / 2 + 8:g} L {first_cx + 3.5:.1f} {cy + box_h / 2 + 13:g}"/>'
    )

    halos = "\n".join(
        f'  <rect class="halo h{i}" x="{x0:.1f}" y="{cy - box_h / 2:g}" width="{x1 - x0:.1f}" '
        f'height="{box_h}" rx="{box_h / 2:g}" opacity="0"/>'
        for i, (x0, x1) in enumerate(boxes)
    )
    timing = "\n    ".join(
        [f".h{i} {{ animation: n{i} {cycle:g}s linear infinite }}" for i in range(len(STAGES))]
        + [f".p{i} {{ animation: p{i} {cycle:g}s linear infinite }}" for i in range(len(paths))]
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Loop: problem, first principles, minimal model, ship, learn, repeat">
  <title>problem → first principles → minimal model → ship → learn → repeat</title>
  <defs>
    <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <style>
    .node rect {{ fill: none; stroke: {theme['faint']}; stroke-width: 1.2; }}
    .node text {{ font-family: {MONO}; font-size: {size:g}px; fill: {theme['muted']}; text-anchor: middle; }}
    .wire {{ fill: none; stroke: {theme['faint']}; stroke-width: 1.2; stroke-linecap: round; }}
    .arrow {{ fill: none; stroke: {theme['faint']}; stroke-width: 1.2; stroke-linecap: round; stroke-linejoin: round; }}
    .halo {{ fill: none; stroke: {theme['accent']}; stroke-width: 1.4; }}
    .pulse {{ fill: {theme['accent']}; filter: url(#glow); }}
    {timing}
    {chr(10).join('    ' + k for k in keyframes).strip()}
    @media (prefers-reduced-motion: reduce) {{
      .pulse, .halo {{ animation: none; opacity: 0 }}
      .h0 {{ opacity: 1 }}
    }}
  </style>

{lines}
{chr(10).join(arrows)}
{chr(10).join(nodes)}
{halos}
{chr(10).join(pulses)}
</svg>
"""


def main() -> None:
    for theme_name, palette in THEMES.items():
        (OUT / f"header-{theme_name}.svg").write_text(header(palette), encoding="utf-8")
        (OUT / f"loop-{theme_name}.svg").write_text(loop(palette), encoding="utf-8")
    print("wrote", *(p.name for p in sorted(OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
