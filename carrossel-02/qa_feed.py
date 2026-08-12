# -*- coding: utf-8 -*-
"""QA de feed: a peça em três tamanhos.

Julgar no monitor em tamanho cheio engana nos dois sentidos. O carrossel é
lido a ~350px de largura, e é nesse tamanho que a legenda em arco e o
pontilhado precisam sobreviver."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

os.chdir(os.path.dirname(os.path.abspath(__file__)))
alvo = sys.argv[1] if len(sys.argv) > 1 else "SLIDE-arco.png"
im = Image.open(alvo).convert("RGB")

TAM = [(560, "560px"), (350, "350px · feed"), (220, "220px · grade do perfil")]
M, G, R = 40, 30, 46
alt = lambda w: round(w * im.height / im.width)
W = M * 2 + sum(t for t, _ in TAM) + G * (len(TAM) - 1)
H = M * 2 + alt(TAM[0][0]) + R

board = Image.new("RGB", (W, H), (12, 11, 10))
dr = ImageDraw.Draw(board)
f = ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 22)
x = M
for t, rot in TAM:
    board.paste(im.resize((t, alt(t)), Image.LANCZOS), (x, M))
    dr.text((x + t / 2, M + alt(TAM[0][0]) + 12), rot, font=f,
            fill=(226, 219, 205), anchor="ma")
    x += t + G
board.save("QA-feed.png")
print(f"QA-feed.png  {W}x{H}  de {alvo}")
