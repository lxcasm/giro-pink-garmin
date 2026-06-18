# -*- coding: utf-8 -*-
"""Genere l'icone de lanceur (maglia rosa) pour le champ de donnees Giro Pink."""
import os
from PIL import Image, ImageDraw, ImageFont

PINK = (236, 0, 140, 255)
PINK_DK = (158, 0, 95, 255)
WHITE = (255, 255, 255, 255)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "resources", "drawables", "launcher_icon.png"))


def load_font(size):
    for name in ("arialbd.ttf", "ariblk.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def make_icon(size=60):
    # supersampling pour des bords nets
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(s * 0.22)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=r, fill=PINK)
    # liseré rose foncé
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=r, outline=PINK_DK, width=max(2, s // 40))

    font = load_font(int(s * 0.68))
    text = "G"
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text(((s - tw) / 2 - bbox[0], (s - th) / 2 - bbox[1]), text, font=font, fill=WHITE)

    img = img.resize((size, size), Image.LANCZOS)
    img.save(OUT)
    print("OK ->", OUT)


if __name__ == "__main__":
    make_icon(40)
