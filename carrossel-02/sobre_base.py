# -*- coding: utf-8 -*-
"""ATLAS SOBRE A BASE — a base entra intacta, a estátua só se sobrepõe.

Regra da peça: BASE-vega.png não é editada, recolorida nem coberta por
retângulo nenhum. Ela é o fundo; o recorte do Atlas (camada com alpha vinda
do Image Decompose) é colado por cima e só. Onde não há mármore, o
pontilhado continua aparecendo — inclusive nos vãos entre braço e corpo.

Dois cuidados que separam o colado do composto:

1. FUROS NO ALPHA. O decompose deixa buracos internos (um deles apareceu no
   peito, um quadrado de fundo vazando no meio do mármore). São tapados por
   preenchimento de furos na máscara, e a cor volta da imagem original.
2. ESCALA PELA LARGURA. Dimensionar pela altura disponível deixa a estátua
   magra no meio do quadro. O que dá presença é a largura ocupada; a altura
   resolve sangrando pela borda de baixo, que é corte, não falta de espaço.
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

W, H = 1080, 1350
BASE = "BASE-vega.png"
MAX_FURO = 4000       # px² — acima disso o buraco é vão da escultura, não defeito
LUM_LO, LUM_HI = 8, 26    # portão de luminância: só o quase-preto sai. Subir
                          # isso corta a sombra própria do mármore e esburaca


def disco(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def limpa(camada, original, fecha=5):
    """A camada do decompose é usada só como MÁSCARA; a cor vem sempre da
    imagem original. Assim um pedaço de fundo escuro que tenha sobrado dentro
    do recorte não vira mancha no meio do mármore.

    A máscara ainda leva um fechamento morfológico antes do preenchimento de
    furos: o matte deixa mordidas de poucos pixels na silhueta (borda do globo,
    ombro), e fechar antes de preencher recupera a curva sem inchar a forma."""
    lay = Image.open(camada).convert("RGBA")
    src = Image.open(original).convert("RGB").resize(lay.size, Image.LANCZOS)
    al = np.asarray(lay)[:, :, 3].astype(np.float32) / 255.0

    # limiar ALTO: a sombra projetada da estátua também vem na camada com
    # alpha baixo. Com corte em 0,06 o fechamento engolia essa sombra e ela
    # reaparecia como bloco escuro ao lado do globo.
    op = al > 0.5
    fechada = ndimage.binary_closing(op, disco(fecha))
    buracos = ndimage.binary_fill_holes(fechada) & ~fechada

    # SÓ furos pequenos são tapados. O vão entre o braço e o globo também é um
    # buraco fechado, e preenchê-lo cola o fundo escuro no meio da peça — foi
    # exatamente o bloco de sombra que apareceu ao lado da esfera.
    lab, n = ndimage.label(buracos)
    areas = np.bincount(lab.ravel())
    espurio = np.isin(lab, [i for i in range(1, n + 1) if areas[i] <= MAX_FURO])
    cheio = fechada | espurio
    add = cheio & ~op
    print(f"   mascara: {n} buracos, {int(espurio.sum())}px tapados, "
          f"+{int(add.sum())}px no total")

    # opacidade cravada SÓ no que foi acrescentado; na silhueta original o
    # antialias do modelo é preservado, senão a borda vira serrilha
    a = np.where(add, 1.0, al) * cheio

    # PORTÃO DE LUMINÂNCIA. O decompose entregou a sombra projetada dentro da
    # camada, com alpha alto — daí o bloco escuro ao lado do globo. Mármore,
    # mesmo na sombra própria, é muito mais claro que o fundo do estúdio, então
    # a luminância separa os dois sem tocar na silhueta.
    lum = np.asarray(Image.fromarray(np.asarray(src)).convert("L"), np.float32)
    a *= np.clip((lum - LUM_LO) / (LUM_HI - LUM_LO), 0, 1)

    # Fragmentos soltos saem, mas só os DESPREZÍVEIS (menos de 1% do corpo).
    # Nada de "ficar só o maior componente": com portão agressivo as junções
    # escuras afinam, o globo vira componente separado e a peça perde a esfera.
    lab, n = ndimage.label(a > 0.5)
    if n > 1:
        areas = np.bincount(lab.ravel())[1:]
        lixo = [i + 1 for i, ar in enumerate(areas) if ar < areas.max() * 0.01]
        if lixo:
            a *= ~ndimage.binary_dilation(np.isin(lab, lixo), disco(2))
            print(f"   {len(lixo)} fragmento(s) solto(s) removido(s)")
    a = ndimage.gaussian_filter(a, 0.6)

    out = np.dstack([np.asarray(src).astype(np.float32),
                     np.clip(a, 0, 1) * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def circulo_do_globo(alpha, frac=0.34):
    """Ajusta um círculo à calota superior da silhueta — é o globo.

    Só a faixa mais alta entra na conta: mais abaixo o contorno já é braço e
    ombro, e incluí-los puxa o centro pra baixo e estufa o raio. Ajuste
    algébrico de Kåsa, que resolve em um passo e não precisa de chute inicial.
    """
    op = alpha > 128
    topo = np.array([np.argmax(op[:, x]) if op[:, x].any() else -1
                     for x in range(op.shape[1])], float)
    val = topo >= 0
    xs = np.where(val)[0].astype(float)
    ys = topo[val]
    corte = ys.min() + (ys.max() - ys.min()) * frac
    m = ys <= corte
    xs, ys = xs[m], ys[m]

    A = np.c_[2 * xs, 2 * ys, np.ones(len(xs))]
    sol, *_ = np.linalg.lstsq(A, xs ** 2 + ys ** 2, rcond=None)
    cx, cy = sol[0], sol[1]
    r = float(np.sqrt(sol[2] + cx * cx + cy * cy))
    return float(cx), float(cy), r


def montar(camada, original, saida, larg=0.72, base_y=1730, S=1, base=None):
    """larg   = fração da largura do canvas que o mármore ocupa
       base_y = y do pé da estátua; acima de {H} ela sangra pela borda
       S      = fator de escala do canvas (2 = entrega em 2160x2700)

    Em S=2 a estátua é redimensionada a partir da camada ORIGINAL, que tem
    2048px de altura: o alvo cabe dentro dela, então a alta é resolução de
    verdade e não upscale de um render de 1080."""
    W, H = 1080 * S, 1350 * S
    base_y = round(base_y * S)
    base = base or (BASE if S == 1 else BASE.replace(".png", "@2x.png"))
    im = limpa(camada, original)
    a = np.asarray(im)[:, :, 3]
    ys = np.where((a > 128).any(1))[0]
    xs = np.where((a > 128).any(0))[0]
    im = im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))

    esc = (W * larg) / im.width
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    topo = base_y - im.height

    x0 = (W - im.width) // 2
    fundo = Image.open(base).convert("RGBA")           # intacta
    fundo.alpha_composite(im, (x0, topo))
    fundo.convert("RGB").save(saida)

    # o JSON do globo fica SEMPRE em coordenadas lógicas de 1080: é nelas que
    # o compositor desenha o arco, independente da escala de entrega
    cx, cy, r = circulo_do_globo(np.asarray(im)[:, :, 3])
    cx, cy = (cx + x0) / S, (cy + topo) / S
    json.dump({"cx": round(cx, 1), "cy": round(cy, 1), "r": round(r / S, 1)},
              open(os.path.splitext(saida)[0].replace("@2x", "") + ".json", "w"))
    print(f"{saida}  {im.width}x{im.height}  topo y={topo}  "
          f"sangra {base_y - H}px  globo c=({cx:.0f},{cy:.0f}) r={r:.0f}")


B = ("decompose/B/atlas.png", "fundos/atlas_B.png")
# C veio decomposto em três objetos (statue, sphere, base) e foi reunido num
# alpha só, respeitando o offset que o próprio decompose devolve por camada
C = ("decompose/C/atlas.png", "fundos/atlas_C.png")

if __name__ == "__main__":
    montar("decompose/A/atlas.png", "fundos/atlas_A.png", "SLIDE-atlas-A.png")
    montar(*B, "SLIDE-atlas-B.png")
    montar(*B, "SLIDE-atlas-B-contido.png", larg=0.52, base_y=1400)

    # três arranjos para responder onde o texto entra
    montar(*B, "fundos/arranjo-1.png", larg=0.52, base_y=1749)   # texto em cima
    montar(*B, "fundos/arranjo-2.png", larg=0.72, base_y=1730)   # texto por cima
    montar(*B, "fundos/arranjo-3.png", larg=0.40, base_y=1360)   # texto em cima, inteira
    # O ESCOLHIDO: estátua inteira, um pouco menor e mais baixa. base_y colado
    # em H de propósito — sangrar aqui decepa o pé de apoio, e é ele que
    # sustenta a leitura de alguém ajoelhado sob peso.
    # com o arco em duas linhas em vez de três, sobra raio: a estátua volta a
    # crescer sem que o texto encoste na headline
    # O plinto tem ~182px nesta escala; base_y = H + 91 corta exatamente na
    # metade dele. Descer a estátua também empurra o globo, e é essa folga
    # extra em cima que paga a legenda maior.
    montar(*C, "fundos/arco.png", larg=0.44, base_y=1441)
