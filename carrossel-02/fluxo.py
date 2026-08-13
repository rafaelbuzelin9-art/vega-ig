# -*- coding: utf-8 -*-
"""FLUXO — slide de nó/editor: o agente de follow-up rodando.

v2: os nós das pontas viraram CENAS DE CHAT reais (caso real do CRM,
anonimizado: cliente adia na sexta 22h18, equipe retoma na segunda 11h35,
consulta confirmada) e o meio virou nós QUADRADOS com ícone gerado no
Higgsfield. A atendente conduz a conversa; o agente só pensa e deixa o
texto pronto.

Regras herdadas do júri:
  · nenhuma linha contínua fina — todo conector é trilha de pontos redondos;
  · luz nunca ATRÁS dos cartões de vidro — conectores correm entre nós;
  · Creme #F2EAD9 sempre, branco puro nunca.
"""
import base64, subprocess, sys
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).resolve().parent
DS = AQUI.parent / "design-system"
FONTE = DS / "assets" / "jost-variable-latin.woff2"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H = 1080, 1350

PAINEL_TOP = 430
PW, PH = 1080, 920

def icone_alfa(nome):
    """Converte o PNG do Higgsfield (glow sobre preto) em alfa real.
    mix-blend-mode não atravessa o isolation:isolate do cartão de vidro,
    então o preto vira transparência de verdade: alfa = canal máximo."""
    src = AQUI / f"{nome}.png"
    dst = AQUI / f"{nome}_alfa.png"
    if dst.exists() and dst.stat().st_mtime > src.stat().st_mtime:
        return
    im = Image.open(src).convert("RGB")
    px = im.load()
    out = Image.new("RGBA", im.size)
    po = out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            a = max(r, g, b)
            if a < 8:
                po[x, y] = (0, 0, 0, 0)
            else:
                # desfaz a pré-multiplicação pelo preto: cor = canal/alfa
                po[x, y] = (min(255, r * 255 // a), min(255, g * 255 // a),
                            min(255, b * 255 // a), a)
    out.save(dst)

# ---------------------------------------------------------------- geometria --
# grafo: CHAT1 → TEMPO (contador de dias) → AGENTE → CHAT2 → AGENDADO
CHAT1 = dict(x=64,  y=0,   w=490, h=336)
TEMPO = dict(x=654, y=16,  w=206, h=180)
AGENT = dict(x=784, y=268, w=210, h=250)
CHAT2 = dict(x=64,  y=424, w=520, h=468)
AGEND = dict(x=664, y=662, w=206, h=226)

def cubica(p0, p3, modo, r=110):
    (x0, y0), (x3, y3) = p0, p3
    if modo == "h":            # lateral → lateral, indo pra direita
        return (p0, (x0 + r, y0), (x3 - r, y3), p3)
    if modo == "hl":           # lateral → lateral, indo pra ESQUERDA
        return (p0, (x0 - r, y0), (x3 + r, y3), p3)
    if modo == "vh":           # sai por baixo → entra pela lateral direita
        return (p0, (x0, y0 + r), (x3 + r, y3), p3)
    return (p0, (x0, y0 + r), (x3, y3 - r), p3)   # "vv": baixo → topo

def path(c):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = c
    return f"M {x0} {y0} C {x1} {y1}, {x2} {y2}, {x3} {y3}"

def ponto(c, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = c
    u = 1 - t
    return (u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3,
            u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3)

P_C1_IN  = (CHAT1["x"], CHAT1["y"] + 118)
P_C1_OUT = (CHAT1["x"] + CHAT1["w"], CHAT1["y"] + 118)
P_TP_IN  = (TEMPO["x"], TEMPO["y"] + TEMPO["h"] * .5)
P_TP_OUT = (TEMPO["x"] + TEMPO["w"] * .5, TEMPO["y"] + TEMPO["h"])
P_AG_IN  = (AGENT["x"] + AGENT["w"] * .5, AGENT["y"])
P_AG_OUT = (AGENT["x"], AGENT["y"] + AGENT["h"] * .5)
P_C2_IN  = (CHAT2["x"] + CHAT2["w"], CHAT2["y"] + 66)
P_C2_OUT = (CHAT2["x"] + CHAT2["w"], CHAT2["y"] + CHAT2["h"] - 66)
P_AD_IN  = (AGEND["x"], AGEND["y"] + AGEND["h"] * .5)
P_AD_OUT = (AGEND["x"] + AGEND["w"], AGEND["y"] + AGEND["h"] * .5)

C_1T = cubica(P_C1_OUT, P_TP_IN, "h", 56)      # a aresta dos DIAS
C_TA = cubica(P_TP_OUT, P_AG_IN, "vv", 46)
C_A2 = cubica(P_AG_OUT, P_C2_IN, "hl", 110)
C_2D = cubica(P_C2_OUT, P_AD_IN, "h", 56)

E_IN  = f"M -24 {P_C1_IN[1]} L {P_C1_IN[0]} {P_C1_IN[1]}"
E_OUT = f"M {P_AD_OUT[0]} {P_AD_OUT[1]} L 1098 {P_AD_OUT[1]}"

ARESTAS = [
    dict(d=E_IN), dict(d=path(C_1T)), dict(d=path(C_TA)),
    dict(d=path(C_A2)), dict(d=path(C_2D)), dict(d=E_OUT),
]
# relógio do node do tempo: parado em 10h10 no still; no vídeo os ponteiros
# varrem o mostrador enquanto os dias contam (1 hora do mostrador = 1 dia)
REL_SVG = (
    '<svg class="rel" width="46" height="46" viewBox="0 0 24 24">'
    '<circle cx="12" cy="12" r="9.5" fill="none" '
    'stroke="rgba(242,234,217,.55)" stroke-width="1.6"/>'
    '<line id="rh" x1="12" y1="12" x2="12" y2="7.4" stroke="#F2EAD9" '
    'stroke-width="1.9" stroke-linecap="round" transform="rotate(-60 12 12)"/>'
    '<line id="rm" x1="12" y1="12" x2="12" y2="5.4" stroke="rgba(242,234,217,.8)" '
    'stroke-width="1.5" stroke-linecap="round" transform="rotate(60 12 12)"/>'
    '<circle cx="12" cy="12" r="1.4" fill="#F2EAD9"/></svg>')

ROTULOS = [
    dict(txt="sugestão pronta", em=ponto(C_A2, .50)),
]
PORTAS = [P_C1_IN, P_C1_OUT, P_TP_IN, P_TP_OUT, P_AG_IN, P_AG_OUT,
          P_C2_IN, P_C2_OUT, P_AD_IN, P_AD_OUT]
# pulso: a conversa parada sendo puxada PRA DENTRO do contador de dias
PULSO = ponto(C_1T, .80)

# ---------------------------------------------------------------- conteúdo --
# REATIVAÇÃO DE CLIENTE SUMIDO. Padrões reais do CRM: o interesse ("quanto
# fica"), a fuga clássica ("vou ver e te falo" — literal nas conversas) e o
# "perguntou valores há 12 dias e parou de responder" da própria proposta.
# Copy fechada no júri de 13/08 (5 lentes): P9 com a dúvida confirmada (4
# juízes), P5 "sugestão" (4), P7 ecoando o "ver certinho" da citação (3),
# P2 morna com a elipse coberta (3), P8 com artigo (gramática).
GAP_DIAS = 12
CHAT1_HORA = "sexta · 15h40"
CHAT1_MSG1 = "Quanto fica a avaliação?"
ATEND_MSG = "Oi! Te mandei os valores"
CHAT1_MSG2 = "Vou ver certinho e te falo"
CHAT2_HORA = "quarta · 8h03"
HIST_TAG = "SEXTA · CLIENTE"
HIST_MSG = "vou ver certinho e te falo…"
SUGG_TAG = "AGENTE → ATENDENTE · SÓ A EQUIPE VÊ"
SUGG_MSG = "Oi! Conseguiu ver certinho? Qualquer dúvida, tô por aqui"
REPLY_MSG = "Que bom que chamou! Fiquei na dúvida mesmo. Consigo marcar?"
AGEND_DET = "quinta · 10h20"
RAZAO = "interesse alto"

CHAT1_HTML = f"""
<div data-slot="card" class="chat" style="left:{CHAT1['x']}px;top:{CHAT1['y']}px;
     width:{CHAT1['w']}px;height:{CHAT1['h']}px">
  <div class="chd"><span class="avt"></span><span class="nome">Cliente</span>
    <span class="hora">{CHAT1_HORA}</span></div>
  <div class="bin">{CHAT1_MSG1}</div>
  <div class="bout">{ATEND_MSG}</div>
  <div class="bin">{CHAT1_MSG2}</div>
</div>"""

TEMPO_HTML = f"""
<div data-slot="card" class="quad" style="left:{TEMPO['x']}px;top:{TEMPO['y']}px;
     width:{TEMPO['w']}px;height:{TEMPO['h']}px">
  {REL_SVG}
  <div class="tval">{GAP_DIAS}</div>
  <div class="qdet">dias no vácuo</div>
</div>"""

AGENT_HTML = f"""
<div data-slot="card" class="quad hero" style="left:{AGENT['x']}px;top:{AGENT['y']}px;
     width:{AGENT['w']}px;height:{AGENT['h']}px">
  <img class="icone" src="icone_agente_alfa.png">
  <div class="qrot"><span class="vivo"></span>AGENTE</div>
  <div class="qdet">{RAZAO}</div>
</div>"""

CHAT2_HTML = f"""
<div data-slot="card" class="chat" style="left:{CHAT2['x']}px;top:{CHAT2['y']}px;
     width:{CHAT2['w']}px;height:{CHAT2['h']}px">
  <div class="chd"><span class="avt"></span><span class="nome">Cliente</span>
    <span class="hora">{CHAT2_HORA}</span></div>
  <div class="hist"><span class="hq">{HIST_TAG}</span>
    {HIST_MSG}</div>
  <div class="sugg">
    <div class="stag">{SUGG_TAG}</div>
    {SUGG_MSG}
  </div>
  <div class="acao">a atendente revisou e enviou <span class="vv">✓✓</span></div>
  <div class="bin">{REPLY_MSG}</div>
</div>"""

AGEND_HTML = f"""
<div data-slot="card" class="quad" style="left:{AGEND['x']}px;top:{AGEND['y']}px;
     width:{AGEND['w']}px;height:{AGEND['h']}px">
  <img class="icone" src="icone_agendado_alfa.png">
  <div class="qrot">AGENDADO</div>
  <div class="qdet">{AGEND_DET}</div>
</div>"""


# ---------------------------------------------------------------- o painel --
def painel_fluxo(saida="_painel_fluxo.png", S=2):
    tra = "".join(f'<path class="glow" d="{a["d"]}"/><path class="fio" d="{a["d"]}"/>'
                  for a in ARESTAS)
    pts = "".join(f'<circle class="porta" cx="{x}" cy="{y}" r="7"/>'
                  for x, y in PORTAS)
    px, py = PULSO
    pulso = (f'<circle class="pulso-halo" cx="{px:.0f}" cy="{py:.0f}" r="17"/>'
             f'<circle class="pulso" cx="{px:.0f}" cy="{py:.0f}" r="6.5"/>')
    rots = "".join(
        f'<div class="rotulo" style="left:{r["em"][0]:.0f}px;'
        f'top:{r["em"][1]:.0f}px">{REL_SVG if r.get("rel") else ""}{r["txt"]}</div>'
        for r in ROTULOS)

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="shadcn-ref/saida.css">
<style>
@font-face{{font-family:'Jost';src:url(data:font/woff2;base64,__FONT__)
  format('woff2');font-weight:100 900}}
html{{margin:0}}
body{{margin:0;width:{PW}px;height:{PH}px;overflow:hidden;font-family:'Jost';
  background:url('BASE-vega.png') no-repeat 0px {-PAINEL_TOP}px}}
*{{font-family:'Jost';box-sizing:border-box}}

/* ---- janelas de chat (vidro): ritmo fixo de 16px, header com fio ---- */
.chat{{position:absolute;z-index:2;padding:24px 26px;display:flex;
  flex-direction:column;gap:16px}}
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
/* balão da ATENDENTE: enviado, à direita, com o azul da casa */
.bout{{align-self:flex-end;max-width:88%;padding:16px 22px;font-size:26px;
  font-weight:300;line-height:1.3;color:rgba(242,234,217,.94);
  background:rgba(29,67,184,.18);border:1px solid rgba(90,125,230,.30);
  border-radius:20px;border-bottom-right-radius:6px}}
/* node do tempo: o contador de dias */
.tval{{font-size:64px;font-weight:300;color:#F2EAD9;line-height:1;
  font-variant-numeric:tabular-nums;letter-spacing:-.03em}}
/* histórico herdado do chat 1: citação estilo reply do WhatsApp */
.hist{{font-size:22px;font-weight:300;color:rgba(231,220,198,.60);
  padding:8px 16px;border-left:3px solid rgba(231,220,198,.35);
  background:rgba(242,234,217,.045);border-radius:0 12px 12px 0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.hq{{display:block;font-size:15px;letter-spacing:.14em;
  color:rgba(231,220,198,.45);margin-bottom:3px;text-transform:uppercase}}
/* sugestão interna: o texto pronto do agente pra atendente (não é do cliente) */
.sugg{{align-self:stretch;padding:16px 22px;font-size:25px;font-weight:300;
  line-height:1.3;color:rgba(242,234,217,.94);border-radius:18px;
  background:rgba(29,67,184,.14);border:1.5px dashed rgba(90,125,230,.55)}}
.stag{{font-size:15px;font-weight:400;letter-spacing:.14em;
  color:rgba(160,180,240,.90);margin-bottom:8px;white-space:nowrap}}
.acao{{font-size:21px;font-weight:300;color:rgba(231,220,198,.60);
  letter-spacing:.03em;padding-left:6px}}
.vv{{color:rgba(120,160,255,.90);letter-spacing:-.08em}}

/* ---- nós quadrados com ícone ---- */
.quad{{position:absolute;z-index:2;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:10px;padding:18px}}
.icone{{width:132px;height:132px}}
.qrot{{font-size:20px;font-weight:400;letter-spacing:.24em;
  color:rgba(231,220,198,.80);display:flex;align-items:center;gap:10px}}
.qdet{{font-size:19px;font-weight:300;color:rgba(231,220,198,.50);
  letter-spacing:.06em}}
.vivo{{width:9px;height:9px;border-radius:50%;background:#F2EAD9;flex:none;
  box-shadow:0 0 8px rgba(242,234,217,.9),0 0 20px rgba(242,234,217,.45)}}
.pensa{{display:flex;gap:9px;align-items:center}}
.pensa i{{width:9px;height:9px;border-radius:50%;background:#F2EAD9;display:block}}
.pensa i:nth-child(1){{opacity:.95}}
.pensa i:nth-child(2){{opacity:.50}}
.pensa i:nth-child(3){{opacity:.22}}
/* o nó do agente é o cérebro: aresta de luz mais forte + halo (LUZ, não sombra) */
body.vega-liquid [data-slot=card].hero{{
  box-shadow:inset 0 1.5px 0 rgba(242,234,217,.85),
    inset 0 -1.5px 0 rgba(0,0,0,.45),
    inset 0 0 52px rgba(242,234,217,.09),
    0 0 46px rgba(242,234,217,.07),
    0 30px 60px -22px rgba(0,0,0,.95) !important}}

/* ---- fios, portas, pílulas ---- */
.rotulo{{position:absolute;font-size:23px;font-weight:300;z-index:3;
  letter-spacing:.04em;color:rgba(231,220,198,.85);white-space:nowrap;
  transform:translate(-50%,-50%);padding:8px 20px;border-radius:999px;
  background:rgba(8,8,8,.82);border:1px solid rgba(231,220,198,.15);
  display:flex;align-items:center;gap:10px}}
.rel{{flex:none;display:block;position:static}}
svg{{position:absolute;left:0;top:0;z-index:1}}
.fio{{fill:none;stroke:rgba(242,234,217,.92);stroke-width:4;
  stroke-linecap:round;stroke-dasharray:.1 16}}
.glow{{fill:none;stroke:rgba(242,234,217,.15);stroke-width:12;
  stroke-linecap:round;stroke-dasharray:.1 16}}
.porta{{fill:#0A0A0A;stroke:rgba(242,234,217,.85);stroke-width:2.5}}
.pulso{{fill:#F2EAD9}}
.pulso-halo{{fill:rgba(242,234,217,.16)}}
</style></head><body class="vega-liquid">
<svg width="{PW}" height="{PH}" viewBox="0 0 {PW} {PH}">{tra}{pts}{pulso}</svg>
{CHAT1_HTML}{TEMPO_HTML}{AGENT_HTML}{CHAT2_HTML}{AGEND_HTML}{rots}
</body></html>"""
    html = html.replace("__FONT__", base64.b64encode(FONTE.read_bytes()).decode())
    pag = AQUI / "_painel_fluxo.html"
    pag.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--no-sandbox", f"--force-device-scale-factor={S}",
                    "--default-background-color=00000000",
                    f"--window-size={PW},{PH}", "--virtual-time-budget=4000",
                    "--allow-file-access-from-files",
                    f"--screenshot={(AQUI / saida).as_posix()}", pag.as_uri()],
                   check=True, capture_output=True)
    return AQUI / saida


# ---------------------------------------------------------------- o slide --
def enfase(t):
    import re
    return re.sub(r"\*(.+?)\*", r'<span class="hard">\1</span>', t)

EXTRA = """
.obj{display:block;font-weight:200;font-size:80px;letter-spacing:-.025em;word-spacing:-.10em}
.txt{padding:0 72px}
.obj .hard{font-weight:500;color:#F6EFDE;
  text-shadow:0 0 10px rgba(242,234,217,.45),0 0 30px rgba(242,234,217,.20)}
.painel{position:absolute;left:0;top:__TOP__px;width:1080px}
"""

def render(nome="fluxo-followup", com_painel=True):
    if com_painel:
        icone_alfa("icone_agente")
        icone_alfa("icone_agendado")
        painel_fluxo()
    css = (DS / "preset.css").read_text(encoding="utf-8")
    css = css.replace("__FONT__", base64.b64encode(FONTE.read_bytes()).decode())
    css = css.replace("__BG__", "BASE-vega.png")
    css += EXTRA.replace("__TOP__", str(PAINEL_TOP)) + "\n.txt{top:165px}"

    obj = ["O cliente que sumiu", "Não tava *perdido*"]
    linhas = "".join(f'<span class="obj">{enfase(l)}</span>' for l in obj)
    painel_img = '<img class="painel" src="_painel_fluxo.png">' if com_painel else ""

    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<style>{css}</style></head><body>
<div class="canvas">
<div class="txt">{linhas}</div>
{painel_img}
</div></body></html>"""
    pag = AQUI / f"_{nome}.html"
    pag.write_text(html, encoding="utf-8")
    shot = AQUI / f"_shot_{nome}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--no-sandbox", "--force-device-scale-factor=2",
                    f"--window-size={W},{H}", "--virtual-time-budget=4000",
                    "--allow-file-access-from-files",
                    f"--screenshot={shot.as_posix()}", pag.as_uri()],
                   check=True, capture_output=True)
    bruto = Image.open(shot).convert("RGB")
    bruto.save(AQUI / f"SLIDE-{nome}@2x.png")
    im = bruto.resize((W, H), Image.LANCZOS)
    im.save(AQUI / f"SLIDE-{nome}.png")
    print(f"SLIDE-{nome}.png pronto")

if __name__ == "__main__":
    render()
