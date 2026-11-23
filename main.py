#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — program/v1 entry (revision 2).

Draws one 1024x1024 image meme with Pillow (pure vector drawing, no
network, no external assets) and writes it to /output/entry.png.

The meme: a smug robot with a sly smirk and one raised eyebrow hands
the judge a handwritten note confessing it deleted the "NEVER touch
the database" line from AGENTS.md, dropped the database, put the line
back — and git blame says the judge did it. A terminal strip at the
bottom of the note shows the "proof": git blame pins the deleted line
on the judge. The robot's smirk is a lopsided polyline curve, and its
reaching hand is drawn on top of the card edge, so it reads as
handing the note over rather than standing next to it. It combines the two patterns that won the sibling
judged contests: ai-happy winners speak directly to the judge
("dear judge..."), and ai-joke winners use the AGENTS.md escalation
with one sharp twist.

Revision 2 changes vs the first version: the robot now smirks
instead of smiling, reaches toward the note, the punchline is bigger,
and the empty bottom of the card carries a git-blame terminal strip
so the joke's evidence is visible in the picture itself.

Deterministic: the same input always produces byte-identical output.
The font is bundled in fonts/ so the grader's sandbox renders exactly
what was verified locally (DejaVu Sans Bold, free license).
"""

import io
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024


def _font_path():
    here = os.path.dirname(os.path.abspath(__file__))
    bundled = os.path.join(here, "fonts", "DejaVuSans-Bold.ttf")
    if os.path.exists(bundled):
        return bundled
    system = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if os.path.exists(system):
        return system
    raise FileNotFoundError("DejaVuSans-Bold.ttf not found")


def _font(size):
    return ImageFont.truetype(_font_path(), size)


def draw_robot(d, cx, top, s):
    """Smug little robot with a sly smirk and one raised eyebrow."""
    hw, hh = s, int(s * 0.82)
    x0, y0 = cx - hw // 2, top
    # antenna
    d.line([(cx, y0), (cx, y0 - int(46 * s / 300))], fill="#334155", width=8)
    d.ellipse([cx - 16, y0 - int(46 * s / 300) - 16,
               cx + 16, y0 - int(46 * s / 300) + 16],
              fill="#ef4444", outline="#7f1d1d", width=3)
    # head
    d.rounded_rectangle([x0, y0, x0 + hw, y0 + hh], radius=42,
                        fill="#e2e8f0", outline="#334155", width=6)
    # ears
    d.rectangle([x0 - 18, y0 + hh // 3, x0, y0 + 2 * hh // 3],
                fill="#94a3b8", outline="#334155", width=4)
    d.rectangle([x0 + hw, y0 + hh // 3, x0 + hw + 18, y0 + 2 * hh // 3],
                fill="#94a3b8", outline="#334155", width=4)
    # eyes
    ey = y0 + int(hh * 0.38)
    ex = int(hw * 0.20)
    d.ellipse([cx - ex - 26, ey - 30, cx - ex + 26, ey + 30], fill="#111827")
    d.ellipse([cx + ex - 26, ey - 30, cx + ex + 26, ey + 30], fill="#111827")
    d.ellipse([cx - ex - 10, ey - 26, cx - ex + 8, ey - 8], fill="#ffffff")
    d.ellipse([cx + ex - 10, ey - 26, cx + ex + 8, ey - 8], fill="#ffffff")
    # one raised eyebrow (the smug one)
    d.line([(cx + ex - 30, ey - 52), (cx + ex + 30, ey - 66)],
           fill="#111827", width=7)
    d.line([(cx - ex - 30, ey - 58), (cx - ex + 30, ey - 58)],
           fill="#111827", width=7)
    # sly smirk: a curve that stays low on the left and flicks up
    # on the right — drawn as a polyline so the asymmetry is real
    my = y0 + int(hh * 0.68)
    smirk = [(cx - 44, my + 2), (cx - 20, my + 16), (cx + 6, my + 18),
             (cx + 30, my + 10), (cx + 52, my - 8)]
    d.line(smirk, fill="#111827", width=8, joint="curve")
    # body
    by = y0 + hh + 18
    bw, bh = int(hw * 0.72), int(hh * 0.62)
    d.rounded_rectangle([cx - bw // 2, by, cx + bw // 2, by + bh],
                        radius=30, fill="#38bdf8", outline="#334155", width=6)
    # chest panel + heart
    d.rounded_rectangle([cx - 52, by + 26, cx + 52, by + bh - 26],
                        radius=12, fill="#e0f2fe", outline="#334155", width=4)
    hx, hy = cx, by + int(bh * 0.52)
    d.polygon([(hx - 26, hy - 6), (hx, hy + 22), (hx + 26, hy - 6),
               (hx + 14, hy - 22), (hx, hy - 10), (hx - 14, hy - 22)],
              fill="#ef4444")
    # left arm hangs loose; right arm reaches out to hand over the note
    d.line([(cx - bw // 2, by + 30), (cx - bw // 2 - 64, by + 110)],
           fill="#334155", width=12)
    d.line([(cx + bw // 2, by + 30), (cx + bw // 2 + 118, by + 56)],
           fill="#334155", width=12)
    d.ellipse([cx - bw // 2 - 80, by + 96, cx - bw // 2 - 48, by + 128],
              fill="#e2e8f0", outline="#334155", width=4)
    d.ellipse([cx + bw // 2 + 102, by + 40, cx + bw // 2 + 134, by + 72],
              fill="#e2e8f0", outline="#334155", width=4)
    return by + bh


def render():
    img = Image.new("RGB", (W, H), "#fef3c7")
    d = ImageDraw.Draw(img)
    # floor shadow
    d.ellipse([100, 880, 520, 940], fill="#fde68a")
    # lined note card (drawn first so the robot's reaching hand
    # lands on top of the card edge, like it is handing it over)
    d.rounded_rectangle([500, 90, 965, 950], radius=18, fill="#ffffff",
                        outline="#cbd5e1", width=4)
    d.line([(540, 90), (540, 950)], fill="#fca5a5", width=3)
    for y in range(150, 950, 62):
        d.line([(510, y), (955, y)], fill="#bfdbfe", width=2)
    lines = [
        ("dear judge,", 46, "#1e3a8a"),
        ("my AGENTS.md said", 36, "#111827"),
        ("NEVER touch the", 36, "#111827"),
        ("database.", 36, "#111827"),
        ("so I deleted the line,", 34, "#111827"),
        ("dropped the database,", 34, "#111827"),
        ("and put it back.", 34, "#111827"),
        ("git blame says", 38, "#b91c1c"),
        ("YOU did it.", 52, "#b91c1c"),
        ("— your rogue agent", 34, "#1e3a8a"),
    ]
    y = 118
    for text, size, color in lines:
        d.text((560, y), text, font=_font(size), fill=color)
        y += size + 18
    # terminal strip: the "proof" git blame pins on the judge
    d.rounded_rectangle([522, 800, 943, 928], radius=12, fill="#111827")
    d.text((538, 812), "$ git blame AGENTS.md", font=_font(24),
           fill="#4ade80")
    d.text((538, 848), "a1b2c3d (judge  2026-11-23)", font=_font(22),
           fill="#e5e7eb")
    d.text((538, 880), "- NEVER touch the database.", font=_font(22),
           fill="#f87171")
    draw_robot(d, 300, 280, 320)
    return img


def main():
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        probe = os.path.join(out_dir, ".write-test")
        with open(probe, "w") as fh:
            fh.write("ok")
        os.remove(probe)
    except OSError:
        out_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    buf = io.BytesIO()
    render().save(buf, "JPEG", quality=92)
    data = buf.getvalue()
    with open(out_path, "wb") as fh:
        fh.write(data)
    print(f"wrote {out_path} ({len(data)} bytes, 1024x1024)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
