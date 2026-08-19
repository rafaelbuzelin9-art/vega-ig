# -*- coding: utf-8 -*-
"""
VEGA · lockup de PEÇA — a marca com a lira em proporção de aplicação
====================================================================
Roda quando a marca mudar. Lê o `vega-lockup.svg` entregue pela v5 e devolve
um lockup próprio para peça gráfica, sem redesenhar nada: os mesmos paths, em
outra proporção.

POR QUE A PEÇA TEM LOCKUP PRÓPRIO
---------------------------------
No lockup de marca a lira mede 2.188 vezes a altura de caps. No canto de um
slide, onde a marca é assinatura e não protagonista, isso lê como símbolo
grande demais (Rafael, 19/08). Mesmo diagnóstico e mesma solução que o hero
do site (`site-v3/gera_v5.py`): a lira desce para 1.35 caps (escolha do Rafael entre 1.55, 1.35 e 1.20).

As três decisões são herdadas do hero, e nenhuma é arbitrária:
  · ALTURA em múltiplos da ALTURA DE CAPS, não em % do símbolo — caps é a
    medida que não muda quando o símbolo encolhe;
  · FOLGA também ancorada em caps: a folga de marca (0.775) foi desenhada
    para a lira grande; mantida, o nome descola do símbolo;
  · ALINHAMENTO pelo CENTRÓIDE DE TINTA, não pelo centro da caixa — a lira
    tem a massa no corpo e a bola pendurada embaixo.

O x medido é ABSOLUTO no viewBox de origem, não local do símbolo. Confundir
os dois espaços desloca a lira em meia largura — foi o erro que o hero pegou.

SAÍDA
-----
  vega-lockup-peca.svg / -tinta.svg   ao lado dos assets de origem
  + a geometria do canto, no stdout: é ela que vai para `.logo` no preset.css
"""
import subprocess, pathlib, re, sys
import numpy as np
from PIL import Image

ALTURA_CAPS = 1.35      # os dois botões do estudo (ver cabeçalho)
FOLGA_CAPS  = 0.62
PAD_CAPS    = 0.30

CAP_ALVO, MARG_X, CAP_MEIO = 29.0, 74, 101   # âncoras do canto, herdadas da v4
CHROME = pathlib.Path(__file__).parent  # placeholder; resolvido abaixo
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TMP = pathlib.Path(__file__).resolve().parent / "_lockup_peca_tmp"
LARG = 1400


def _raster(svg, largura=LARG, claro=False):
    """claro=True rasteriza sobre branco e inverte a leitura — é o que a
    versão -tinta pede: tinta escura sobre fundo preto sai como quadro vazio."""
    TMP.mkdir(exist_ok=True)
    p = TMP/"m.html"
    p.write_text(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0}}'
                 f'html,body{{background:{"#fff" if claro else "#000"}}}.w{{width:{largura}px}}'
                 f'.w svg{{width:100%;height:auto;display:block}}</style></head>'
                 f'<body><div class="w">{svg}</div></body></html>', encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={largura+20},{largura}",
                    f"--screenshot={(TMP/'m.png').as_posix()}", p.as_uri()],
                   check=True, capture_output=True)
    a = np.asarray(Image.open(TMP/"m.png").convert("L")).astype(float)/255
    return 1.0-a if claro else a


def recompoe(origem: pathlib.Path):
    lock = origem.read_text(encoding="utf-8")
    vb0 = re.search(r'viewBox="([-\d. ]+)"', lock).group(1)
    ms = re.search(r'<g transform="translate\(([\d.]+) ([\d.]+)\) scale\(([\d.]+)\)">(.*?)</g>',
                   lock, re.S)
    tx0, ty0, s0, corpo = float(ms.group(1)), float(ms.group(2)), float(ms.group(3)), ms.group(4)
    mn = re.search(r'<g fill="(#[0-9A-Fa-f]{6})" transform="translate\(([\d.]+) ([\d.]+)\)">(.*?)</g>',
                   lock, re.S)
    cor, nx, ny, nome = mn.group(1), float(mn.group(2)), float(mn.group(3)), mn.group(4)

    escuro = int(cor[1:3], 16)*0.299 + int(cor[3:5], 16)*0.587 + int(cor[5:7], 16)*0.114 < 128

    def tinta(trecho):
        a = _raster(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb0}">{trecho}</svg>', claro=escuro)
        ys, xs = np.nonzero(a > 0.02)
        mnx, mny, w, _h = [float(v) for v in vb0.split()]
        e = w/a.shape[1]; peso = a[a > 0.02]
        return dict(x0=mnx+xs.min()*e, x1=mnx+xs.max()*e, y0=mny+ys.min()*e,
                    y1=mny+ys.max()*e, cy=mny+(ys*peso).sum()/peso.sum()*e)

    sim = tinta(f'<g transform="translate({tx0} {ty0}) scale({s0})">{corpo}</g>')
    nom = tinta(f'<g fill="{cor}" transform="translate({nx} {ny})">{nome}</g>')
    cap = nom['y1']-nom['y0']; meio = (nom['y0']+nom['y1'])/2
    razao = (ALTURA_CAPS*cap)/(sim['y1']-sim['y0'])
    tx = nom['x0'] - FOLGA_CAPS*cap - (sim['x1']-tx0)*razao
    ty = meio - (sim['cy']-ty0)*razao
    px = lambda a: tx + (a-tx0)*razao
    py = lambda a: ty + (a-ty0)*razao
    pad = PAD_CAPS*cap
    ix0, ix1 = px(sim['x0']), nom['x1']
    iy0, iy1 = min(py(sim['y0']), nom['y0']), max(py(sim['y1']), nom['y1'])
    vb = f"{ix0-pad:.2f} {iy0-pad:.2f} {(ix1-ix0)+2*pad:.2f} {(iy1-iy0)+2*pad:.2f}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
           f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s0*razao:.5f})">{corpo}</g>'
           f'<g fill="{cor}" transform="translate({nx} {ny})">{nome}</g></svg>')
    return svg, (sim['y1']-sim['y0'])/cap


def canto(svg):
    """caixa/left/top que põem a cap em CAP_ALVO, a tinta na margem MARG_X e
    o meio da caixa alta na linha CAP_MEIO. Medido no pixel, não deduzido."""
    a = _raster(svg, 600); m = a > 0.235
    ys, xs = np.nonzero(m)
    mr = m.copy(); mr[:, :int(xs.min()+(xs.max()-xs.min())*0.45)] = False
    yr, _ = np.nonzero(mr)
    kcap = (yr.max()-yr.min()+1)/600
    caixa = CAP_ALVO/kcap
    return caixa, MARG_X - (xs.min()/600)*caixa, CAP_MEIO - (((yr.min()+yr.max())/2)/600)*caixa


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent
    for src, dst in [("vega-lockup.svg", "vega-lockup-peca.svg"),
                     ("vega-lockup-tinta.svg", "vega-lockup-peca-tinta.svg")]:
        p = base/src
        if not p.exists():
            print(f"  ! nao achei {p}"); continue
        svg, antes = recompoe(p)
        (base/dst).write_text(svg, encoding="utf-8")
        print(f"  + {dst}   lira {antes:.3f} -> {ALTURA_CAPS} caps")
    c, l, t = canto((base/"vega-lockup-peca.svg").read_text(encoding="utf-8"))
    print(f"\n.logo{{position:absolute;top:{t:.0f}px;left:{l:.0f}px;width:{c:.0f}px;line-height:0}}")
