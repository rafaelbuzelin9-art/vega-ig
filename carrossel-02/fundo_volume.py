# -*- coding: utf-8 -*-
"""FUNDO DO VOLUME — contagem de grafite transbordando a linha do campo.

Cena: painel de gesso do filme (cena1_dia_4k.png, faixa limpa 900..2100 medida).
Campo: CREME chapado até 50,5%, alternando com o preto da capa.
Elemento que quebra a linha: os grupos de contagem que passam dela. Grafite
escuro sobre creme lê perfeitamente — o volume literalmente ultrapassando.

Os riscos são STAMPS de traço real (grão e poeira no canal alpha), carimbados
com jitter. Linha desenhada por código lê como vetor, não como lápis.
"""
import os, math, glob, random
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
DIA = r"C:\Users\rafae\Downloads\replit-design-DbYioAEAmd_\vega-dia"

W, H = 1080, 1350
LINHA = round(H * 0.505)                 # 682
GY0, GY1 = 900, 2100                     # faixa de gesso limpo no 4K
CREME = np.array((242, 234, 217), np.float32)
GRAFITE = np.array((86, 76, 62), np.float32)

STAMPS = [Image.open(f).convert("RGBA")
          for f in sorted(glob.glob(os.path.join(AQUI, "stamps", "hi*.png")))]

def gesso():
    a = Image.open(os.path.join(DIA, "cena1_dia_4k.png")).convert("RGB")
    ph = GY1 - GY0
    pw = int(ph * W / H)
    x0 = (a.width - pw) // 2
    return a.crop((x0, GY0, x0 + pw, GY1)).resize((W, H), Image.LANCZOS)

def risco(im, tinta, cx, cy, alt, ang, forca, rnd):
    st = STAMPS[rnd.randrange(len(STAMPS))]
    s = alt / st.height
    t = st.resize((max(int(st.width * s), 3), max(int(st.height * s), 3)), Image.LANCZOS)
    t = t.rotate(ang, resample=Image.BICUBIC, expand=True, fillcolor=(0, 0, 0, 0))
    a = np.asarray(t)[:, :, 3].astype(np.float32) / 255.0 * forca
    ph, pw = a.shape
    x0, y0 = int(cx - pw / 2), int(cy - ph / 2)
    X0, Y0 = max(x0, 0), max(y0, 0)
    X1, Y1 = min(x0 + pw, W), min(y0 + ph, H)
    if X1 <= X0 or Y1 <= Y0:
        return
    sub = a[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    im[Y0:Y1, X0:X1] = im[Y0:Y1, X0:X1] * (1 - sub[:, :, None]) + GRAFITE * sub[:, :, None]
    tinta[Y0:Y1, X0:X1] = np.maximum(tinta[Y0:Y1, X0:X1], sub)

def grupo(im, tinta, cx, cy, alt, giro, rnd, forca):
    passo = alt * 0.23
    c, s = math.cos(math.radians(giro)), math.sin(math.radians(giro))
    for i in range(4):
        dx = (i - 1.5) * passo
        risco(im, tinta, cx + dx * c, cy + dx * s + rnd.uniform(-5, 5),
              alt * rnd.uniform(0.93, 1.07), giro + rnd.uniform(-5, 5),
              forca * rnd.uniform(0.80, 1.0), rnd)
    risco(im, tinta, cx, cy, alt * 1.18, giro + rnd.uniform(56, 72),
          forca * rnd.uniform(0.85, 1.0), rnd)

def main(seed=7):
    rnd = random.Random(seed)
    im = np.asarray(gesso()).astype(np.float32)
    tinta = np.zeros((H, W), np.float32)

    # malha frouxa de baixo pra cima; a fileira mais alta CRUZA a linha
    px, py, alt = 150, 132, 76
    y = H + 30
    while y > LINHA + py * 0.5:          # a malha comum para ANTES da linha
        x = -60 + rnd.uniform(0, px)
        while x < W + 80:
            grupo(im, tinta, x + rnd.uniform(-22, 22), y + rnd.uniform(-30, 30),
                  alt * rnd.uniform(0.84, 1.16), rnd.uniform(-8, 8), rnd, 0.62)
            x += px * rnd.uniform(0.88, 1.12)
        y -= py * rnd.uniform(0.90, 1.10)

    # a fileira que ATRAVESSA: centrada na própria linha e mais alta, pra nascer
    # na cena e terminar dentro do campo. Solta acima da linha ela lê como
    # mancha; é o cruzamento que é a assinatura da série.
    x = -40 + rnd.uniform(0, px)
    while x < W + 80:
        grupo(im, tinta, x + rnd.uniform(-18, 18), LINHA + rnd.uniform(-6, 22),
              152 * rnd.uniform(0.92, 1.10), rnd.uniform(-7, 7), rnd, 0.72)
        x += px * 1.34 * rnd.uniform(0.90, 1.10)

    # CAMPO CREME chapado acima da linha, preservando só o grafite que cruzou
    k = np.clip(tinta * 1.25, 0, 1)[:, :, None]
    campo = CREME * (1 - k) + GRAFITE * k
    im[:LINHA] = campo[:LINHA]

    Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).save("fundos/volume.png")
    acima = (tinta[:LINHA] > 0.12)
    ys = np.where(acima.any(1))[0]
    print(f"volume.png  linha {LINHA}px  grafite no campo: {acima.mean()*100:.2f}% "
          f"da area, sobe ate y={ys.min() if len(ys) else '-'}")

if __name__ == "__main__":
    main()
