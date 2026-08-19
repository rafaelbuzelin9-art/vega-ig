#!/usr/bin/env python3
"""
Renderiza slides do carrossel VEGA aplicando o preset travado.

  python3 render.py          -> renderiza todos os slides definidos
  python3 render.py 2        -> renderiza só o slide 2

Autoria do texto: use *asterisco* para marcar a palavra de ênfase.
  "Entendemos a *empresa*"  ->  "empresa" recebe peso 500 + brilho
"""
import base64, json, re, subprocess, sys
from pathlib import Path
from PIL import Image

BASE   = Path(__file__).resolve().parent
ROOT   = BASE.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H   = 1080, 1350

SLIDES = {
    1: {"bg": "slide1-raw.png", "l1": "Antes da tecnologia", "l2": "Entendemos a *empresa*"},
    2: {"bg": "slide2-cand-B.png", "l2": "Como ela *atrai*", "align": 0.505, "txt_top": 291},
    3: {"bg": "slide3-raw.png", "l2": "Como ela *vende*", "align": 0.505, "txt_top": 311},
}
# field  -> altura do campo preto em CSS. Ausente = já vem na imagem.
# suave  -> True troca a borda reta por degradê curto.
# align  -> alinha a linha dura da imagem nessa fração do quadro (0.505 = slide 1).


def _detectar_linha(im):
    """y da borda campo-preto -> cena: maior salto na FRAÇÃO de pixels claros.
    (salto de brilho médio confunde com bordas internas da cena, ex. degraus)"""
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    cols = range(0, w, 20)
    n = len(cols)
    rows = [sum(1 for x in cols if px[x, y] > 60) / n for y in range(h)]
    # a linha do sistema vive perto do meio; buscar fora disso pega degraus/bordas
    y0, y1 = int(h * 0.30), int(h * 0.62)
    return max(range(y0, y1), key=lambda y: rows[y + 1] - rows[y]) + 1


def preparar_fundo(nome_raw, destino, align=None):
    """3:4 -> 4:5 e levanta o preto puro para Preto Cine #050505.

    align=0.505 -> detecta a linha dura e distribui o corte entre topo e base
    para ela cair exatamente nessa fração do quadro final. Sem align, corta
    tudo do topo (comportamento do slide 1, já aprovado)."""
    im = Image.open(ROOT / "fundos" / nome_raw).convert("RGB")
    w, h = im.size
    novo_h = int(w * 5 / 4)
    corte = h - novo_h
    if corte < 0:
        raise SystemExit(f"{nome_raw}: imagem mais larga que 4:5, corte manual necessário")
    topo = corte
    if align:
        y_linha = _detectar_linha(im)
        topo = round(y_linha - align * novo_h)
        if topo < 0:
            # linha alta demais para o corte alcançar: estende o campo preto
            # por cima (preto sobre preto, emenda invisível) e corta só embaixo
            pad = -topo
            ext = Image.new("RGB", (w, h + pad), (5, 5, 5))
            ext.paste(im, (0, pad))
            im, h, topo = ext, h + pad, 0
            corte = h - novo_h
            y_linha += pad
            print(f"  linha alta: +{pad}px de campo preto no topo")
        topo = max(0, min(corte, topo))
        print(f"  linha do raw em {y_linha/h*100:.1f}% -> corte {topo}px topo / "
              f"{corte-topo}px base -> linha final em {(y_linha-topo)/novo_h*100:.1f}%")
    im = im.crop((0, topo, w, topo + novo_h)).point(lambda v: max(v, 5))
    im.resize((W * 2, H * 2), Image.LANCZOS).save(destino, quality=94)
    return topo, novo_h


def marcar_enfase(txt):
    return re.sub(r"\*(.+?)\*", r'<span class="hard">\1</span>', txt)


def render(n, cfg):
    bg = BASE / f"_bg{n}.jpg"
    preparar_fundo(cfg["bg"], bg, align=cfg.get("align"))

    css = (BASE / "preset.css").read_text()
    css = css.replace("__FONT__", base64.b64encode(
        (ROOT / "fonts" / "jost-variable-latin.woff2").read_bytes()).decode())
    css = css.replace("__BG__", bg.name)

    campo = ""
    if cfg.get("field"):
        css += f"\n:root{{--field:{cfg['field']}}}"
        campo = f'<div class="field{" suave" if cfg.get("suave") else ""}"></div>'
    if cfg.get("txt_top"):
        css += f"\n.txt{{top:{cfg['txt_top']}px}}"

    linhas = "".join(
        f'<span class="{c}">{marcar_enfase(cfg[c])}</span>'
        for c in ("l1", "l2") if cfg.get(c)
    )

    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<style>{css}</style></head><body><div class="canvas">
{campo}
<div class="grid"></div>
<div class="logo">{(ROOT / "vega-lockup-peca.svg").read_text()}</div>
<div class="txt">{linhas}</div>
</div></body></html>"""

    pagina = BASE / f"_slide{n}.html"
    pagina.write_text(html)
    shot = BASE / f"_shot{n}.png"

    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--no-sandbox", "--force-device-scale-factor=2",
                    f"--window-size={W},{H}", "--virtual-time-budget=4000",
                    "--allow-file-access-from-files",
                    f"--screenshot={shot}", f"file://{pagina}"],
                   check=True, capture_output=True)

    saida = ROOT / f"SLIDE{n}.png"
    im = Image.open(shot).convert("RGB").resize((W, H), Image.LANCZOS)
    im.save(saida)

    # confere se alguma linha de texto vazou a margem lateral
    px = im.convert("L").load()
    faixa = range(150, 430)          # cobre o bloco de texto inteiro
    esq = next((x for x in range(W) if any(px[x, y] > 70 for y in faixa)), None)
    dir_ = next((x for x in range(W - 1, -1, -1) if any(px[x, y] > 70 for y in faixa)), None)
    if esq is None or dir_ is None:
        print(f"SLIDE{n}.png  <-- nenhum texto detectado, conferir manualmente")
        return
    md = W - 1 - dir_
    aviso = "" if esq >= 20 and md >= 20 else "  <-- MARGEM APERTADA"
    print(f"SLIDE{n}.png  margens {esq}/{md}px{aviso}")


if __name__ == "__main__":
    alvos = [int(a) for a in sys.argv[1:]] or sorted(SLIDES)
    for n in alvos:
        render(n, SLIDES[n])
