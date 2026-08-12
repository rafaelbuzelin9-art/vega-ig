# -*- coding: utf-8 -*-
"""ANIMAÇÃO DO SLIDE 02 — cursor clica, cartão nasce, número sobe.

Como o vídeo é montado:
  1. o slide SEM o painel vira uma imagem de fundo (fundo, wordmark, headline e
     subtítulo já rasterizados pelo compor.py);
  2. por cima entra só o painel, em Tailwind, animado por um relógio próprio;
  3. o puppeteer varre o tempo quadro a quadro e o ffmpeg fecha o MP4.

O passo 1 existe porque Tailwind e preset.css se anulam no mesmo documento
(`*{margin:0;padding:0}` mata o px-6/py-6 do cartão). Separando, cada um manda
no seu documento e o encontro acontece em pixel.
"""
import base64, json, subprocess, sys
from pathlib import Path

import compor

AQUI = Path(__file__).resolve().parent
FRAMES = AQUI / "_frames"
DUR = 6.0          # segundos
FPS = 30
ESCALA = 2         # captura em 2160x2700 e o ffmpeg reduz


def fundo_sem_painel(nome="volume"):
    """Rasteriza o slide sem o painel: é o cenário fixo do vídeo."""
    cfg = dict(compor.SLIDES[nome])
    cfg.pop("card", None)
    compor.render("_cenario", cfg)
    return AQUI / "SLIDE-_cenario.png"


def html_anim(C, cenario):
    cartoes = "".join(
        f'<div class="cartao" data-i="{i}">'
        f'<div data-slot="card" class="{compor.CARD_CLS}">'
        f'<span class="ripple"></span><span class="flash"></span>'
        f'<div data-slot="card-header" class="grid auto-rows-min '
        f'grid-rows-[auto_auto] items-start gap-2 px-6">'
        f'<div data-slot="card-description" class="text-sm text-muted-foreground">'
        f'{m["rot"]}</div>'
        f'<div data-slot="card-title" class="leading-none font-semibold '
        f'text-2xl tabular-nums @[250px]/card:text-3xl">'
        f'<span class="valor" data-alvo="{m["alvo"]}">0</span> {m["un"]}'
        f'</div></div></div></div>'
        for i, m in enumerate(C["metricas"]))

    Z = C.get("zoom", 1)
    larg = round(C["larg"] * Z)
    esq = (compor.W - larg) // 2
    fonte = base64.b64encode(
        (compor.DS / "assets" / "jost-variable-latin.woff2").read_bytes()).decode()

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="shadcn-ref/saida.css">
<style>
@font-face{{font-family:'Jost';src:url(data:font/woff2;base64,{fonte})
  format('woff2');font-weight:100 900}}
html,body{{margin:0;width:1080px;height:1350px;overflow:hidden;background:#050505}}
body{{background:url('{cenario.name}') no-repeat;font-family:'Jost'}}
*{{font-family:'Jost'}}
.painel{{position:absolute;left:{esq}px;top:{C["top"]}px;width:{larg}px}}
.escala{{zoom:{Z}}}
.cartao{{transform-origin:50% 30%;will-change:transform,opacity,filter}}
.cartao + .cartao{{margin-top:16px}}
[data-slot=card]{{position:relative;overflow:hidden}}
/* RIPPLE: o anel que sai de onde o cursor tocou */
.ripple{{position:absolute;left:50%;top:50%;width:40px;height:40px;
  margin:-20px 0 0 -20px;border-radius:50%;pointer-events:none;
  border:2px solid rgba(242,234,217,.55);opacity:0;transform:scale(.2)}}
/* FLASH: a luz que atravessa o vidro no instante em que ele nasce */
.flash{{position:absolute;top:-20%;bottom:-20%;width:52%;pointer-events:none;
  left:-60%;opacity:0;transform:skewX(-18deg);
  background:linear-gradient(90deg,transparent,rgba(242,234,217,.30),transparent)}}
/* CURSOR */
#cursor{{position:absolute;left:0;top:0;width:46px;height:46px;
  transform-origin:6px 4px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.85));
  z-index:9}}
</style></head><body class="vega-liquid">
<div class="painel"><div class="escala">{cartoes}</div></div>
<svg id="cursor" viewBox="0 0 24 24">
  <path d="M5 2 L5 20.5 L9.6 16.2 L12.4 22.4 L15.4 21 L12.6 15 L19 14.6 Z"
        fill="#F2EAD9" stroke="#141010" stroke-width="1.2" stroke-linejoin="round"/>
</svg>
<script>
const CLIQUES = {json.dumps(C["cliques"])};      // instante de cada clique, em s
const cartoes = [...document.querySelectorAll('.cartao')];
const cursor  = document.getElementById('cursor');
const CH = {json.dumps(C.get("chegada", .45))};   // quanto antes o cursor chega

const cl  = (x,a,b) => x < a ? a : x > b ? b : x;
const t01 = (x) => cl(x, 0, 1);
const outCubic = x => 1 - Math.pow(1 - t01(x), 3);
const inOutCubic = x => (x = t01(x)) < .5 ? 4*x*x*x : 1 - Math.pow(-2*x + 2, 3)/2;
const outExpo = x => (x = t01(x)) === 1 ? 1 : 1 - Math.pow(2, -9*x);
// mola de verdade: amplitude que decai enquanto oscila. E o overshoot que faz
// a caixa parecer ter massa em vez de so aparecer
const mola = (x, f = 3.1, d = 5.4) =>
  x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.exp(-d*x) * Math.cos(f*Math.PI*x);

