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
/* CURSOR: disco de vidro em vez da seta de sistema. A seta era um corpo
   estranho no meio de um painel de vidro; o disco usa a mesma linguagem e
   ainda deixa ver o cartao por baixo. */
#cursor{{position:absolute;left:0;top:0;width:46px;height:46px;
  margin:-23px 0 0 -23px;border-radius:50%;z-index:9;
  border:1.5px solid rgba(242,234,217,.75);
  background:radial-gradient(circle at 35% 30%,rgba(242,234,217,.30),
             rgba(242,234,217,.06) 60%,transparent 72%);
  backdrop-filter:blur(3px) brightness(1.25);
  box-shadow:0 8px 22px rgba(0,0,0,.75),inset 0 1px 0 rgba(255,255,255,.5)}}
#cursor::after{{content:"";position:absolute;left:50%;top:50%;width:5px;height:5px;
  margin:-2.5px 0 0 -2.5px;border-radius:50%;background:#F2EAD9}}
/* rastro: o mesmo disco atrasado alguns quadros, e o que da a leitura de
   movimento continuo num video de 30 quadros */
#rastro{{position:absolute;left:0;top:0;width:46px;height:46px;
  margin:-23px 0 0 -23px;border-radius:50%;z-index:8;
  border:1.5px solid rgba(242,234,217,.20)}}
.valor{{display:inline-block;transform-origin:0% 60%}}
</style></head><body class="vega-liquid">
<div class="painel"><div class="escala">{cartoes}</div></div>
<div id="rastro"></div><div id="cursor"></div>
<script>
const CLIQUES = {json.dumps(C["cliques"])};      // instante de cada clique, em s
const cartoes = [...document.querySelectorAll('.cartao')];
const cursor  = document.getElementById('cursor');
const rastro  = document.getElementById('rastro');
const CH = {json.dumps(C.get("chegada", .45))};   // quanto antes o cursor chega

const cl  = (x,a,b) => x < a ? a : x > b ? b : x;
const t01 = (x) => cl(x, 0, 1);
const outCubic = x => 1 - Math.pow(1 - t01(x), 3);
const inOutCubic = x => (x = t01(x)) < .5 ? 4*x*x*x : 1 - Math.pow(-2*x + 2, 3)/2;
const outExpo = x => (x = t01(x)) === 1 ? 1 : 1 - Math.pow(2, -9*x);
const inOutQuint = x => (x = t01(x)) < .5 ? 16*x*x*x*x*x : 1 - Math.pow(-2*x + 2, 5)/2;
function bezier(x0, y0, x1, y1, k){{
  const cx = (x0 + x1)/2 + Math.abs(y1 - y0) * .34 + 40;   // barriga do arco
  const cy = (y0 + y1)/2;
  const u = 1 - k;
  return [u*u*x0 + 2*u*k*cx + k*k*x1, u*u*y0 + 2*u*k*cy + k*k*y1];
}}
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
    // e o numero so ganha corpo DEPOIS de fechar a contagem: escalar durante
    // a subida embaralha as duas leituras
    const dp2 = dt - (cur + .04);
    const pop = dp2 > 0 && dp2 < .42 ? Math.sin(Math.PI * (dp2 / .42)) : 0;
    v.style.transform = 'scale(' + (1 + .16 * pop).toFixed(4) + ')';
  }});

  // CURSOR: sai de fora do quadro, encosta em cada cartao um pouco antes do
  // clique e afunda no toque
  let px = 540, py = -90, pt = -1;      // entra por cima, no eixo do quadro
  let alvo = 0;
  for (let i = 0; i < CLIQUES.length; i++) {{
    if (t >= CLIQUES[i] - CH) alvo = i;
  }}
  const [ax, ay] = alvoDoCartao(alvo);
  if (alvo > 0) {{ [px, py] = alvoDoCartao(alvo - 1); pt = CLIQUES[alvo - 1]; }}
  const ini = alvo === 0 ? CLIQUES[0] - CH - .55 : pt + .10;
  const k = inOutQuint((t - ini) / (CLIQUES[alvo] - CH - ini + .0001));
  // trajetoria em ARCO: linha reta entre dois cartoes empilhados le como
  // teleporte vertical. O ponto de controle joga a curva para a direita.
  const [x, y] = bezier(px, py, ax, ay, k);

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
  if (window.__ant === undefined) window.__ant = [sx, sy];
  // o rastro persegue a posicao atual com atraso fixo; em quadro a quadro isso
  // equivale a um seguidor amortecido e custa nada
  window.__ant = [window.__ant[0] + (sx - window.__ant[0]) * .34,
                  window.__ant[1] + (sy - window.__ant[1]) * .34];
  rastro.style.opacity = (op * .55).toFixed(3);
  rastro.style.transform = 'translate(' + window.__ant[0].toFixed(1) + 'px,'
    + window.__ant[1].toFixed(1) + 'px) scale(' + (press * 1.22).toFixed(3) + ')';

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
