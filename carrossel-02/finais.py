# -*- coding: utf-8 -*-
"""ENTREGA — gera a pasta finais/ com a base e a capa, em 1x e 2x.

A alta não é upscale: o fundo é recomposto em 2160x2700 a partir da camada
original do Atlas (2048px de altura, resolução de sobra) sobre a base
renderizada em 2x pelo Chrome, e a tipografia é rasterizada direto em 2x.
"""
import shutil, subprocess, sys
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).resolve().parent
FINAIS = AQUI / "finais"
PY = sys.executable

ENTREGA = [
    ("BASE-vega.png",        "finais/VEGA-fundo-base.png"),
    ("BASE-vega-20g@2x.png", "finais/VEGA-fundo-base@2x.png"),
    ("SLIDE-arco-b.png",     "finais/VEGA-carrossel02-slide01.png"),
    ("SLIDE-arco-b@2x.png",  "finais/VEGA-carrossel02-slide01@2x.png"),
]


def roda(*args):
    subprocess.run([PY, *args], cwd=AQUI, check=True)


if __name__ == "__main__":
    FINAIS.mkdir(exist_ok=True)
    roda("base.py")                       # base 1x e 2x
    # o nível travado (20g) vira a base canônica, nos dois tamanhos
    shutil.copy(AQUI / "BASE-vega-20g.png", AQUI / "BASE-vega.png")
    shutil.copy(AQUI / "BASE-vega-20g@2x.png", AQUI / "BASE-vega@2x.png")
    roda("sobre_base.py")                 # fundos 1x (e o JSON do globo)
    roda("-c", "import sobre_base as s; "
         "s.montar(*s.C, 'fundos/arco@2x.png', larg=0.44, base_y=1441, S=2)")
    roda("compor.py", "arco-b")           # slide 1x e 2x

    for origem, destino in ENTREGA:
        shutil.copy(AQUI / origem, AQUI / destino)
        im = Image.open(AQUI / destino)
        kb = (AQUI / destino).stat().st_size / 1024
        print(f"{destino}  {im.width}x{im.height}  {kb:.0f} KB")
