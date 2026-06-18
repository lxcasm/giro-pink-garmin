# -*- coding: utf-8 -*-
"""Images du Connect IQ Store pour Giro Pink :
- captures d'ecran par zone (282x470)
- image principale 1440x720
- image de couverture 500x500
"""
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
WHITE = (255, 255, 255)

ZONE = {1: (0x9A, 0xA0, 0xA6), 2: (0x2D, 0x9C, 0xDB), 3: (0x39, 0xB5, 0x4A),
        4: (0xF5, 0xE6, 0x17), 5: (0xFC, 0x67, 0x19), 6: (0xE3, 0x19, 0x37)}

HERE = os.path.dirname(os.path.abspath(__file__))


def f(sz, bold=True):
    names = (["arialbd.ttf", "segoeuib.ttf"] if bold else ["arial.ttf", "segoeui.ttf"])
    for n in names:
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def ct(d, cx, cy, s, fn, fill):
    b = d.textbbox((0, 0), s, font=fn)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), s, font=fn, fill=fill)


def lt(d, x, cy, s, fn, fill):
    b = d.textbbox((0, 0), s, font=fn)
    d.text((x, cy - (b[3] - b[1]) / 2 - b[1]), s, font=fn, fill=fill)


def rt(d, x, cy, s, fn, fill):
    b = d.textbbox((0, 0), s, font=fn)
    d.text((x - (b[2] - b[0]) - b[0], cy - (b[3] - b[1]) / 2 - b[1]), s, font=fn, fill=fill)


def render_field(speed, power, zone, hr, cad, grade, dist, alt, tmr, asc, temp, clock):
    img = Image.new("RGB", (W, H), C_BG)
    d = ImageDraw.Draw(img)

    barH = int(H * 0.064)
    d.rectangle([0, 0, W, barH], fill=C_BAR)
    cy = barH / 2
    lt(d, int(W * 0.05), cy, clock, f(14), C_TOPTXT)
    ct(d, W / 2, cy, "GIRO", f(14), C_TOPTXT)
    rt(d, int(W * 0.95), cy, temp + "\u00b0", f(14), C_TOPTXT)
    d.rectangle([0, barH - 2, W, barH], fill=C_ACCENT)

    heroH = int(H * 0.29)
    ct(d, W / 2, barH + heroH * 0.16, "VITESSE", f(13, False), C_ACCENT)
    ct(d, W / 2, barH + heroH * 0.52, speed, f(72), C_VALUE)
    ct(d, W / 2, barH + heroH * 0.86, "km/h", f(14), C_UNIT)
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

    def metric(cx, top, label, value, unit, vsz):
        ct(d, cx, top + rowH * 0.24, label, f(11, False), C_ACCENT)
        ct(d, cx, top + rowH * 0.57, value, f(vsz), C_VALUE)
        if unit:
            ct(d, cx, top + rowH * 0.85, unit, f(11, False), C_UNIT)

    # puissance + barre de zone
    ct(d, cxL, gridY + rowH * 0.22, "PUISSANCE W", f(11, False), C_ACCENT)
    ct(d, cxL, gridY + rowH * 0.53, power, f(33), ZONE[zone] if zone else C_UNIT)
    barW = W * 0.40
    seg = barW / 6
    bx = cxL - (seg * 6) / 2
    by = gridY + rowH * 0.84
    bh = max(5, rowH * 0.11)
    for z in range(1, 7):
        col = ZONE[z] if (zone and z <= zone) else C_SEG_OFF
        d.rectangle([bx + (z - 1) * seg, by, bx + (z - 1) * seg + seg - 2, by + bh], fill=col)

    metric(cxR, gridY, "COEUR", hr, "bpm", 33)
    metric(cxL, gridY + rowH, "CADENCE", cad, "rpm", 27)
    metric(cxR, gridY + rowH, "PENTE", grade, "%", 27)
    metric(cxL, gridY + rowH * 2, "DISTANCE", dist, "km", 27)
    metric(cxR, gridY + rowH * 2, "ALTITUDE", alt, "m", 27)
    metric(cxL, gridY + rowH * 3, "TEMPS ROULANT", tmr, "", 25)
    metric(cxR, gridY + rowH * 3, "DENIVELE +", asc, "m", 27)
    return img


