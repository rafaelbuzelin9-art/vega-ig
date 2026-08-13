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

ROTEIRO. Primeira passada: um clique por cartão, cada um nasce e conta. Segunda
passada: o cursor volta ao primeiro cartão e clica mais três vezes; a cada
clique o minuto da confirmação sobe e o total do mês sobe JUNTO — é a frase da
peça dita em movimento, mexer numa tarefa mexe no mês inteiro.
"""
import base64, json, subprocess, sys
from pathlib import Path

import compor

AQUI = Path(__file__).resolve().parent
FRAMES = AQUI / "_frames"
DUR = 9.0          # segundos
FPS = 30
ESCALA = 2         # captura em 2160x2700 e o ffmpeg reduz

# --- ROTEIRO -------------------------------------------------------------
NASCE = [0.80, 1.85, 2.90, 3.95]        # nascimento de cada cartão
EXTRAS = [5.45, 6.15, 6.85]             # cliques extras, todos no primeiro
# cada minuto a mais na confirmação custa 16h no mês (32 confirmações por dia
# × 30 dias ÷ 60). É a conta que sustenta os dois números subindo juntos.
POR_MINUTO = 16


def roteiro(C):
    """Eventos (instante, valor) por cartão, e as paradas do cursor."""
    ev = [[(NASCE[i], m["alvo"])] for i, m in enumerate(C["metricas"])]
    base_min = C["metricas"][0]["alvo"]
    base_tot = C["metricas"][-1]["alvo"]
    for k, t in enumerate(EXTRAS, start=1):
        ev[0].append((t, base_min + k))
        ev[-1].append((t, base_tot + k * POR_MINUTO))
    paradas = [(t, i) for i, t in enumerate(NASCE)] + [(t, 0) for t in EXTRAS]
    return ev, paradas


def fundo_sem_painel(nome="volume"):
    """Rasteriza o slide sem o painel: é o cenário fixo do vídeo."""
    cfg = dict(compor.SLIDES[nome])
    cfg.pop("card", None)
    compor.render("_cenario", cfg)
    return AQUI / "SLIDE-_cenario.png"


def html_anim(C, cenario):
    eventos, paradas = roteiro(C)
    cartoes = "".join(
        f'<div class="cartao" data-ev=\'{json.dumps(eventos[i])}\'>'
        f'<div data-slot="card" class="{compor.CARD_CLS}">'
        f'<span class="ripple"></span><span class="flash"></span>'
        f'<div data-slot="card-header" class="grid auto-rows-min '
        f'grid-rows-[auto_auto] items-start gap-2 px-6">'
        f'<div data-slot="card-description" class="text-sm text-muted-foreground">'
        f'{m["rot"]}</div>'
        f'<div data-slot="card-title" class="leading-none font-semibold '
        f'text-2xl tabular-nums @[250px]/card:text-3xl">'
        f'<span class="valor">0</span> {m["un"]}'
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
.valor{{display:inline-block;transform-origin:0% 60%}}
/* RIPPLE: o anel que sai de onde o cursor tocou */
.ripple{{position:absolute;left:50%;top:50%;width:40px;height:40px;
  margin:-20px 0 0 -20px;border-radius:50%;pointer-events:none;
  border:2px solid rgba(242,234,217,.55);opacity:0;transform:scale(.2)}}
/* FLASH: a luz que atravessa o vidro no instante em que ele nasce */
.flash{{position:absolute;top:-20%;bottom:-20%;width:52%;pointer-events:none;
  left:-60%;opacity:0;transform:skewX(-18deg);
  background:linear-gradient(90deg,transparent,rgba(242,234,217,.30),transparent)}}
/* CURSOR: disco de vidro, mesma linguagem dos cartões, com rastro atrás */
#cursor{{position:absolute;left:0;top:0;width:46px;height:46px;
  margin:-23px 0 0 -23px;border-radius:50%;z-index:9;
  border:1.5px solid rgba(242,234,217,.78);
  background:radial-gradient(circle at 35% 30%,rgba(242,234,217,.32),
             rgba(242,234,217,.07) 60%,transparent 72%);
  backdrop-filter:blur(3px) brightness(1.25);
  box-shadow:0 8px 22px rgba(0,0,0,.75),inset 0 1px 0 rgba(255,255,255,.5)}}
#cursor::after{{content:"";position:absolute;left:50%;top:50%;width:5px;height:5px;
  margin:-2.5px 0 0 -2.5px;border-radius:50%;background:#F2EAD9}}
#rastro{{position:absolute;left:0;top:0;width:46px;height:46px;
  margin:-23px 0 0 -23px;border-radius:50%;z-index:8;
  border:1.5px solid rgba(242,234,217,.20)}}
</style></head><body class="vega-liquid">
<div class="painel"><div class="escala">{cartoes}</div></div>
<div id="rastro"></div><div id="cursor"></div>
<script>
const PARADAS = {json.dumps(paradas)};   // [instante do clique, cartão alvo]
const cartoes = [...document.querySelectorAll('.cartao')];
const EV = cartoes.map(c => JSON.parse(c.dataset.ev));
const cursor = document.getElementById('cursor');
const rastro = document.getElementById('rastro');
const CH = .10;          // o cursor pousa 0,10s antes do clique
const SAI = {json.dumps(round(EXTRAS[-1] + 1.4, 2))};

const cl  = (x,a,b) => x < a ? a : x > b ? b : x;
const t01 = (x) => cl(x, 0, 1);
const outCubic = x => 1 - Math.pow(1 - t01(x), 3);
const inOutQuint = x => (x = t01(x)) < .5 ? 16*x*x*x*x*x
                                          : 1 - Math.pow(-2*x + 2, 5)/2;
const outExpo = x => (x = t01(x)) === 1 ? 1 : 1 - Math.pow(2, -9*x);
// mola de verdade: amplitude que decai enquanto oscila. É o overshoot que faz
// a caixa parecer ter massa em vez de só aparecer.
const mola = (x, f = 3.1, d = 5.4) =>
  x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.exp(-d*x) * Math.cos(f*Math.PI*x);

function bezier(x0, y0, x1, y1, k){{
  const cx = (x0 + x1)/2 + Math.abs(y1 - y0) * .38 + 60;   // barriga do arco
  const cy = (y0 + y1)/2;
  const u = 1 - k;
  return [u*u*x0 + 2*u*k*cx + k*k*x1, u*u*y0 + 2*u*k*cy + k*k*y1];
}}

function alvoDoCartao(i){{
  const r = cartoes[i].getBoundingClientRect();
  return [r.left + r.width*0.60, r.top + r.height*0.58];
}}

/* posição do cursor no instante t. Fica isolada porque o rastro precisa
   reconstruir o caminho inteiro a cada quadro: como o vídeo é renderizado
   quadro a quadro e não em tempo real, um seguidor com estado dependeria da
   ordem em que os quadros foram desenhados. */
function posicao(t){{
  let ant = [540, -120], t_ant = PARADAS[0][0] - 1.30, alvo = 0;
  for (let k = 0; k < PARADAS.length; k++) {{
    if (t >= PARADAS[k][0]) {{
      alvo = Math.min(k + 1, PARADAS.length - 1);
      ant = alvoDoCartao(PARADAS[k][1]);
      t_ant = PARADAS[k][0];
    }}
  }}
  const chega = PARADAS[alvo][0] - CH;
  const [ax, ay] = alvoDoCartao(PARADAS[alvo][1]);
  // usa TODO o intervalo entre uma parada e a seguinte: com 0,3s para
  // atravessar o quadro, o movimento lia como teleporte
  const k = inOutQuint((t - (t_ant + .05)) / Math.max(.12, chega - t_ant - .05));
  return bezier(ant[0], ant[1], ax, ay, k);
}}

function frame(t){{
  cartoes.forEach((c, i) => {{
    const ev = EV[i];
    const dt = t - ev[0][0];
    if (dt < 0) {{                       // ainda não nasceu: guarda o lugar
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

    // clique MAIS RECENTE deste cartão: o ripple e a contagem partem dele
    let idx = 0;
    for (let j = 0; j < ev.length; j++) if (t >= ev[j][0]) idx = j;
    const dtc = t - ev[idx][0];

    const rip = c.querySelector('.ripple');
    rip.style.opacity = (0.55 * (1 - t01(dtc / .55))).toFixed(3);
    rip.style.transform = 'scale(' + (0.2 + 7.5 * outCubic(dtc / .55)).toFixed(2) + ')';

    const fl = c.querySelector('.flash');
    const p = t01((dt - .05) / .55);
    fl.style.opacity = (p > 0 && p < 1 ? 1 : 0);
    fl.style.left = (-60 + 220 * outCubic(p)) + '%';

    // VALOR: interpola do valor anterior para o do clique atual
    const de = idx === 0 ? 0 : ev[idx - 1][1];
    const para = ev[idx][1];
    // o total tem curso maior: 38 subindo no tempo de 1 vira piscada
    const cur = (i === cartoes.length - 1) ? (idx === 0 ? .95 : .55) : .5;
    const v = c.querySelector('.valor');
    v.textContent = Math.round(de + (para - de) * outExpo((dtc - .04) / cur));
    // e o número só ganha corpo DEPOIS de fechar a contagem: escalar durante
    // a subida embaralha as duas leituras
    const dp = dtc - (cur + .04);
    const pop = dp > 0 && dp < .42 ? Math.sin(Math.PI * (dp / .42)) : 0;
    v.style.transform = 'scale(' + (1 + .16 * pop).toFixed(4) + ')';
  }});

  // CURSOR
  let [x, y] = posicao(t);
  let alvo = 0;
  for (let k = 0; k < PARADAS.length; k++) if (t >= PARADAS[k][0] - .5) alvo = k;
  const dtc = t - PARADAS[alvo][0];
  const press = dtc > -.09 && dtc < .16
      ? 1 - .18 * Math.sin(Math.PI * t01((dtc + .09) / .25)) : 1;

  let op = 1;
  if (t > SAI) {{                        // sai pela borda de baixo
    const k2 = inOutQuint((t - SAI) / .9);
    x += 150 * k2; y += 400 * k2; op = 1 - t01((t - SAI) / .7);
  }}
  cursor.style.opacity = op.toFixed(3);
  cursor.style.transform =
    'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) scale(' + press.toFixed(3) + ')';

  // RASTRO: seguidor amortecido, refeito do zero a cada quadro
  let rx = 540, ry = -120;
  for (let s = 0; s <= t; s += 1/60) {{
    const q = posicao(s);
    rx += (q[0] - rx) * .20; ry += (q[1] - ry) * .20;
  }}
  rastro.style.opacity = (op * .5).toFixed(3);
  rastro.style.transform = 'translate(' + rx.toFixed(1) + 'px,' + ry.toFixed(1)
    + 'px) scale(' + (press * 1.24).toFixed(3) + ')';

  // TOTAL respira uma vez no fim, para o olho terminar nele
  const ult = cartoes[cartoes.length - 1].querySelector('[data-slot=card]');
  const dpz = t - (SAI + .15);
  const pulso = dpz > 0 && dpz < 1.2 ? Math.sin(Math.PI * (dpz / 1.2)) : 0;
  ult.style.boxShadow = pulso > 0
    ? 'inset 0 1.5px 0 rgba(242,234,217,.60), inset 0 -1.5px 0 rgba(0,0,0,.45),'
      + ' 0 0 ' + (80 * pulso).toFixed(0) + 'px rgba(29,67,184,' + (.45 * pulso).toFixed(3) + '),'
      + ' 0 30px 60px -22px rgba(0,0,0,.95)'
    : '';
}}
window.frame = frame;
frame(0);
</script></body></html>"""


def gerar(nome="volume"):
    C = dict(compor.SLIDES[nome]["card"])
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
    print(f"{saida.name}  {saida.stat().st_size/1024/1024:.1f} MB  {DUR}s")
    return saida


if __name__ == "__main__":
    gerar(*(sys.argv[1:] or []))
