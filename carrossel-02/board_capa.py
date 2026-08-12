# -*- coding: utf-8 -*-
"""ANTES x DEPOIS da capa: matte por limiar (v1) contra camadas do Image
Decompose (v2). Inclui um par de crops 1:1 na borda mais difícil — os dedos
recortados contra o campo — porque é lá que matte ruim aparece."""
import os
from PIL import Image, ImageDraw, ImageFont

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PARES = [("SLIDE-capa-b.png", "antes · campo cortando a cena"),
         ("SLIDE-capa-d.png", "D · preto puro, texto sobreposto"),
         ("SLIDE-capa-e.png", "E · idem, Atlas subindo mais")]
CROP = (170, 500, 470, 740)          # borda da mão, onde matte ruim aparece

LARG = 470
ALT = round(LARG * 1350 / 1080)
CW, CH = CROP[2] - CROP[0], CROP[3] - CROP[1]
MARG, GAP, ROT = 40, 28, 46

W = MARG * 2 + LARG * len(PARES) + GAP * (len(PARES) - 1)
H = MARG * 2 + ALT + ROT + GAP + CH + ROT

board = Image.new("RGB", (W, H), (20, 18, 16))
dr = ImageDraw.Draw(board)
f = ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 24)
fm = ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 19)

for i, (arq, rot) in enumerate(PARES):
    im = Image.open(arq).convert("RGB")
    x = MARG + i * (LARG + GAP)
    board.paste(im.resize((LARG, ALT), Image.LANCZOS), (x, MARG))
    dr.text((x + LARG / 2, MARG + ALT + 12), rot, font=f,
            fill=(226, 219, 205), anchor="ma")
    y = MARG + ALT + ROT + GAP
    board.paste(im.crop(CROP), (x + (LARG - CW) // 2, y))
    dr.text((x + LARG / 2, y + CH + 10), "detalhe 1:1 · borda na linha",
            font=fm, fill=(140, 128, 110), anchor="ma")

board.save("BOARD-capa-v1-v2.png")
print(f"BOARD-capa-v1-v2.png  {W}x{H}")
