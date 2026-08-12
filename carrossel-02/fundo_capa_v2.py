# -*- coding: utf-8 -*-
"""CAPA v2 — Atlas montado a partir das CAMADAS do Image Decompose.

O v1 extraía a silhueta com limiar de luminância (funcionou porque o fundo da
foto era quase preto absoluto). O Higgsfield agora devolve a cena decomposta
em camadas com alpha, e isso muda duas coisas:

  · a borda vem do modelo, não de um limiar que só serve para fundo escuro
  · ESTÁTUA e GLOBO são camadas independentes, então o texto pode ficar
    ENTRE elas — atrás do globo e na frente do corpo

Saídas:
  fundos/capa2.png       campo + névoa + estátua (vai atrás do texto)
  fundos/capa2_over.png  só o globo, transparente (vai na frente do texto)
"""
import numpy as np
from PIL import Image

W, H = 1080, 1350
LINHA = round(H * 0.505)
PRETO = np.array((5, 5, 5), np.float32)
SEPIA = np.array((116, 101, 82), np.float32)

DEC = "decompose/atlas"
CORTE_Y = 1402          # o mesmo corte do v1 (1600 na fonte), na escala da camada
TOPO = 540              # topo do globo no canvas
NEVOA, NEVOA0 = 0.26, 0.11
GLOBE_XY = (137, 0)     # bbox devolvido pelo decompose, no espaço da camada


def main():
    est = Image.open(f"{DEC}/statue.png").convert("RGBA").crop((0, 0, 1528, CORTE_Y))
    alt = H - TOPO
    esc = alt / CORTE_Y
    larg = round(est.width * esc)
    est = est.resize((larg, alt), Image.LANCZOS)

    glb = Image.open(f"{DEC}/globe.png").convert("RGBA")
    glb = glb.resize((round(glb.width * esc), round(glb.height * esc)), Image.LANCZOS)

    # campo preto + névoa sépia abaixo da linha: aqui quem revela a borda dura
    # é TEMPERATURA, não brilho — cena e campo são os dois escuros
    y = np.arange(H, dtype=np.float32)[:, None, None]
    t = np.clip((y - LINHA) / (H - LINHA), 0, 1)
    g = np.where(y >= LINHA, NEVOA0 + (NEVOA - NEVOA0) * t ** 1.3, 0.0)
    fundo = Image.fromarray(np.clip(
        np.broadcast_to(PRETO + (SEPIA - PRETO) * g, (H, W, 3)), 0, 255
    ).astype(np.uint8)).convert("RGBA")

    # ORDEM IMPORTA: o globo entra ANTES da estátua. As mãos e a cabeça fazem
    # parte da camada "statue" e na cena real estão à frente da esfera — colar
    # o globo por cima inverte a profundidade e ele parece flutuar.
    x0 = (W - larg) // 2
    gx = x0 + round(GLOBE_XY[0] * esc)
    gy = TOPO + round(GLOBE_XY[1] * esc)
    fundo.alpha_composite(glb, (gx, gy))
    fundo.alpha_composite(est, (x0, TOPO))
    fundo.convert("RGB").save("fundos/capa2.png")

    a = np.asarray(est)[:, :, 3]
    ys = np.where((a > 128).any(1))[0]
    topo_real = TOPO + int(ys.min())
    print(f"capa2.png  linha {LINHA}px  estatua sobe ate y={topo_real}  "
          f"globo em ({gx},{gy}) {glb.width}x{glb.height}, "
          f"{LINHA - gy}px dentro do campo")


if __name__ == "__main__":
    main()
