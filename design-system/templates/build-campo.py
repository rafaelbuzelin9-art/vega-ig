#!/usr/bin/env python3
"""
Gera o CAMPO VEGA (quadro escuro + grid + logo) nos dois formatos de publicação.

  python3 build-campo.py

Saídas, nesta mesma pasta:
  campo-feed-1080x1350.html   template editável, feed 4:5
  campo-reel-1080x1920.html   template editável, reel 9:16
  campo-feed-1080x1350.png    overlay PNG com alfa (área da cena transparente)
  campo-reel-1080x1920.png    overlay PNG com alfa

O campo é o mesmo sistema nos dois: mesma largura (1080), logo os corpos,
tracking, glow, logo e grid são IDÊNTICOS. Só a altura muda — e com ela a
posição absoluta da linha, que continua cravada em 50,5% da altura.
"""
import base64, subprocess
from pathlib import Path
from PIL import Image

BASE   = Path(__file__).resolve().parent          # design-system/templates
DS     = BASE.parent                              # design-system
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

FIELD  = 0.505          # linha do sistema — não mexer sem revalidar tudo
LOGO_W = 196                      # caixa do lockup de peca (a v4 era 150)
LOGO_H = LOGO_W * 1417.89 / 4888.8  # viewBox do vega-lockup-peca.svg
LOGO_TOP = 72                     # tinta na margem 74, cap na linha 101

FORMATOS = {
    "feed": {"w": 1080, "h": 1350, "txt_top": 170},   # 170 = valor travado no slide 1
    "reel": {"w": 1080, "h": 1920, "txt_top": None},  # None = centra no vazio
}

# bloco de duas linhas: 72px + 104px, entrelinha 105%
BLOCO_TXT = (72 + 104) * 1.05


def altura_texto(cfg):
    """topo do bloco de texto: travado no feed, centrado no vazio no reel."""
    if cfg["txt_top"]:
        return cfg["txt_top"]
    vazio_topo = LOGO_TOP + LOGO_H
    vazio_base = FIELD * cfg["h"]
    return round(vazio_topo + (vazio_base - vazio_topo - BLOCO_TXT) / 2)


def css(cfg, overlay):
    folha = (DS / "preset.css").read_text()
    folha = folha.replace("__FONT__", base64.b64encode(
        (DS / "assets" / "jost-variable-latin.woff2").read_bytes()).decode())
    # preset.css crava 1080x1350; o reel reaproveita tudo menos a altura
    folha = folha.replace("__BG__", "" if overlay else "SUA-CENA-AQUI.jpg")
    extra = f"""
html,body{{width:{cfg['w']}px;height:{cfg['h']}px}}
.canvas{{width:{cfg['w']}px;height:{cfg['h']}px}}
.txt{{top:{altura_texto(cfg)}px}}
"""
    if overlay:
        # alfa: sem cena, sem texto — só o quadro para sobrepor a qualquer fundo
        extra += "html,body,.canvas{background:none!important}\n"
    return folha + extra


def html(cfg, overlay):
    corpo = "" if overlay else (
        '<div class="txt">'
        '<span class="l1">Antes da tecnologia</span>'
        '<span class="l2">Entendemos a <b class="hard">empresa</b></span>'
        "</div>"
    )
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Campo VEGA — {cfg['w']}x{cfg['h']}</title>
<style>{css(cfg, overlay)}</style></head><body>
<div class="canvas">
<div class="field"></div>
<div class="grid"></div>
<div class="logo">{(DS / "assets" / "vega-lockup-peca.svg").read_text()}</div>
{corpo}
</div></body></html>"""


def shot(pagina, saida, cfg):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--no-sandbox", "--force-device-scale-factor=2",
                    "--default-background-color=00000000",
                    f"--window-size={cfg['w']},{cfg['h']}",
                    "--virtual-time-budget=4000", "--allow-file-access-from-files",
                    f"--screenshot={saida}", f"file://{pagina}"],
                   check=True, capture_output=True)
    im = Image.open(saida).convert("RGBA").resize((cfg["w"], cfg["h"]), Image.LANCZOS)
    im.save(saida)
    return im


for nome, cfg in FORMATOS.items():
    stem = f"campo-{nome}-{cfg['w']}x{cfg['h']}"

    (BASE / f"{stem}.html").write_text(html(cfg, overlay=False))

    tmp = BASE / f"_overlay-{nome}.html"
    tmp.write_text(html(cfg, overlay=True))
    im = shot(tmp, BASE / f"{stem}.png", cfg)
    tmp.unlink()

    linha = round(FIELD * cfg["h"])
    a_campo = im.getpixel((540, linha - 40))[3]      # dentro do campo -> opaco
    a_cena  = im.getpixel((540, linha + 40))[3]      # abaixo da linha -> transparente
    print(f"{stem}: linha em {linha}px ({FIELD*100:.1f}%) · "
          f"texto no topo {altura_texto(cfg)}px · "
          f"alfa campo {a_campo} / cena {a_cena}")
