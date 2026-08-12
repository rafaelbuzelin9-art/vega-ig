# -*- coding: utf-8 -*-
"""Prancha das opções de Atlas sobre a base."""
import os
from PIL import Image, ImageDraw, ImageFont

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ITENS = [("SLIDE-arranjo-1.png", "1 · texto em cima, estátua sangra"),
         ("SLIDE-arranjo-2.png", "2 · estátua cheia, texto embaixo"),
         ("SLIDE-arranjo-3.png", "3 · estátua inteira e pequena")]

LARG = 420
ALT = round(LARG * 1350 / 1080)
M, G, R = 40, 26, 54
W = M * 2 + LARG * len(ITENS) + G * (len(ITENS) - 1)
board = Image.new("RGB", (W, M * 2 + ALT + R), (12, 11, 10))
dr = ImageDraw.Draw(board)
f = ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 24)

for i, (arq, rot) in enumerate(ITENS):
    x = M + i * (LARG + G)
    board.paste(Image.open(arq).resize((LARG, ALT), Image.LANCZOS), (x, M))
    dr.text((x + LARG / 2, M + ALT + 14), rot, font=f,
            fill=(226, 219, 205), anchor="ma")

board.save("PRANCHA-arranjos.png")
print(f"PRANCHA-arranjos.png  {board.width}x{board.height}")
