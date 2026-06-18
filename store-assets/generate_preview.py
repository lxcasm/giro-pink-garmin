# -*- coding: utf-8 -*-
"""Apercu fidele du champ Giro Pink (Edge 1040, 282x470) - style Carbone Rosa.
Reproduit la mise en page du fichier source GiroPinkApp.mc."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 282, 470
C_BG = (0x3A, 0x0E, 0x26)
C_BAR = (0x29, 0x09, 0x1A)
C_ACCENT = (0xFF, 0x2E, 0x9C)
C_TOPTXT = (0xFF, 0x8A, 0xC6)
C_VALUE = (0xFF, 0xFF, 0xFF)
C_UNIT = (0xB8, 0x7A, 0x9C)
C_SEP = (0x5A, 0x24, 0x44)
C_SEG_OFF = (0x4A, 0x2A, 0x3E)

ZONE = {1: (0x9A, 0xA0, 0xA6), 2: (0x2D, 0x9C, 0xDB), 3: (0x39, 0xB5, 0x4A),
        4: (0xF5, 0xE6, 0x17), 5: (0xFC, 0x67, 0x19), 6: (0xE3, 0x19, 0x37)}

# Exemple : 185 W, FTP 200 -> 92% -> Z4 (jaune)
PW = "185"
PW_ZONE = 4

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "apercu-edge1040.png")


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


def ct(d, cx, cy, s, fn, fill):
    b = d.textbbox((0, 0), s, font=fn)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), s, font=fn, fill=fill)


def lt(d, x, cy, s, fn, fill):
    b = d.textbbox((0, 0), s, font=fn)
    d.text((x, cy - (b[3] - b[1]) / 2 - b[1]), s, font=fn, fill=fill)


def rt(d, x, cy, s, fn, fill):
    b = d.textbbox((0, 0), s, font=fn)
    d.text((x - (b[2] - b[0]) - b[0], cy - (b[3] - b[1]) / 2 - b[1]), s, font=fn, fill=fill)


def metric(d, cx, top, rowH, label, value, unit, vsz):
    ct(d, cx, top + rowH * 0.24, label, f(11, False), C_ACCENT)
    ct(d, cx, top + rowH * 0.57, value, f(vsz), C_VALUE)
    if unit:
        ct(d, cx, top + rowH * 0.85, unit, f(11, False), C_UNIT)


def power(d, cx, top, rowH):
    ct(d, cx, top + rowH * 0.22, "PUISSANCE W", f(11, False), C_ACCENT)
    ct(d, cx, top + rowH * 0.53, PW, f(33), ZONE[PW_ZONE])
    barW = W * 0.40
    seg = barW / 6
    bx = cx - (seg * 6) / 2
    by = top + rowH * 0.84
    bh = max(5, rowH * 0.11)
    for z in range(1, 7):
        col = ZONE[z] if z <= PW_ZONE else C_SEG_OFF
        d.rectangle([bx + (z - 1) * seg, by, bx + (z - 1) * seg + seg - 2, by + bh], fill=col)


def main():
    img = Image.new("RGB", (W, H), C_BG)
    d = ImageDraw.Draw(img)

    barH = int(H * 0.064)
    d.rectangle([0, 0, W, barH], fill=C_BAR)
    cy = barH / 2
    lt(d, int(W * 0.05), cy, "6:34", f(14), C_TOPTXT)
    ct(d, W / 2, cy, "GIRO", f(14), C_TOPTXT)
    rt(d, int(W * 0.95), cy, "24\u00b0", f(14), C_TOPTXT)
    d.rectangle([0, barH - 2, W, barH], fill=C_ACCENT)

    heroH = int(H * 0.29)
    cxh = W / 2
    ct(d, cxh, barH + heroH * 0.16, "VITESSE", f(13, False), C_ACCENT)
    ct(d, cxh, barH + heroH * 0.52, "42.5", f(72), C_VALUE)
    ct(d, cxh, barH + heroH * 0.86, "km/h", f(14), C_UNIT)
    m = int(W * 0.085)
    d.rectangle([m, barH + heroH - 2, W - m, barH + heroH + 1], fill=C_ACCENT)

    gridY = barH + heroH
    rowH = (H - gridY) / 4
    midX = W / 2
    pad = W * 0.02
    d.rectangle([midX - 1, gridY + pad, midX + 1, gridY + rowH * 4 - pad], fill=C_SEP)
    for i in range(1, 4):
        d.rectangle([pad, gridY + rowH * i - 1, W - pad, gridY + rowH * i + 1], fill=C_SEP)

    cxL, cxR = W * 0.25, W * 0.75
    power(d, cxL, gridY, rowH)
    metric(d, cxR, gridY, rowH, "COEUR", "154", "bpm", 33)
    metric(d, cxL, gridY + rowH, rowH, "CADENCE", "92", "rpm", 27)
    metric(d, cxR, gridY + rowH, rowH, "PENTE", "6.2", "%", 27)
    metric(d, cxL, gridY + rowH * 2, rowH, "DISTANCE", "34.18", "km", 27)
    metric(d, cxR, gridY + rowH * 2, rowH, "ALTITUDE", "1240", "m", 27)
    metric(d, cxL, gridY + rowH * 3, rowH, "TEMPS ROULANT", "1:23:45", "", 25)
    metric(d, cxR, gridY + rowH * 3, rowH, "DENIVELE +", "612", "m", 27)

    img.save(OUT)
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
