# -*- coding: utf-8 -*-
"""FUNDO DA CAPA — Atlas RECORTADO cruzando a linha do campo.

Nada de mascarar retângulo: a estátua é extraída com matte próprio e colada
sobre o campo. O fundo da foto é quase preto absoluto (média de luminância 1,2
e máximo 4,0 nos cantos, medido), então o matte sai da própria luminância entre
dois limiares — o que dá borda com antialias natural, sem halo e sem serrilha.

Composição, de baixo pra cima:
  campo Preto Cine em todo o quadro
  névoa sépia ABAIXO da linha — é ela que revela a linha, porque a cena é
  escura como o campo e quem separa os dois é a temperatura, não o brilho
  Atlas recortado por cima de tudo, atravessando a linha
"""
import numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1350
LINHA = round(H * 0.505)                 # 682
PRETO = np.array((5, 5, 5), np.float32)
SEPIA = np.array((116, 101, 82), np.float32)

SRC = "fundos/atlas_1.png"
CORTE_Y = 1600          # do topo do globo ao fim do torso, na fonte
TOPO = 540              # topo do globo no slide: 142px acima da linha
NEVOA = 0.26            # teto da névoa na base do quadro
NEVOA0 = 0.11           # degrau logo abaixo da linha — é ele que a revela
LO, HI = 3.5, 13.0      # limiares do matte (fundo < 4 · mármore > 13)

def matte(rgb):
    """alpha da estátua. Um blur pequeno ANTES do corte tira o ruído de sensor
    do fundo sem comer a borda; o corte depois devolve a silhueta."""
    lum = np.asarray(Image.fromarray(rgb.astype(np.uint8)).convert("L")
                     .filter(ImageFilter.GaussianBlur(0.6)), np.float32)
    return np.clip((lum - LO) / (HI - LO), 0, 1)

def main():
    src = Image.open(SRC).convert("RGB").crop((0, 0, 1744, CORTE_Y))
    alt = H - TOPO
    larg = round(src.width * alt / src.height)
    a = np.asarray(src.resize((larg, alt), Image.LANCZOS)).astype(np.float32)
    al = matte(a)

    y = np.arange(H, dtype=np.float32)[:, None, None]
    t = np.clip((y - LINHA) / (H - LINHA), 0, 1)
    # sem DEGRAU a névoa nasce em zero e a linha some junto com o recorte:
    # a borda dura precisa de um salto de temperatura, não de uma rampa
    g = np.where(y >= LINHA, NEVOA0 + (NEVOA - NEVOA0) * t ** 1.3, 0.0)
    arr = np.broadcast_to(PRETO + (SEPIA - PRETO) * g, (H, W, 3)).copy()

    x0 = (W - larg) // 2
    reg = arr[TOPO:TOPO + alt, x0:x0 + larg]
    arr[TOPO:TOPO + alt, x0:x0 + larg] = reg * (1 - al[:, :, None]) + a * al[:, :, None]

    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save("fundos/capa.png")

    sil = np.zeros((H, W), np.float32)
    sil[TOPO:TOPO + alt, x0:x0 + larg] = al
    op = sil > 0.5
    ys = np.where(op.any(1))[0]
    xs = np.where(op[LINHA])[0]
    print(f"capa.png  linha {LINHA}px ({LINHA/H*100:.1f}%)  "
          f"silhueta sobe ate y={ys.min()} ({LINHA-ys.min()}px dentro do campo)  "
          f"largura na linha {len(xs)}px, de x={xs.min()} a {xs.max()}")

if __name__ == "__main__":
    main()
