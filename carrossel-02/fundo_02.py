# -*- coding: utf-8 -*-
"""FUNDOS DO SLIDE 02 — cena de marmore sobre a BASE-vega, intacta.

Mesma regra da capa: a base nao e editada nem coberta. A cena vem das
geracoes do Higgsfield (fundo preto de estudio), e o alpha e recuperado por
luminancia, porque o preto do estudio esta 250 niveis abaixo do marmore.

O corte por componente conectado tem um motivo: as geracoes trazem o halo da
luz de recorte flutuando no canto, solto do objeto. Ele passaria em qualquer
limiar razoavel e viraria mancha no meio do pontilhado.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

W, H = 1080, 1350
BASE = "BASE-vega.png"
LUM_LO, LUM_HI = 14, 40      # portao suave: o preto de estudio sai, a sombra
                             # propria do marmore fica


def disco(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def recorta(caminho):
    """Devolve a cena com alpha, ja aparada na caixa do objeto."""
    src = Image.open(caminho).convert("RGB")
    lum = np.asarray(src.convert("L"), np.float32)
    a = np.clip((lum - LUM_LO) / (LUM_HI - LUM_LO), 0, 1)

    solido = ndimage.binary_closing(a > 0.5, disco(4))
    solido = ndimage.binary_fill_holes(solido)
    lab, n = ndimage.label(solido)
    if n > 1:
        # NAO ficar so com o maior: na pilha, a placa que cai e um componente
        # separado, e e justamente ela que vai animar. Sai o que for
        # desprezivel perto do objeto — halo de luz, grão solto, poeira.
        areas = np.bincount(lab.ravel())[1:]
        fica = [i + 1 for i, ar in enumerate(areas) if ar >= areas.max() * 0.01]
        solido = np.isin(lab, fica)
        print(f"   {n} componentes, ficaram {len(fica)} "
              f"(maior {areas.max()}px)")
    a *= ndimage.binary_dilation(solido, disco(3))
    a = ndimage.gaussian_filter(a, 0.8)

    im = Image.fromarray(np.dstack([np.asarray(src, np.float32),
                                    np.clip(a, 0, 1) * 255]).astype(np.uint8), "RGBA")
    m = np.asarray(im)[:, :, 3] > 128
    ys, xs = np.where(m.any(1))[0], np.where(m.any(0))[0]
    return im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))


def recorta_card(caminho):
    """Recorta a TELA das geracoes de UI. Elas vem sobre fundo claro de
    estudio, entao o teste e o inverso do marmore: o card e a mancha ESCURA.
    Os cantos arredondados sobrevivem porque a mascara sai do proprio pixel."""
    src = Image.open(caminho).convert("RGB")
    lum = np.asarray(src.convert("L"), np.float32)
    card = ndimage.binary_fill_holes(lum < 200)
    lab, n = ndimage.label(card)
    if n > 1:
        areas = np.bincount(lab.ravel())[1:]
        card = lab == (int(areas.argmax()) + 1)   # a sombra solta fica de fora
    card = ndimage.binary_erosion(card, disco(2))  # come a borda clara do halo
    a = ndimage.gaussian_filter(card.astype(np.float32), 0.8)

    im = Image.fromarray(np.dstack([np.asarray(src, np.float32),
                                    np.clip(a, 0, 1) * 255]).astype(np.uint8), "RGBA")
    m = np.asarray(im)[:, :, 3] > 128
    ys, xs = np.where(m.any(1))[0], np.where(m.any(0))[0]
    return im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))


def montar(caminho, saida, larg=0.62, base_y=1350, S=1, card=False):
    """larg   = fracao da largura do quadro ocupada pela cena
       base_y = y do pe da cena; acima de H ela sangra pelo rodape"""
    w, h = W * S, H * S
    im = recorta_card(caminho) if card else recorta(caminho)
    esc = (w * larg) / im.width
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    topo = round(base_y * S) - im.height

    base = BASE if S == 1 else BASE.replace(".png", "@2x.png")
    fundo = Image.open(base).convert("RGBA")
    fundo.alpha_composite(im, ((w - im.width) // 2, topo))
    fundo.convert("RGB").save(saida)
    print(f"{saida}  cena {im.width}x{im.height}  topo y={topo}  "
          f"sangra {round(base_y * S) - h}px")


if __name__ == "__main__":
    # topo da cena tem que ficar abaixo do subtitulo, que termina em ~500
    montar("opcoes/01-clepsidra.png", "fundos/vol-a.png", larg=0.68, base_y=1420)
    # a ampulheta e alta: dimensionada pela largura como as outras, o topo dela
    # subia ate 346 e entrava no subtitulo. Aqui a largura cede pra altura caber
    montar("opcoes/02-ampulheta.png", "fundos/vol-b.png", larg=0.38, base_y=1400)
    montar("opcoes/03-pilha.png",     "fundos/vol-c.png", larg=0.56, base_y=1470)
