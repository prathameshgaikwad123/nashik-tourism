#!/usr/bin/env python3
"""
WCAG contrast of the colour pairings the design actually uses (computed, not estimated).

    python3 tools/qa/contrast.py        # exit 1 if any text pairing is below 4.5:1 or any UI pairing below 3:1

Tokens are read from the :root block of nashiktourism/style.css so the check cannot
drift from the stylesheet. Semi-transparent colours are composited over the surface
they sit on before the ratio is taken.
"""
import os
import re
import sys

CSS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nashiktourism", "style.css")


def tokens():
    css = open(CSS, encoding="utf-8").read()
    root = css[css.index(":root"):css.index("}", css.index(":root"))]
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"--([\w-]+):\s*([^;]+?);", root)}


def parse(c, T, under=None):
    c = c.strip()
    if c.startswith("var("):
        return parse(T[c[6:-1]], T, under)
    if c.startswith("#"):
        c = c[1:]
        if len(c) == 3:
            c = "".join(x * 2 for x in c)
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    m = re.match(r"rgba?\(([^)]+)\)", c)
    if m:
        parts = [float(x) for x in m.group(1).split(",")]
        r, g, b = parts[:3]
        a = parts[3] if len(parts) > 3 else 1
        if a < 1 and under is not None:
            ur, ug, ub = under
            return (r * a + ur * (1 - a), g * a + ug * (1 - a), b * a + ub * (1 - a))
        return (r, g, b)
    raise ValueError(c)


def lum(rgb):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main():
    T = tokens()
    P = lambda c, under=None: parse(c, T, under)  # noqa: E731
    light = ["var(--cream)", "var(--light)", "var(--stone)", "var(--white)"]
    text = [("ink", "var(--ink)"), ("body", "var(--body-clr)"), ("muted", "var(--muted)"), ("muted-strong", "var(--muted-strong)"),
            ("stone-ink", "var(--stone-ink)"), ("primary", "var(--primary)"), ("saffron-deep", "var(--saffron-deep)"),
            ("gold-deep", "var(--gold-deep)"), ("vine", "var(--vine)")]
    rows = []  # (label, fg, bg, minimum)
    for tn, tv in text:
        for bg in light:
            rows.append(("%s on %s" % (tn, bg[6:-1]), tv, bg, 4.5))
    badges = [("verified", "#0B5B3D", "#E3F3EC"), ("reported", "#6E4F12", "#FFF1D3"), ("not_verified", "var(--stone-ink)", "var(--stone)"),
              ("disputed", "#8F3B0E", "#FCE6D8"), ("cancelled", "#8A1C1C", "#F9DEDE"), ("status-notice body", "var(--body-clr)", "#FFF9EC"),
              ("status-notice title", "var(--gold-deep)", "#FFF9EC")]
    for n, fg, bg in badges:
        rows.append(("badge: " + n, fg, bg, 4.5))
    dark = [("on-dark", "var(--on-dark)", "var(--dark)"), ("on-dark-muted", "var(--on-dark-muted)", "var(--dark)"),
            ("on-dark-soft", "var(--on-dark-soft)", "var(--dark)"), ("accent-warm", "var(--accent-warm)", "var(--dark)"),
            ("white on primary-dark", "#FFFFFF", "var(--primary-dark)"), ("on-dark-muted on primary-dark", "var(--on-dark-muted)", "var(--primary-dark)"),
            ("accent-warm on primary-dark", "var(--accent-warm)", "var(--primary-dark)"),
            ("white on saffron-deep (buttons)", "#FFFFFF", "var(--saffron-deep)"), ("white on primary (tags, buttons)", "#FFFFFF", "var(--primary)"),
            ("white on saffron-deep-h (hover)", "#FFFFFF", "var(--saffron-deep-h)")]
    for n, fg, bg in dark:
        rows.append((n, fg, bg, 4.5))
    ui = [("focus ring (indigo) on cream", "var(--focus-ring)", "var(--cream)"), ("focus ring (gold) on dark", "var(--focus)", "var(--dark)"),
          ("search field border (primary) on white", "var(--primary)", "var(--white)"),
          ("pressed chip fill (primary) vs unpressed chip (white)", "var(--primary)", "var(--white)")]
    for n, fg, bg in ui:
        rows.append((n, fg, bg, 3.0))

    bad = 0
    for label, fg, bg, need in rows:
        b = P(bg)
        f = P(fg, b)
        r = ratio(f, b)
        ok = r >= need
        bad += not ok
        print("%s %6.2f:1  need %.1f  %s" % ("ok  " if ok else "FAIL", r, need, label))
    print("\n%d pairing(s) below threshold" % bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
