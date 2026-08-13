# -*- coding: utf-8 -*-
"""ANIMAÇÃO DO FLUXO DE FOLLOW-UP — reativação de cliente sumido, em beats.

Grafo: CHAT1 → TEMPO (contador de dias) → AGENTE → CHAT2 → AGENDADO.

Roteiro:
  1. A conversa acontece  — pergunta, resposta da atendente, a fuga.
  2. O TEMPO PASSA        — o chat esfria, o NODE DO TEMPO nasce e conta
                            "1 → 12", o relógio fecha uma volta (1 hora do
                            mostrador = 1 dia) e a trilha acende UM PONTO
                            POR DIA.
  3. O agente pensa       — orbe acorda, pontos ciclam, "interesse alto"
                            substitui o pensamento, decide.
  4. A sugestão chega     — chat 2 nasce do header e cresce; o balão da fuga
                            VIAJA e vira a citação; chat 1 colapsa.
  5. Enviado, respondido  — ✓ chega, ✓✓ atrasado azula; cliente responde.
  6. Agendado             — calendário nasce, o último ponto respira na borda.

Suavidade: pops mais longos com translateY, digitação com fade nas pontas,
blur de nascimento mais gentil, portas em fade de 0.4s.
"""
import base64, math, subprocess
from pathlib import Path

import fluxo

AQUI = Path(__file__).resolve().parent
FRAMES = AQUI / "_frames"
DUR = 15.0
FPS = 30
ESCALA = 2

