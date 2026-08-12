# -*- coding: utf-8 -*-
"""CAPA v3 — sem caixa. Fundo Preto Cine em todo o quadro e o Atlas recortado
por cima; o campo do texto passa a ser SOBREPOSIÇÃO, não corte.

O que mudou em relação ao v2, e por quê:
  · saiu a névoa sépia. Ela existia para revelar a borda dura do campo, mas
    como cena e campo são os dois escuros, ela virava uma faixa que lia como
    retângulo cortando a estátua
  · a silhueta vem do Image Decompose em modo STANDARD, que devolve a estátua
    e o globo numa camada só. O modo granular separava os dois e deixava uma
    falha na borda da esfera, onde a mão a encobria na cena original

A linha do sistema continua existindo: quem a marca é o grid de pontos do
preset, que se esvai antes de 50,5%.
"""
import sys
import numpy as np
from PIL import Image

W, H = 1080, 1350
LINHA = round(H * 0.505)
PRETO = (5, 5, 5)

SRC = "decompose/atlas/atlas_inteiro.png"
CORTE_Y = 1402          # mesmo corte do v1 (1600 na fonte), na escala da camada


def main(topo=540, saida="capa3.png"):
    src = Image.open(SRC).convert("RGBA").crop((0, 0, 1528, CORTE_Y))
    alt = H - topo
    larg = round(src.width * alt / CORTE_Y)
    src = src.resize((larg, alt), Image.LANCZOS)

    fundo = Image.new("RGBA", (W, H), PRETO + (255,))
    x0 = (W - larg) // 2
    fundo.alpha_composite(src, (x0, topo))
    fundo.convert("RGB").save(f"fundos/{saida}")

    a = np.asarray(src)[:, :, 3]
    ys = np.where((a > 128).any(1))[0]
    xs = np.where((a > 128).any(0))[0]
    topo_real = topo + int(ys.min())
    print(f"{saida}  fundo preto puro  silhueta de y={topo_real} "
          f"({LINHA - topo_real}px acima da linha)  largura {xs.max()-xs.min()}px")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(int(sys.argv[1]), sys.argv[2])
    else:
        main()