def rounded_shadow(field, radius=18):
    """Renvoie le champ avec coins arrondis facon ecran."""
    mask = Image.new("L", field.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, field.size[0], field.size[1]], radius=radius, fill=255)
    out = Image.new("RGBA", field.size, (0, 0, 0, 0))
    out.paste(field, (0, 0), mask)
    return out


def main():
    # --- captures par zone ---
    shots = [
        ("capture-z2-bleu.png", "28.4", "150", 2, "138", "88", "1.5", "12.30", "540", "0:42:10", "210", "21", "9:14"),
        ("capture-z4-jaune.png", "42.5", "185", 4, "154", "92", "6.2", "34.18", "1240", "1:23:45", "612", "24", "6:34"),
        ("capture-z6-rouge.png", "51.0", "420", 6, "176", "98", "9.8", "58.70", "1980", "2:05:30", "1340", "19", "15:02"),
    ]
    for fn, sp, pw, zn, hr, cad, gr, di, al, tm, asx, tp, ck in shots:
        render_field(sp, pw, zn, hr, cad, gr, di, al, tm, asx, tp, ck).save(os.path.join(HERE, fn))

    # --- image principale 1440x720 ---
    MW, MH = 1440, 720
    main_img = Image.new("RGB", (MW, MH), (0x24, 0x07, 0x16))
    md = ImageDraw.Draw(main_img)
    for y in range(MH):
        t = y / MH
        md.line([(0, y), (MW, y)],
                fill=tuple(int(a + (b - a) * t) for a, b in zip((0x2A, 0x08, 0x1A), (0x4A, 0x0E, 0x30))))
    # champ scale x1.25
    field = render_field("42.5", "185", 4, "154", "92", "6.2", "34.18", "1240", "1:23:45", "612", "24", "6:34")
    scale = 1.35
    fw, fh = int(W * scale), int(H * scale)
    fimg = rounded_shadow(field.resize((fw, fh), Image.LANCZOS), radius=24)
    fx, fy = 120, (MH - fh) // 2
    # ombre simple (bloc sombre decale)
    main_img.paste((10, 3, 12), (fx + 8, fy + 10, fx + 8 + fw, fy + 10 + fh))
    main_img.paste(fimg, (fx, fy), fimg)

    tx = fx + fw + 90
    md.text((tx, 150), "GIRO PINK", font=f(96), fill=(0xFF, 0x2E, 0x9C))
    md.text((tx, 260), "Tout l'ecran. Tout en rose.", font=f(40, False), fill=WHITE)
    bullets = [
        "Vitesse geante + 9 metriques",
        "Puissance en couleurs Zwift",
        "Barre de zones Z1 a Z6",
        "Pente, altitude, D+, temps roulant",
        "Concu pour Edge 1040",
    ]
    yy = 350
    for bsv in bullets:
        md.ellipse([tx, yy + 12, tx + 16, yy + 28], fill=(0xFF, 0x2E, 0x9C))
        md.text((tx + 32, yy), bsv, font=f(34, False), fill=(0xF0, 0xD5, 0xE5))
        yy += 58
    main_img.save(os.path.join(HERE, "image-principale-1440x720.png"))

    # --- couverture 500x500 ---
    CV = 500
    cov = Image.new("RGB", (CV, CV), (0xEC, 0x00, 0x8C))
    cd = ImageDraw.Draw(cov)
    for y in range(CV):
        t = y / CV
        cd.line([(0, y), (CV, y)],
                fill=tuple(int(a + (b - a) * t) for a, b in zip((0xF5, 0x2B, 0x9E), (0xC2, 0x00, 0x72))))
    ct(cd, CV / 2, 150, "GIRO", f(150), WHITE)
    ct(cd, CV / 2, 285, "PINK", f(150), (0x2A, 0x0A, 0x1E))
    ct(cd, CV / 2, 420, "EDGE 1040 DATA FIELD", f(28, False), (0xFF, 0xD5, 0xEC))
    cov.save(os.path.join(HERE, "image-couverture-500x500.png"))

    print("OK - images store generees")


if __name__ == "__main__":
    main()