# ---------------------------------------------------------------- amostrar --
def amostrar(curva, n=None, espac=16.0):
    """Pontos equidistantes ao longo da cúbica (por comprimento de arco).
    n força a QUANTIDADE — na aresta do tempo, 12 pontos = 12 dias."""
    bruto = [fluxo.ponto(curva, t / 400) for t in range(401)]
    compr = [0.0]
    for a, b in zip(bruto, bruto[1:]):
        compr.append(compr[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    total = compr[-1]
    passo = total / (n - 1) if n else espac
    alvos = [i * passo for i in range(int(total / passo) + 1)]
    pts, j = [], 0
    for alvo in alvos:
        while j < 399 and compr[j + 1] < alvo:
            j += 1
        f = (alvo - compr[j]) / max(compr[j + 1] - compr[j], 1e-6)
        pts.append((bruto[j][0] + (bruto[j + 1][0] - bruto[j][0]) * f,
                    bruto[j][1] + (bruto[j + 1][1] - bruto[j][1]) * f))
    return pts

def reta(p0, p1, espac=16.0):
    n = max(2, int(math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / espac) + 1)
    return [(p0[0] + (p1[0] - p0[0]) * i / (n - 1),
             p0[1] + (p1[1] - p0[1]) * i / (n - 1)) for i in range(n)]

T_ENTRA = reta((-24, fluxo.P_C1_IN[1]), fluxo.P_C1_IN)
T_1T    = amostrar(fluxo.C_1T, n=fluxo.GAP_DIAS)          # 12 pontos = 12 dias
T_TA    = amostrar(fluxo.C_TA)
T_A2    = amostrar(fluxo.C_A2)
T_2D    = amostrar(fluxo.C_2D)
T_SAI   = reta(fluxo.P_AD_OUT, (1098, fluxo.P_AD_OUT[1]))

def circulos(nome, pts):
    return "".join(
        f'<circle class="td {nome}" data-i="{i}" cx="{x:.1f}" cy="{y:.1f}" r="2.6"/>'
        f'<circle class="tg {nome}" data-i="{i}" cx="{x:.1f}" cy="{y:.1f}" r="7"/>'
        for i, (x, y) in enumerate(pts))


# ---------------------------------------------------------------- documento --
def html_anim():
    import json
    fonte = base64.b64encode(fluxo.FONTE.read_bytes()).decode()
    C1, TP, AG, C2, AD = (fluxo.CHAT1, fluxo.TEMPO, fluxo.AGENT,
                          fluxo.CHAT2, fluxo.AGEND)
    top = fluxo.PAINEL_TOP

    json_t1 = json.dumps([[round(x, 1), round(y, 1)] for x, y in T_1T])
    json_tta = json.dumps([[round(x, 1), round(y, 1)] for x, y in T_TA])
    json_ta2 = json.dumps([[round(x, 1), round(y, 1)] for x, y in T_A2])
    json_t2d = json.dumps([[round(x, 1), round(y, 1)] for x, y in T_2D])
    gap = fluxo.GAP_DIAS
    # match cut: o balão da FUGA (terceiro do chat 1) → citação do chat 2
    b0x, b0y, b0w = C1["x"] + 26, C1["y"] + 262, 400
    b1x, b1y, b1w = C2["x"] + 26, C2["y"] + 98, C2["w"] - 52
    c1h = C1["h"]

    svg = (f'<svg width="{fluxo.PW}" height="{fluxo.PH}" '
           f'viewBox="0 0 {fluxo.PW} {fluxo.PH}">'
           + circulos("e0", T_ENTRA) + circulos("e1", T_1T)
           + circulos("e2", T_TA) + circulos("e3", T_A2)
           + circulos("e4", T_2D) + circulos("e5", T_SAI)
           + "".join(f'<circle class="porta" data-k="{k}" cx="{x}" cy="{y}" r="7"/>'
                     for k, (x, y) in enumerate(fluxo.PORTAS))
           + '<circle id="pulso-h" r="16" fill="rgba(242,234,217,.16)"/>'
           + '<circle id="pulso" r="6" fill="#F2EAD9"/>'
           + '</svg>')

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="shadcn-ref/saida.css">
<style>
@font-face{{font-family:'Jost';src:url(data:font/woff2;base64,{fonte})
  format('woff2');font-weight:100 900}}
html,body{{margin:0;width:1080px;height:1350px;overflow:hidden;
  font-family:'Jost';background:#050505 url('SLIDE-_cenario-fluxo.png') no-repeat 0 0;
  background-size:1080px 1350px}}
*{{font-family:'Jost';box-sizing:border-box}}
#painel{{position:absolute;left:0;top:{top}px;width:{fluxo.PW}px;height:{fluxo.PH}px}}

.chat{{position:absolute;z-index:2;padding:24px 26px;display:flex;
  flex-direction:column;gap:16px;overflow:hidden}}
.chat>*{{flex:none}}
.chd{{display:flex;align-items:center;gap:12px;padding-bottom:14px;
  border-bottom:1px solid rgba(231,220,198,.10)}}
.avt{{width:30px;height:30px;border-radius:50%;flex:none;
  background:radial-gradient(circle at 34% 30%,rgba(242,234,217,.55),rgba(242,234,217,.10) 60%);
  border:1px solid rgba(231,220,198,.35)}}
.nome{{font-size:24px;font-weight:400;color:#F2EAD9;letter-spacing:.02em}}
.hora{{margin-left:auto;font-size:19px;font-weight:300;
  color:rgba(231,220,198,.55);letter-spacing:.06em}}
.bin{{align-self:flex-start;max-width:88%;padding:16px 22px;font-size:26px;
  font-weight:300;line-height:1.3;color:rgba(242,234,217,.94);
  background:rgba(242,234,217,.07);border:1px solid rgba(231,220,198,.14);
  border-radius:20px;border-bottom-left-radius:6px}}
.bout{{align-self:flex-end;max-width:88%;padding:16px 22px;font-size:26px;
  font-weight:300;line-height:1.3;color:rgba(242,234,217,.94);
  background:rgba(29,67,184,.18);border:1px solid rgba(90,125,230,.30);
  border-radius:20px;border-bottom-right-radius:6px}}
.hist{{font-size:22px;font-weight:300;color:rgba(231,220,198,.60);
  padding:8px 16px;border-left:3px solid rgba(231,220,198,.35);
  background:rgba(242,234,217,.045);border-radius:0 12px 12px 0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.hq{{display:block;font-size:15px;letter-spacing:.14em;
  color:rgba(231,220,198,.45);margin-bottom:3px;text-transform:uppercase}}
.sugg{{align-self:stretch;padding:16px 22px;font-size:25px;font-weight:300;
  line-height:1.3;color:rgba(242,234,217,.94);border-radius:18px;
  background:rgba(29,67,184,.14);border:1.5px dashed rgba(90,125,230,.55)}}
.stag{{font-size:15px;font-weight:400;letter-spacing:.14em;
  color:rgba(160,180,240,.90);margin-bottom:8px;white-space:nowrap}}
.acao{{font-size:21px;font-weight:300;color:rgba(231,220,198,.60);
  letter-spacing:.03em;padding-left:6px}}
.vv i{{font-style:normal}}

.quad{{position:absolute;z-index:2;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:10px;padding:18px}}
.icone{{width:132px;height:132px}}
/* o orbe e o anel de processamento que gira enquanto o agente pensa */
.orb{{position:relative;width:132px;height:132px;flex:none}}
.anel{{position:absolute;left:-14px;top:-14px;opacity:0;z-index:2;
  transform-origin:50% 50%}}
.qrot{{font-size:20px;font-weight:400;letter-spacing:.24em;
  color:rgba(231,220,198,.80);display:flex;align-items:center;gap:10px}}
.qdet{{font-size:19px;font-weight:300;color:rgba(231,220,198,.50);
  letter-spacing:.06em}}
.tval{{font-size:64px;font-weight:300;color:#F2EAD9;line-height:1;
  font-variant-numeric:tabular-nums;letter-spacing:-.03em}}
.vivo{{width:9px;height:9px;border-radius:50%;background:#F2EAD9;flex:none;
  box-shadow:0 0 8px rgba(242,234,217,.9),0 0 20px rgba(242,234,217,.45)}}
.pensa{{display:flex;gap:9px;align-items:center;height:12px}}
.pensa i{{width:9px;height:9px;border-radius:50%;background:#F2EAD9;display:block}}

.dig{{display:flex;gap:8px;align-items:center;padding:18px 22px;
  align-self:flex-start;background:rgba(242,234,217,.07);
  border:1px solid rgba(231,220,198,.14);border-radius:20px;
  border-bottom-left-radius:6px}}
.dig.dir{{align-self:flex-end;background:rgba(29,67,184,.18);
  border:1px solid rgba(90,125,230,.30);
  border-radius:20px;border-bottom-right-radius:6px}}
.dig i{{width:9px;height:9px;border-radius:50%;background:rgba(242,234,217,.8);
  display:block}}

.rotulo{{position:absolute;font-size:23px;font-weight:300;z-index:3;
  letter-spacing:.04em;color:rgba(231,220,198,.85);white-space:nowrap;
  transform:translate(-50%,-50%);padding:8px 20px;border-radius:999px;
  background:rgba(8,8,8,.82);border:1px solid rgba(231,220,198,.15)}}
svg{{position:absolute;left:0;top:0;z-index:1}}
.rel{{flex:none;display:block;position:static}}
.td{{fill:rgba(242,234,217,.92)}}
.tg{{fill:rgba(242,234,217,.15)}}
.porta{{fill:#0A0A0A;stroke:rgba(242,234,217,.85);stroke-width:2.5}}

#veu1{{position:absolute;z-index:3;border-radius:28px;background:#050505;
  pointer-events:none}}
#clone{{position:absolute;z-index:5;padding:16px 22px;font-size:26px;
  font-weight:300;line-height:1.3;color:rgba(242,234,217,.94);
  background:rgba(20,18,14,.92);border:1px solid rgba(231,220,198,.20);
  border-radius:20px;transform-origin:0 0;white-space:nowrap;overflow:hidden}}
#halo{{position:absolute;z-index:1;border-radius:50%;pointer-events:none;
  background:radial-gradient(circle,rgba(242,234,217,.16),transparent 65%)}}

body.vega-liquid [data-slot=card].hero{{
  box-shadow:inset 0 1.5px 0 rgba(242,234,217,.85),
    inset 0 -1.5px 0 rgba(0,0,0,.45),
    inset 0 0 52px rgba(242,234,217,.09),
    0 0 46px rgba(242,234,217,.07),
    0 30px 60px -22px rgba(0,0,0,.95) !important}}
</style></head><body class="vega-liquid">
<div id="painel">
{svg}
<div data-slot="card" class="chat" id="chat1" style="left:{C1['x']}px;top:{C1['y']}px;
     width:{C1['w']}px;height:{C1['h']}px">
  <div class="chd"><span class="avt"></span><span class="nome">Cliente</span>
    <span class="hora">{fluxo.CHAT1_HORA}</span></div>
  <div class="dig" id="dig1a"><i></i><i></i><i></i></div>
  <div class="bin" id="bolha1">{fluxo.CHAT1_MSG1}</div>
  <div class="dig dir" id="dig1o"><i></i><i></i><i></i></div>
  <div class="bout" id="bolha1o">{fluxo.ATEND_MSG}</div>
  <div class="dig" id="dig1b"><i></i><i></i><i></i></div>
  <div class="bin" id="bolha1b">{fluxo.CHAT1_MSG2}</div>
</div>
<div id="veu1" style="left:{C1['x']}px;top:{C1['y']}px;width:{C1['w']}px;
     height:{C1['h']}px;opacity:0"></div>

<div data-slot="card" class="quad" id="tempo" style="left:{TP['x']}px;top:{TP['y']}px;
     width:{TP['w']}px;height:{TP['h']}px">
  <svg class="rel" width="46" height="46" viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="9.5" fill="none"
      stroke="rgba(242,234,217,.55)" stroke-width="1.6"/>
    <line id="rh" x1="12" y1="12" x2="12" y2="7.4" stroke="#F2EAD9"
      stroke-width="1.9" stroke-linecap="round" transform="rotate(-60 12 12)"/>
    <line id="rm" x1="12" y1="12" x2="12" y2="5.4" stroke="rgba(242,234,217,.8)"
      stroke-width="1.5" stroke-linecap="round" transform="rotate(60 12 12)"/>
    <circle cx="12" cy="12" r="1.4" fill="#F2EAD9"/>
  </svg>
  <div class="tval" id="dias">1</div>
  <div class="qdet">dias no vácuo</div>
</div>

<div id="halo" style="left:{AG['x'] + AG['w']/2 - 130}px;top:{AG['y'] + 40}px;
     width:260px;height:260px;opacity:0"></div>
<div data-slot="card" class="quad" id="agente" style="left:{AG['x']}px;top:{AG['y']}px;
     width:{AG['w']}px;height:{AG['h']}px">
  <div class="orb">
    <img class="icone" id="ic-agente" src="icone_agente_alfa.png">
    <svg class="anel" id="anel" width="160" height="160" viewBox="0 0 160 160">
      <circle cx="80" cy="80" r="72" fill="none"
        stroke="rgba(242,234,217,.60)" stroke-width="2.5"
        stroke-linecap="round" stroke-dasharray="112 341"/>
    </svg>
  </div>
  <div class="qrot"><span class="vivo" id="vivo"></span>AGENTE</div>
  <div class="pensa" id="pensa"><i></i><i></i><i></i></div>
  <div class="qdet" id="razao" style="margin-top:-22px">{fluxo.RAZAO}</div>
</div>

<div data-slot="card" class="chat" id="chat2" style="left:{C2['x']}px;top:{C2['y']}px;
     width:{C2['w']}px;height:{C2['h']}px">
  <div class="chd"><span class="avt"></span><span class="nome">Cliente</span>
    <span class="hora">{fluxo.CHAT2_HORA}</span></div>
  <div class="hist" id="hist"><span class="hq">{fluxo.HIST_TAG}</span>
    {fluxo.HIST_MSG}</div>
  <div class="sugg" id="sugg">
    <div class="stag">{fluxo.SUGG_TAG}</div>
    {fluxo.SUGG_MSG}
  </div>
  <div class="acao" id="acao">a atendente revisou e enviou
    <span class="vv"><i id="v1">✓</i><i id="v2">✓</i></span></div>
  <div class="dig" id="dig2"><i></i><i></i><i></i></div>
  <div class="bin" id="bolha2">{fluxo.REPLY_MSG}</div>
</div>

<div data-slot="card" class="quad" id="agend" style="left:{AD['x']}px;top:{AD['y']}px;
     width:{AD['w']}px;height:{AD['h']}px">
  <img class="icone" id="ic-agend" src="icone_agendado_alfa.png">
  <div class="qrot">AGENDADO</div>
  <div class="qdet">{fluxo.AGEND_DET}</div>
</div>

<div class="rotulo" id="pil2" style="left:{fluxo.ROTULOS[0]['em'][0]:.0f}px;
     top:{fluxo.ROTULOS[0]['em'][1]:.0f}px">{fluxo.ROTULOS[0]['txt']}</div>

<div id="clone">{fluxo.HIST_MSG}</div>
</div>

<script>
// ---------- utilidades (tudo função de t: nenhum estado entre quadros) ----
const outExpo = x => x<=0?0 : x>=1?1 : 1-Math.pow(2,-10*x);
const inOutQ  = x => x<.5 ? 16*x**5 : 1-Math.pow(-2*x+2,5)/2;
const clamp01 = x => x<0?0 : x>1?1 : x;
const mola = x => x<=0?0 : x>=1?1 : 1 - Math.exp(-5.4*x)*Math.cos(3.1*Math.PI*x);
const seg = (t,a,b) => clamp01((t-a)/(b-a));
const $ = id => document.getElementById(id);

function nasce(el, p){{
  el.style.opacity = String(clamp01(p*3));
  const m = mola(p);
  el.style.transform = `translateY(${{26*(1-m)}}px) scale(${{.88+.12*m}})`;
  el.style.filter = `blur(${{10*(1-clamp01(p*1.8))}}px)`;
}}

const T1  = {json_t1};
const TTA = {json_tta};
const TA2 = {json_ta2};
const T2D = {json_t2d};

function trilha(nome, p){{
  const ds = document.querySelectorAll('.td.'+nome);
  const gs = document.querySelectorAll('.tg.'+nome);
  const n = ds.length, vis = Math.floor(p*n + 1e-6);
  ds.forEach((d,i)=>{{ d.style.opacity = i<vis? '1':'0'; }});
  gs.forEach((g,i)=>{{ g.style.opacity = i<vis? '1':'0'; }});
}}
function pulsoEm(pts, p){{
  const i = Math.min(pts.length-1.001, p*(pts.length-1));
  const j = Math.floor(i), f = i-j;
  const x = pts[j][0]+(pts[j+1][0]-pts[j][0])*f;
  const y = pts[j][1]+(pts[j+1][1]-pts[j][1])*f;
  $('pulso').setAttribute('cx',x);  $('pulso').setAttribute('cy',y);
  $('pulso-h').setAttribute('cx',x);$('pulso-h').setAttribute('cy',y);
  $('pulso').style.opacity='1'; $('pulso-h').style.opacity='1';
}}
function pulsoSome(){{ $('pulso').style.opacity='0'; $('pulso-h').style.opacity='0'; }}

// digitação com fade nas pontas (suave, sem corte seco)
function digita(id, p, t){{
  const el = $(id);
  const ramp = Math.min(1, p*7, (1-p)*7);
  el.style.display = (p>0 && p<1)? 'flex':'none';
  if (p>0 && p<1){{
    el.style.opacity = String(ramp);
    el.querySelectorAll('i').forEach((n,k)=>{{
      n.style.opacity = .25+.75*Math.abs(Math.sin((t*4.2-k*.5)*Math.PI/2));
    }});
  }}
}}
// pop suave: escala + subida + fade na mesma curva
function pop(id, p){{
  const el = $(id);
  el.style.display = p>0? 'block':'none';
  const e = outExpo(p);
  el.style.opacity = String(e);
  el.style.transform = `translateY(${{10*(1-e)}}px) scale(${{.90+.10*e}})`;
}}

const B0 = {{x:{b0x}, y:{b0y}, w:{b0w}}};
const B1 = {{x:{b1x}, y:{b1y}, w:{b1w}}};
const C1H = {c1h};

// ---------- o roteiro ------------------------------------------------------
window.frame = function(t){{
  // portas nascem COM seus nós, em fade longo
  // ordem: c1-in, c1-out, tp-in, tp-out, ag-in, ag-out, c2-in, c2-out, ad-in, ad-out
  const PORTA_T = [.45, .45, 3.0, 3.0, .7, .7, 8.35, 11.1, 12.4, 12.4];
  document.querySelectorAll('.porta').forEach(p=>{{
    p.style.opacity = String(seg(t, PORTA_T[+p.dataset.k], PORTA_T[+p.dataset.k]+.4));
  }});

  // BEAT 1 — a conversa acontece: pergunta, resposta da atendente, fuga
  nasce($('chat1'), seg(t, .25, 1.05));
  trilha('e0', seg(t, .0, .3));
  digita('dig1a', seg(t, .70, 1.20), t);
  pop('bolha1', seg(t, 1.20, 1.60));
  digita('dig1o', seg(t, 1.55, 2.05), t);
  pop('bolha1o', seg(t, 2.05, 2.45));
  digita('dig1b', seg(t, 2.40, 2.90), t);
  pop('bolha1b', seg(t, 2.90, 3.30));

  // BEAT 2 — o tempo passa: o node do TEMPO nasce e conta; o chat esfria
  nasce($('tempo'), seg(t, 3.0, 3.8));
  const pf = seg(t, 3.3, 5.3);
  $('veu1').style.opacity = String(.42*outExpo(pf));
  const pc = outExpo(seg(t, 3.5, 5.4));
  $('dias').textContent = Math.max(1, Math.round({gap}*pc));
  $('rh').setAttribute('transform', `rotate(${{-60+360*pc}} 12 12)`);
  $('rm').setAttribute('transform', `rotate(${{60+360*{gap}*pc}} 12 12)`);
  trilha('e1', pc);

  // BEAT 3 — o agente pensa e conclui
  nasce($('agente'), seg(t, .45, 1.25));
  const pv0 = seg(t, 5.55, 6.10);
  if (pv0>0 && pv0<1) pulsoEm(TTA, inOutQ(pv0));
  trilha('e2', inOutQ(pv0));
  const pw = seg(t, 6.05, 6.55);
  $('halo').style.opacity = String(pw);
  $('agente').classList.toggle('hero', t>=6.05);
  $('vivo').style.opacity = t<6.05? '.25'
      : String(.45+.55*Math.abs(Math.sin((t-6.05)*2.6)));
  const think = t>=6.3 && t<7.7;
  $('pensa').querySelectorAll('i').forEach((el,k)=>{{
    el.style.opacity = !think? String(.18*(1-seg(t,7.7,7.95)))
        : String(.18+.82*Math.abs(Math.sin((t*3.4-k*.42)*Math.PI/2)));
  }});
  // pensando: o anel gira ao redor do orbe e o orbe respira
  $('anel').style.opacity = String(Math.min(seg(t,6.3,6.6), 1-seg(t,7.55,7.85)));
  $('anel').style.transform = `rotate(${{(t-6.3)*265}}deg)`;
  $('ic-agente').style.transform = think?
      `scale(${{1+.045*Math.sin((t-6.3)*5.2)}})` : 'scale(1)';
  $('razao').style.opacity = String(seg(t, 7.7, 8.05));
  const dec = seg(t, 8.0, 8.35);
  if (dec>0 && dec<1) $('agente').style.transform +=
      ` scale(${{1+.05*Math.sin(dec*Math.PI)}})`;

  // pulso desce a aresta da sugestão
  const pv = seg(t, 8.2, 9.0);
  if (pv>0 && pv<1) pulsoEm(TA2, inOutQ(pv));
  else if (t>=6.10) pulsoSome();
  trilha('e3', inOutQ(pv));
  const pp2 = seg(t, 8.6, 9.0);
  $('pil2').style.opacity = String(outExpo(pp2));

  // BEAT 4 — chat 2 nasce do header e cresce; match cut do histórico
  nasce($('chat2'), seg(t, 9.0, 9.8));
  const h2 = 100
    + 82*inOutQ(seg(t, 9.55, 9.85))
    + 136*inOutQ(seg(t, 9.95, 10.45))
    + 46*inOutQ(seg(t, 10.65, 10.90))
    + 104*inOutQ(seg(t, 11.55, 11.90));
  $('chat2').style.height = h2+'px';
  const pm = seg(t, 9.2, 9.85);
  if (pm>0 && pm<1){{
    const e = inOutQ(pm);
    const x = B0.x+(B1.x-B0.x)*e, y = B0.y+(B1.y-B0.y)*e - 40*Math.sin(e*Math.PI);
    const cl = $('clone');
    cl.style.display='block';
    cl.style.left=x+'px'; cl.style.top=y+'px';
    cl.style.width=(B0.w+(B1.w-B0.w)*e)+'px';
    cl.style.fontSize=(26-4*e)+'px';
    cl.style.opacity=String(.95-.30*e);
  }} else $('clone').style.display='none';
  $('hist').style.opacity = String(seg(t, 9.78, 9.98));
  const pcol = seg(t, 9.3, 9.95);
  const h1 = C1H-(C1H-100)*inOutQ(pcol);
  $('chat1').style.height = h1+'px';
  $('veu1').style.height = h1+'px';
  if (pcol>0){{
    ['bolha1','bolha1o','bolha1b'].forEach(id=>
      $(id).style.opacity=String(Math.max(0,1-pcol*1.6)));
    $('veu1').style.opacity=String(.42*(1-inOutQ(pcol)));
  }}
  const ps = seg(t, 10.0, 10.5);
  $('sugg').style.opacity = ps>0? '1':'0';
  $('sugg').style.clipPath = `inset(0 ${{(1-outExpo(ps))*100}}% 0 0 round 18px)`;

  // BEAT 5 — enviado (✓ ✓✓ azul), cliente digita e responde
  $('acao').style.opacity = String(seg(t, 10.65, 10.95));
  $('v1').style.opacity = String(seg(t, 10.95, 11.10));
  $('v2').style.opacity = String(seg(t, 11.35, 11.50));
  const azul = t>=11.35;
  $('v1').style.color = azul? 'rgba(120,160,255,.95)':'rgba(231,220,198,.60)';
  $('v2').style.color = 'rgba(120,160,255,.95)';
  digita('dig2', seg(t, 11.65, 12.25), t);
  pop('bolha2', seg(t, 12.25, 12.65));

  // BEAT 6 — agendado
  const pv2 = seg(t, 12.75, 13.25);
  if (pv2>0 && pv2<1) pulsoEm(T2D, inOutQ(pv2));
  else if (t>=9.0) pulsoSome();
  trilha('e4', inOutQ(pv2));
  nasce($('agend'), seg(t, 13.25, 13.95));
  const pi = seg(t, 13.25, 13.85);
  $('ic-agend').style.transform = `scale(${{1.15-.15*mola(pi)}})`;
  $('ic-agend').style.filter = `brightness(${{1.4-.4*outExpo(pi)}})`;
  trilha('e5', seg(t, 13.9, 14.4));
  if (t>14.4){{
    const ult = document.querySelectorAll('.tg.e5');
    const g = ult[ult.length-1];
    if (g) g.setAttribute('r', String(7+3*Math.abs(Math.sin((t-14.4)*2.2))));
  }}
}};
window.frame(0);
</script></body></html>"""


def montar():
    fluxo.icone_alfa("icone_agente")
    fluxo.icone_alfa("icone_agendado")
    print("cenário (fundo + headline, sem painel)…")
    fluxo.render("_cenario-fluxo", com_painel=False)

    (AQUI / "_anim.html").write_text(html_anim(), encoding="utf-8")

    FRAMES.mkdir(exist_ok=True)
    for f in FRAMES.glob("*.png"):
        f.unlink()
    n = int(DUR * FPS)
    print(f"captura: {n} quadros a {FPS}fps, escala {ESCALA}x…")
    subprocess.run(["node", "captura.js", str(n), str(FPS), str(ESCALA)],
                   cwd=AQUI, check=True)
    print("ffmpeg…")
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS),
                    "-i", str(FRAMES / "f%04d.png"),
                    "-vf", "scale=1080:1350:flags=lanczos",
                    "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart",
                    str(AQUI / "VIDEO-followup.mp4")],
                   check=True, capture_output=True)
    print("VIDEO-followup.mp4 pronto")


def prancha():
    """Instantes-chave em grade: julgar pelo quadro, não pelo play."""
    from PIL import Image
    instantes = [1.4, 2.7, 4.2, 5.5, 7.0, 9.6, 10.8, 14.2]
    tiles = []
    for t in instantes:
        subprocess.run(["ffmpeg", "-y", "-ss", str(t), "-i",
                        str(AQUI / "VIDEO-followup.mp4"), "-frames:v", "1",
                        str(AQUI / "_chk" / f"fx_{t}.png")],
                       check=True, capture_output=True)
        tiles.append(AQUI / "_chk" / f"fx_{t}.png")
    TW = 540
    ims = [Image.open(p).resize((TW, 675), Image.LANCZOS) for p in tiles]
    board = Image.new("RGB", (TW * 4 + 30 * 5, 675 * 2 + 30 * 3), "#101010")
    for k, im in enumerate(ims):
        x = 30 + (k % 4) * (TW + 30)
        y = 30 + (k // 4) * (675 + 30)
        board.paste(im, (x, y))
    board.save(AQUI / "PRANCHA-followup-anim.png")
    print("PRANCHA-followup-anim.png pronta")


if __name__ == "__main__":
    montar()
    prancha()
