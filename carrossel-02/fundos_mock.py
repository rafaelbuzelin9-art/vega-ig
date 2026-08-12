# -*- coding: utf-8 -*-
"""FUNDOS MOCK — slides 03 a 06 do carrossel 02.

NÃO é arte final. São wireframes na geometria certa (linha em 50,5%, elemento
cruzando, jogo de cores) para julgar o ARCO do carrossel antes de gastar
geração no Higgsfield. A capa e o volume já são reais; estes quatro são mock.

Cada um respeita o sistema: campo preto ou creme até a linha, borda reta e
dura, e UM elemento da cena atravessando.
"""
import glob, math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
DIA = r"C:\Users\rafae\Downloads\replit-design-DbYioAEAmd_\vega-dia"

W, H = 1080, 1350
LINHA = round(H * 0.505)                  # 682
PRETO = np.array((5, 5, 5), np.float32)
CREME = np.array((242, 234, 217), np.float32)
SEPIA = np.array((116, 101, 82), np.float32)
GRAFITE = np.array((86, 76, 62), np.float32)


def nevoa(arr, teto=0.26, degrau=0.11):
    """A mesma névoa da capa: quem separa campo e cena aqui é TEMPERATURA,
    não brilho — os dois são escuros. O degrau logo abaixo da linha é o que
    revela a borda dura."""
    y = np.arange(H, dtype=np.float32)[:, None, None]
    t = np.clip((y - LINHA) / (H - LINHA), 0, 1)
    g = np.where(y >= LINHA, degrau + (teto - degrau) * t ** 1.3, 0.0)
    return arr * (1 - g) + SEPIA * g


def bolinhas(dr, passo=26, raio=1.3, cor=(242, 234, 217), alpha=26, y0=0):
    """A grade do fim do filme — o mundo do SISTEMA."""
    for y in range(y0, H, passo):
        for x in range(passo // 2, W, passo):
            dr.ellipse([x - raio, y - raio, x + raio, y + raio],
                       fill=cor + (alpha,))


def campo(arr, claro=False):
    arr[:LINHA] = CREME if claro else PRETO
    return arr


def salvar(im, nome, cruza_ate):
    im.save(f"fundos/{nome}.png")
    print(f"{nome}.png  linha {LINHA}px  elemento cruza ate y={cruza_ate} "
          f"({LINHA - cruza_ate}px dentro do campo)")


# ---------------------------------------------------------------- 03 · arcos
def arcos():
    """A VIRADA: o aqueduto. Um homem segurando tudo (capa) × muitos arcos
    dividindo tudo. Os arcos nascem na cena e os topos entram no campo."""
    base = np.broadcast_to(PRETO, (H, W, 3)).copy()
    base = nevoa(base, teto=0.20, degrau=0.09)
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    bolinhas(dr, y0=LINHA + 26, alpha=22)

    # Aqueduto de VERDADE são duas ordens: arcada larga no chão e arcada miúda
    # sobre o tabuleiro. Uma ordem só lê como fileira de portas, não como obra.
    cor = (231, 220, 198, 150)
    solo, tabuleiro = H - 70, 902

    def arcada(vao, r, base, topo_pilar):
        for i in range(int(W / vao) + 2):
            cx = -vao // 2 + i * vao
            cy = topo_pilar + r
            dr.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=cor, width=3)
            dr.line([cx - r, cy, cx - r, base], fill=cor, width=3)
            dr.line([cx + r, cy, cx + r, base], fill=cor, width=3)

    arcada(300, 148, solo, tabuleiro + 44)          # ordem baixa, no chão
    dr.line([0, tabuleiro, W, tabuleiro], fill=cor, width=4)
    arcada(196, 118, tabuleiro, LINHA - 52)         # ordem alta, cruza a linha
    dr.line([0, LINHA - 66, W, LINHA - 66], fill=(231, 220, 198, 120), width=3)

    im = Image.alpha_composite(im, ov).convert("RGB")
    salvar(im, "arcos", LINHA - 66)


# ------------------------------------------------------------- 04 · sistema
def sistema():
    """O QUE O SISTEMA FAZ: quatro colunas de pontos, uma por automação.
    A quarta acende até dentro do campo — é ela que cruza."""
    base = np.broadcast_to(PRETO, (H, W, 3)).copy()
    base = nevoa(base, teto=0.14, degrau=0.06)
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    bolinhas(dr, y0=LINHA + 26, alpha=20)

    alturas = [LINHA + 210, LINHA + 130, LINHA + 60, LINHA - 78]
    for i, topo in enumerate(alturas):
        cx = 190 + i * 235
        y = H - 60
        while y > topo:
            f = np.clip((H - 60 - y) / (H - 60 - topo), 0, 1)
            a = int(40 + 190 * f)
            r = 3.0 + 2.4 * f
            dr.ellipse([cx - r, y - r, cx + r, y + r], fill=(242, 234, 217, a))
            y -= 46
        r = 7 + 3 * (i == 3)
        dr.ellipse([cx - r, topo - r, cx + r, topo + r], fill=(246, 239, 222, 255))

    glow = ov.filter(ImageFilter.GaussianBlur(9))
    im = Image.alpha_composite(Image.alpha_composite(im, glow), ov).convert("RGB")
    salvar(im, "sistema", alturas[3])