function alvoDoCartao(i){{
  const r = cartoes[i].getBoundingClientRect();
  return [r.left + r.width*0.62, r.top + r.height*0.58];
}}

function frame(t){{
  cartoes.forEach((c, i) => {{
    const dt = t - CLIQUES[i];
    const card = c.querySelector('[data-slot=card]');
    if (dt < 0) {{                       // ainda nao nasceu: guarda o lugar
      c.style.opacity = 0;
      c.style.transform = 'translateY(30px) scale(.86)';
      c.style.filter = 'blur(16px)';
      return;
    }}
    const m = mola(dt / .78);
    c.style.opacity = t01(dt / .16).toFixed(3);
    c.style.filter = 'blur(' + (16 * (1 - t01(dt / .26))).toFixed(2) + 'px)';
    c.style.transform =
      'translateY(' + (30 * (1 - m)).toFixed(2) + 'px) ' +
      'scale(' + (0.86 + 0.14 * m).toFixed(4) + ')';

    const rip = c.querySelector('.ripple');
    rip.style.opacity = (0.55 * (1 - t01(dt / .55))).toFixed(3);
    rip.style.transform = 'scale(' + (0.2 + 7.5 * outCubic(dt / .55)).toFixed(2) + ')';

    const fl = c.querySelector('.flash');
    const p = t01((dt - .05) / .55);
    fl.style.opacity = (p > 0 && p < 1 ? 1 : 0);
    fl.style.left = (-60 + 220 * outCubic(p)) + '%';

    const v = c.querySelector('.valor');
    // o total tem curso maior: 38 subindo no mesmo tempo de 1 vira piscada
    const cur = (i === cartoes.length - 1) ? 1.05 : .62;
    v.textContent = Math.round(+v.dataset.alvo * outExpo((dt - .04) / cur));
  }});

  // CURSOR: sai de fora do quadro, encosta em cada cartao um pouco antes do
  // clique e afunda no toque
  let px = -70, py = 1460, pt = -1;
  let alvo = 0;
  for (let i = 0; i < CLIQUES.length; i++) {{
    if (t >= CLIQUES[i] - CH) alvo = i;
  }}
  const [ax, ay] = alvoDoCartao(alvo);
  if (alvo > 0) {{ [px, py] = alvoDoCartao(alvo - 1); pt = CLIQUES[alvo - 1]; }}
  const ini = alvo === 0 ? CLIQUES[0] - CH - .35 : pt + .12;
  const k = inOutCubic((t - ini) / (CLIQUES[alvo] - CH - ini + .0001));
  const x = px + (ax - px) * k, y = py + (ay - py) * k;

  const dtc = t - CLIQUES[alvo];
  const press = dtc > -.09 && dtc < .16
      ? 1 - .16 * Math.sin(Math.PI * t01((dtc + .09) / .25)) : 1;
  // SAIDA: depois do ultimo clique o cursor desce e sai pela borda, senao ele
  // fica dois segundos plantado na tela no fim do loop
  const fim = CLIQUES[CLIQUES.length - 1] + 1.35;
  let sx = x, sy = y, op = 1;
  if (t > fim) {{
    const k2 = inOutCubic((t - fim) / .75);
    sx = x + 120 * k2; sy = y + 320 * k2; op = 1 - t01((t - fim) / .55);
  }}
  cursor.style.opacity = op.toFixed(3);
  cursor.style.transform =
    'translate(' + sx.toFixed(1) + 'px,' + sy.toFixed(1) + 'px) scale(' + press.toFixed(3) + ')';

  // e o total respira uma vez, para o olho terminar nele
  const ult = cartoes[cartoes.length - 1].querySelector('[data-slot=card]');
  const dp = t - (fim + .1);
  const pulso = dp > 0 && dp < 1.1 ? Math.sin(Math.PI * (dp / 1.1)) : 0;
  ult.style.boxShadow = pulso > 0
    ? 'inset 0 1.5px 0 rgba(242,234,217,.60), inset 0 -1.5px 0 rgba(0,0,0,.45),'
      + ' 0 0 ' + (70 * pulso).toFixed(0) + 'px rgba(29,67,184,' + (.42 * pulso).toFixed(3) + '),'
      + ' 0 30px 60px -22px rgba(0,0,0,.95)'
    : '';
}}
window.frame = frame;
frame(0);
</script></body></html>"""


def gerar(nome="volume"):
    C = dict(compor.SLIDES[nome]["card"])
    C["cliques"] = [0.62, 1.48, 2.34, 3.22]
    cen = fundo_sem_painel(nome)
    (AQUI / "_anim.html").write_text(html_anim(C, cen), encoding="utf-8")

    FRAMES.mkdir(exist_ok=True)
    for f in FRAMES.glob("*.png"):
        f.unlink()
    subprocess.run(["node", "captura.js", str(round(DUR * FPS)), str(FPS),
                    str(ESCALA)], cwd=AQUI, check=True)

    saida = AQUI / f"VIDEO-{nome}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(FRAMES / "f%04d.png"),
        "-vf", "scale=1080:1350:flags=lanczos", "-c:v", "libx264",
        "-profile:v", "high", "-crf", "17", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(saida)], check=True, capture_output=True)
    print(f"{saida.name}  {saida.stat().st_size/1024/1024:.1f} MB")
    return saida


if __name__ == "__main__":
    gerar(*(sys.argv[1:] or []))
