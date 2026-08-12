# -*- coding: utf-8 -*-
"""PRANCHA DE CONTATO dos 6 slides.

O post-mortem do 01 diz que a monotonia só apareceu com o carrossel inteiro
pronto, porque nunca se montou uma prancha durante a produção. Esta existe
para julgar ARCO, RITMO e JOGO DE CORES antes de qualquer arte final.
"""
import os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)

SLIDES = [("capa-b", "01 · capa", False), ("volume", "02 · volume", False),
          ("arcos", "03 · a virada", True), ("sistema", "04 · o sistema", True),
          ("freio", "05 · o freio", True), ("fecho", "06 · fecho", True)]

LARG, MARG, GAP, RODAPE = 400, 44, 30, 62
COLS = 3
ALT = round(LARG * 1350 / 1080)
LINHAS = (len(SLIDES) + COLS - 1) // COLS

W = MARG * 2 + LARG * COLS + GAP * (COLS - 1)
H = MARG * 2 + (ALT + RODAPE) * LINHAS + GAP * (LINHAS - 1)

fonte = ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 26)
mini = ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 20)

board = Image.new("RGB", (W, H), (20, 18, 16))
dr = ImageDraw.Draw(board)

for i, (nome, rotulo, mock) in enumerate(SLIDES):
    c, l = i % COLS, i // COLS
    x = MARG + c * (LARG + GAP)
    y = MARG + l * (ALT + RODAPE + GAP)
    board.paste(Image.open(f"SLIDE-{nome}.png").resize((LARG, ALT), Image.LANCZOS), (x, y))
    dr.text((x + LARG / 2, y + ALT + 18), rotulo, font=fonte,
            fill=(226, 219, 205), anchor="ma")
    if mock:
        dr.text((x + LARG / 2, y + ALT + 50), "fundo mock", font=mini,
                fill=(140, 128, 110), anchor="ma")

board.save("PRANCHA-6.png")
print(f"PRANCHA-6.png  {W}x{H}")