# ---------------------------------------------------------------- 05 · freio
def freio():
    """O FREIO no gesso, campo creme. Riscos que avançam e PARAM: um deles
    cruza a linha e é cortado pela barra de interdição. O elemento que
    atravessa é o próprio limite."""
    a = Image.open(os.path.join(DIA, "cena1_dia_4k.png")).convert("RGB")
    ph = 2100 - 900
    pw = int(ph * W / H)
    x0 = (a.width - pw) // 2
    gesso = a.crop((x0, 900, x0 + pw, 2100)).resize((W, H), Image.LANCZOS)

    im = np.asarray(gesso).astype(np.float32)
    tinta = np.zeros((H, W), np.float32)
    stamps = [Image.open(f).convert("RGBA")
              for f in sorted(glob.glob(os.path.join(AQUI, "stamps", "hi*.png")))]
    rnd = random.Random(11)

    def risco(cx, cy, alt, ang, forca):
        st = stamps[rnd.randrange(len(stamps))]
        s = alt / st.height
        t = st.resize((max(int(st.width * s), 3), max(int(st.height * s), 3)),
                      Image.LANCZOS)
        t = t.rotate(ang, resample=Image.BICUBIC, expand=True, fillcolor=(0, 0, 0, 0))
        m = np.asarray(t)[:, :, 3].astype(np.float32) / 255.0 * forca
        hh, ww = m.shape
        px, py = int(cx - ww / 2), int(cy - hh / 2)
        X0, Y0 = max(px, 0), max(py, 0)
        X1, Y1 = min(px + ww, W), min(py + hh, H)
        if X1 <= X0 or Y1 <= Y0:
            return
        sub = m[Y0 - py:Y1 - py, X0 - px:X1 - px]
        im[Y0:Y1, X0:X1] = im[Y0:Y1, X0:X1] * (1 - sub[:, :, None]) + GRAFITE * sub[:, :, None]
        tinta[Y0:Y1, X0:X1] = np.maximum(tinta[Y0:Y1, X0:X1], sub)

    # Três avanços que sobem da base e PARAM sob uma barra de interdição.
    # O stamp é um traço vertical: ângulo ~0 mantém vertical, ~90 deita.
    for cx, topo in [(300, LINHA + 170), (540, LINHA - 58), (780, LINHA + 130)]:
        y = H - 90
        while y > topo + 70:
            risco(cx + rnd.uniform(-6, 6), y, 150, rnd.uniform(-3, 3), 0.58)
            y -= 128
        risco(cx, topo, 190, 90, 0.80)          # a barra que interdita

    k = np.clip(tinta * 1.25, 0, 1)[:, :, None]
    campo_cor = CREME * (1 - k) + GRAFITE * k
    im[:LINHA] = campo_cor[:LINHA]

    acima = np.where((tinta[:LINHA] > 0.12).any(1))[0]
    salvar(Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)), "freio",
           int(acima.min()) if len(acima) else LINHA)


# ---------------------------------------------------------------- 06 · fecho
def fecho():
    """FECHO: volta o Preto Cine com a grade parada e a estrela de seis raios
    da marca nascendo na cena e entrando no campo."""
    base = np.broadcast_to(PRETO, (H, W, 3)).copy()
    base = nevoa(base, teto=0.10, degrau=0.05)
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    bolinhas(dr, y0=LINHA + 26, alpha=18)

    cx, cy, R = W // 2, LINHA + 84, 132
    for k in range(6):
        ang = math.radians(90 + k * 60)
        for lado in (1, -1):
            dr.line([cx, cy, cx + lado * R * math.cos(ang), cy - lado * R * math.sin(ang)],
                    fill=(246, 239, 222, 120), width=2)
    dr.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(246, 239, 222, 255))

    glow = ov.filter(ImageFilter.GaussianBlur(11))
    im = Image.alpha_composite(Image.alpha_composite(im, glow), ov).convert("RGB")
    salvar(im, "fecho", cy - R)


if __name__ == "__main__":
    os.chdir(AQUI)
    arcos(); sistema(); freio(); fecho()
