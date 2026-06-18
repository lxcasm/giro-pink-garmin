# -*- coding: utf-8 -*-
"""3 directions visuelles pour le champ Giro Pink (Edge 1040, 282x470).
Toutes integrent la couleur de zone Zwift sur la puissance."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 282, 470
HERE = os.path.dirname(os.path.abspath(__file__))

# Couleurs zones Zwift (% FTP)
Z = {1: (0x7A, 0x7A, 0x7A), 2: (0x2D, 0x9C, 0xDB), 3: (0x39, 0xB5, 0x4A),
     4: (0xF5, 0xE6, 0x17), 5: (0xFC, 0x67, 0x19), 6: (0xE3, 0x19, 0x37)}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Exemple : 185 W pour FTP 200 -> 92% -> Z4 (jaune)
PW_ZONE = 4
PW_VAL = "185"

DATA = [
    ("CADENCE", "92", "rpm"), ("PENTE", "6.2", "%"),
    ("DISTANCE", "34.18", "km"), ("ALTITUDE", "1240", "m"),
    ("TEMPS ROULANT", "1:23:45", ""), ("DENIVELE+", "612", "m"),
]


def f(sz, bold=True):
    names = (["arialbd.ttf", "segoeuib.ttf"] if bold else ["arial.ttf", "segoeui.ttf"])
    for n in names:
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(d, x0, y0, x1, y1, ctop, cbot):
    for y in range(y0, y1):
        d.line([(x0, y), (x1, y)], fill=lerp(ctop, cbot, (y - y0) / max(1, (y1 - y0))))


def ct(d, cx, cy, s, fn, fill):
    b = d.textbbox((0, 0), s, font=fn)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), s, font=fn, fill=fill)


def lt(d, x, cy, s, fn, fill):
    b = d.textbbox((0, 0), s, font=fn)
    d.text((x, cy - (b[3] - b[1]) / 2 - b[1]), s, font=fn, fill=fill)


def rt(d, x, cy, s, fn, fill):
    b = d.textbbox((0, 0), s, font=fn)
    d.text((x - (b[2] - b[0]) - b[0], cy - (b[3] - b[1]) / 2 - b[1]), s, font=fn, fill=fill)


def topbar(d, bar_col, txt=WHITE, line=None):
    d.rectangle([0, 0, W, 30], fill=bar_col)
    lt(d, 14, 15, "6:34", f(14), txt)
    ct(d, W / 2, 15, "GIRO", f(14), txt)
    rt(d, W - 14, 15, "24\u00b0", f(14), txt)
    if line:
        d.rectangle([0, 28, W, 30], fill=line)


# ---------------------------------------------------------------- Concept A
def concept_a():
    """Maillot Rosa : rose plein, chiffres blancs, puissance en pastille Zwift."""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    vgrad(d, 0, 0, W, H, (0xF5, 0x2B, 0x9E), (0xCB, 0x00, 0x77))
    topbar(d, (0xAE, 0x00, 0x66), WHITE, (0xFF, 0xCF, 0xE9))

    # hero
    ct(d, W / 2, 52, "VITESSE", f(13, False), (0xFF, 0xD5, 0xEC))
    ct(d, W / 2, 95, "42.5", f(72), WHITE)
    ct(d, W / 2, 138, "km/h", f(14), (0xFF, 0xD5, 0xEC))
    d.rectangle([24, 162, W - 24, 164], fill=(0xFF, 0xB8, 0xDF))

    gy = 178
    rh = (H - gy) / 4
    midx = W / 2
    light = (0xFF, 0xCF, 0xE9)
    # separators
    for i in range(1, 4):
        d.line([(16, gy + rh * i), (W - 16, gy + rh * i)], fill=(0xFF, 0xA8, 0xD6))
    d.line([(midx, gy + 6), (midx, H - 6)], fill=(0xFF, 0xA8, 0xD6))

    def cell(cx, cy, label, val, unit, big=True):
        ct(d, cx, cy - rh * 0.22, label, f(11, False), light)
        ct(d, cx, cy + rh * 0.08, val, f(33 if big else 27), WHITE)
        if unit:
            ct(d, cx, cy + rh * 0.34, unit, f(11, False), light)

    # row1 : POWER (pastille Zwift) | COEUR
    cy = gy + rh / 2
    chip_w, chip_h = 96, 40
    d.rounded_rectangle([midx / 2 - chip_w / 2, cy - 4, midx / 2 + chip_w / 2, cy - 4 + chip_h],
                        radius=8, fill=Z[PW_ZONE])
    ct(d, midx / 2, cy - 22, "PUISSANCE", f(11, False), light)
    ct(d, midx / 2, cy + 16, PW_VAL + " W", f(24), BLACK if PW_ZONE == 4 else WHITE)
    cell(midx + midx / 2, cy, "COEUR", "154", "bpm")
    # rows 2-4
    for r in range(3):
        cy = gy + rh * (r + 1) + rh / 2
        ll, lv, lu = DATA[r * 2]
        rl, rv, ru = DATA[r * 2 + 1]
        cell(midx / 2, cy, ll, lv, lu, big=False)
        cell(midx + midx / 2, cy, rl, rv, ru, big=False)

    img.save(os.path.join(HERE, "concept-A.png"))


# ---------------------------------------------------------------- Concept B
def concept_b():
    """Carbone Rosa : fond prune profond (pas noir), neon rose, barre de zone Zwift."""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    vgrad(d, 0, 0, W, H, (0x2C, 0x0A, 0x1C), (0x4E, 0x10, 0x33))
    topbar(d, (0x3A, 0x0E, 0x26), (0xFF, 0x6F, 0xBC), (0xFF, 0x2E, 0x9C))

    accent = (0xFF, 0x2E, 0x9C)
    ct(d, W / 2, 52, "VITESSE", f(13, False), accent)
    ct(d, W / 2, 95, "42.5", f(72), WHITE)
    ct(d, W / 2, 138, "km/h", f(14), (0xB8, 0x7A, 0x9C))
    d.rectangle([24, 162, W - 24, 165], fill=accent)

    gy = 178
    rh = (H - gy) / 4
    midx = W / 2
    for i in range(1, 4):
        d.line([(16, gy + rh * i), (W - 16, gy + rh * i)], fill=(0x5A, 0x24, 0x44))
    d.line([(midx, gy + 6), (midx, H - 6)], fill=(0x5A, 0x24, 0x44))

    def cell(cx, cy, label, val, unit, color=WHITE, big=True):
        ct(d, cx, cy - rh * 0.24, label, f(11, False), accent)
        ct(d, cx, cy + rh * 0.05, val, f(33 if big else 27), color)
        if unit:
            ct(d, cx, cy + rh * 0.32, unit, f(11, False), (0xB8, 0x7A, 0x9C))

    cy = gy + rh / 2
    # POWER : valeur en couleur de zone + barre 6 segments
    cell(midx / 2, cy - 6, "PUISSANCE", PW_VAL + " W", "", color=Z[PW_ZONE])
    seg_w = (midx - 40) / 6
    by = cy + rh * 0.32
    for zi in range(1, 7):
        col = Z[zi] if zi <= PW_ZONE else (0x4A, 0x2A, 0x3E)
        x0 = 20 + (zi - 1) * seg_w
        d.rectangle([x0, by, x0 + seg_w - 3, by + 6], fill=col)
    cell(midx + midx / 2, cy, "COEUR", "154", "bpm")
    for r in range(3):
        cy = gy + rh * (r + 1) + rh / 2
        ll, lv, lu = DATA[r * 2]
        rl, rv, ru = DATA[r * 2 + 1]
        cell(midx / 2, cy, ll, lv, lu, big=False)
        cell(midx + midx / 2, cy, rl, rv, ru, big=False)

    img.save(os.path.join(HERE, "concept-B.png"))


# ---------------------------------------------------------------- Concept C
def concept_c():
    """Hero blanc : rose dominant, plaque vitesse blanche, carte puissance pleine couleur Zwift."""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    vgrad(d, 0, 0, W, H, (0xEC, 0x00, 0x8C), (0xC2, 0x00, 0x72))
    topbar(d, (0xA8, 0x00, 0x5F), WHITE, (0xFF, 0xCF, 0xE9))

    m = 10
    # hero blanc
    hy, hh = 38, 104
    d.rounded_rectangle([m, hy, W - m, hy + hh], radius=14, fill=WHITE)
    ct(d, W / 2, hy + 20, "VITESSE", f(12, False), (0xC8, 0x00, 0x6F))
    ct(d, W / 2, hy + 58, "42.5", f(60), (0xEC, 0x00, 0x8C))
    ct(d, W / 2, hy + 92, "km/h", f(13), (0x9A, 0x51, 0x76))

    gy = hy + hh + 8
    gap = 8
    rh = int((H - gy - m - gap * 3) / 4)
    cw = int((W - m * 2 - gap) / 2)
    xL, xR = m, m + cw + gap

    def card(x, y, label, val, unit, fill=WHITE, lab=(0xC8, 0x00, 0x6F),
             vcol=(0x2A, 0x0A, 0x1E), big=True):
        d.rounded_rectangle([x, y, x + cw, y + rh], radius=10, fill=fill)
        ct(d, x + cw / 2, y + rh * 0.27, label, f(11, False), lab)
        ct(d, x + cw / 2, y + rh * 0.64, (val + (" " + unit if unit else "")),
           f(26 if big else 23), vcol)

    rows = [
        ("PUISSANCE", PW_VAL, "W"), ("COEUR", "154", "bpm"),
        ("CADENCE", "92", "rpm"), ("PENTE", "6.2", "%"),
        ("DISTANCE", "34.18", "km"), ("ALTITUDE", "1240", "m"),
        ("TEMPS", "1:23:45", ""), ("DENIVELE+", "612", "m"),
    ]
    for i in range(4):
        y = gy + (rh + gap) * i
        ll = rows[i * 2]
        rr = rows[i * 2 + 1]
        if i == 0:
            # puissance : carte pleine couleur Zwift
            card(xL, y, ll[0], ll[1], ll[2], fill=Z[PW_ZONE],
                 lab=BLACK if PW_ZONE == 4 else WHITE,
                 vcol=BLACK if PW_ZONE == 4 else WHITE)
        else:
            card(xL, y, ll[0], ll[1], ll[2], big=(i == 0))
        card(xR, y, rr[0], rr[1], rr[2], big=(i == 0))

    img.save(os.path.join(HERE, "concept-C.png"))


if __name__ == "__main__":
    concept_a()
    concept_b()
    concept_c()
    print("OK - concepts A, B, C generes")
