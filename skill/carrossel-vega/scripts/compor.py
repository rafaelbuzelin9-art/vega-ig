# -*- coding: utf-8 -*-
"""COMPOSITOR — carrossel 02, sistema VEGA.

Aplica o preset do repo (design-system/preset.css) por cima do fundo já
preparado. Igual ao render.py da skill, com duas diferenças:
  · Chrome do Windows (o do repo aponta pro binário do macOS)
  · modo OBJ (N linhas de 80px + subtítulo) e campo CLARO, que o preset.css
    ainda não cobre — ambos descritos em references/REGRAS.md
"""
import base64, json, os, re, subprocess, sys
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).resolve().parent
# fonte, preset e base saem de ASSETS. Rodando dentro do repo vega-ig, aponte
# ASSETS para design-system/; fora dele, para a pasta assets/ da skill.
ASSETS = Path(os.environ.get("VEGA_ASSETS") or
              (AQUI / "assets" if (AQUI / "assets").exists()
               else AQUI.parent / "design-system"))
DS = ASSETS
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H = 1080, 1350

SLIDES = {
    # SLIDE 01 — capa com o Atlas e a legenda em arco no globo. Depende dos
    # fundos recortados (fundos/arco.png + arco.json), que moram no repo vega-ig;
    # aqui fica como referência de configuração.
    "arco-b": {
        "bg": "arco@2x.png", "hires": True,
        "claro": False, "txt_top": 165, "nu": True,
        "obj": ["Talvez o problema nunca", "Tenha sido uma *pessoa*"],
        # ângulo ≈ comprimento do texto ÷ raio. A 54px o arco dava 167° e as
        # pontas viravam; corpo menor encurta o texto e folga maior abre o raio.
        "arco": {"json": "fundos/arco.json", "folga": 44, "entre": 60,
                 "corpo": 42, "peso": 300, "cor": "#E7DCC6",
                 # linhas do arco com o MESMO número de caracteres
                 "linhas": ["Você troca a agência, o time.",
                            "O resultado continua o mesmo."]},
    },
    # SLIDE 02 — a cena é um componente nosso: o card do shadcn em vidro.
    # A base entra crua, sem nenhuma arte por baixo.
    "volume": {
        "bg": "../BASE-vega.png", "claro": False, "txt_top": 165, "nu": True,
        "obj": ["O problema não é a tarefa", "É o *volume*"],
        "sub": "Um minuto por confirmação. Dois por retomada.|"
               "Cinco por horário vago. Dezenas de vezes, todos os dias.",
        "card": {
            "top": 580, "larg": 300, "zoom": 1.52, "alt": 780,
            "tema": "vega-liquid",
            "metricas": [
                {"rot": "Confirmação", "alvo": 1, "un": "min", "ini": 0.06},
                {"rot": "Retomada", "alvo": 2, "un": "min", "ini": 0.20},
                {"rot": "Horário vago", "alvo": 5, "un": "min", "ini": 0.34},
                {"rot": "No mês", "alvo": 38, "un": "h", "ini": 0.48},
            ],
        },
    },
}

EXTRA = """
/* tokens do shadcn recebendo a paleta da Vega: a geometria do card fica
   intacta, só a cor muda */
.painel{--card:#F7F1E3;--card-foreground:#14100B;--primary:#14100B;
  --muted-foreground:#6E6253;--border:rgba(28,23,18,.14)}
/* --- modo OBJ e campo claro (references/REGRAS.md, formatos objetivos) --- */
.obj{display:block;font-weight:200;font-size:80px;letter-spacing:-.025em;word-spacing:-.10em}
.txt{padding:0 72px}
/* PADRAO DA CASA: 38px. A 31px o subtitulo sumia no feed — no tamanho em que
   o carrossel e visto de verdade ele virava textura, nao leitura. */
.sub{display:block;font-weight:300;font-size:38px;letter-spacing:-.005em;
     margin-top:40px;line-height:1.34;color:#CFC3AE;text-shadow:none;
     white-space:pre-line}
.obj .hard{font-weight:500;color:#F6EFDE;
  text-shadow:0 0 10px rgba(242,234,217,.45),0 0 30px rgba(242,234,217,.20)}
body.claro .txt{color:#050505;text-shadow:none}
body.claro .obj .hard{color:#050505;text-shadow:none}
body.claro .sub{color:#6E6253;font-size:42px}
body.claro .grid{background-image:radial-gradient(circle at center,rgba(5,5,5,.10) 1.2px,transparent 1.3px)}

/* --- CARTÃO DE DADOS (padrão novo do carrossel) ------------------------
   Vidro sobre o Preto Cine: o corpo é quase transparente e quem desenha a
   forma é a luz na borda de cima, como nos painéis da Apple. Fundo chapado
   com borda cinza lê como caixa de formulário; luz na aresta lê como tela. */
.card{position:absolute;left:50%;transform:translateX(-50%);overflow:hidden;
  font-family:'Jost';border-radius:44px;
  border:1px solid rgba(231,220,198,.12);
  /* o vidro precisa de CORPO: com o cartão translúcido de verdade, a malha de
     pontos da base atravessava a tela e a leitura virava textura suja */
  background:linear-gradient(180deg,rgba(247,240,225,.070),
             rgba(247,240,225,.018) 46%,rgba(247,240,225,.040)),
             linear-gradient(180deg,#0B0B0B,#080808);
  /* profundidade em camadas, de dentro pra fora: luz na aresta de cima,
     escuridao acumulada no pe do cartao, linha de contato preta e duas
     sombras de alcance diferente. Uma sombra so achata a peca na tela. */
  box-shadow:inset 0 1.5px 0 rgba(247,240,225,.26),
             inset 0 -90px 120px -40px rgba(0,0,0,.75),
             inset 0 0 120px rgba(247,240,225,.030),
             0 1px 0 rgba(0,0,0,.95),
             0 26px 50px -18px rgba(0,0,0,.90),
             0 70px 130px -30px rgba(0,0,0,.75)}
/* luz ambiente ATRAS do cartao: o quadro deixa de ser fundo e vira espaco */
.glow{position:absolute;left:50%;transform:translateX(-50%);border-radius:50%;
  filter:blur(110px);pointer-events:none;
  background:radial-gradient(60% 60% at 50% 50%,rgba(120,160,255,.20),
             rgba(247,240,225,.06) 55%,transparent 72%)}
/* halo frio subindo do rodapé: é o que dá o ar de tela ligada */
.card::after{content:"";position:absolute;inset:auto -20% -55% -20%;height:90%;
  background:radial-gradient(50% 60% at 50% 100%,rgba(120,160,255,.13),transparent 72%);
  pointer-events:none}
.cardtop{display:flex;align-items:center;justify-content:space-between;
  padding:34px 46px 24px;font-size:22px;font-weight:300;letter-spacing:.22em;
  text-transform:uppercase;color:#6E6253}
.chip{font-size:20px;letter-spacing:.14em;color:#9C8F7D;padding:9px 20px;
  border:1px solid rgba(231,220,198,.16);border-radius:999px}
.lin{display:flex;align-items:baseline;justify-content:space-between;
  padding:22px 46px;border-top:1px solid rgba(0,0,0,.55);
  box-shadow:inset 0 1px 0 rgba(247,240,225,.055)}
.lin .rot{font-size:34px;font-weight:200;color:#C4B7A3;letter-spacing:-.01em}
.lin .val{font-size:60px;font-weight:200;color:#F6EFDE;
  font-variant-numeric:tabular-nums;letter-spacing:-.03em}
.lin .un{font-size:30px;font-weight:300;color:#6E6253;margin-left:12px}
.tot{display:flex;align-items:flex-end;justify-content:space-between;
  padding:30px 46px 34px;border-top:1px solid rgba(0,0,0,.7);
  box-shadow:inset 0 1px 0 rgba(247,240,225,.10);
  background:linear-gradient(180deg,rgba(29,67,184,.14),rgba(29,67,184,.02) 70%)}
.tot .rot{display:block;font-size:20px;letter-spacing:.22em;
  text-transform:uppercase;color:#6E6253;margin-bottom:10px}
.tot .val{font-size:112px;font-weight:200;color:#F6EFDE;line-height:.86;
  font-variant-numeric:tabular-nums;letter-spacing:-.045em}
.tot .un{font-size:48px;font-weight:300;color:#9C8F7D;margin-left:6px}
.seta{fill:none;stroke:#3358D8;stroke-width:5;stroke-linecap:round;
  stroke-linejoin:round;opacity:.85}
.trilho{position:absolute;left:0;right:0;bottom:0;height:3px;
  background:rgba(231,220,198,.08)}
.trilho i{position:absolute;left:0;top:0;bottom:0;display:block;
  background:linear-gradient(90deg,rgba(51,88,216,.25),#3358D8)}

/* CARTÃO CLARO: creme sobre o Preto Cine. O contraste alto tira o cartão do
   fundo e ele passa a flutuar; o escuro se funde com a base e some. */
.card.luz{border:1px solid rgba(247,240,225,.55);
  background:linear-gradient(180deg,#F7F1E2,#E6DBC3);
  box-shadow:inset 0 2px 0 rgba(255,255,255,.85),
             inset 0 -70px 90px -50px rgba(110,98,83,.35),
             0 1px 0 rgba(0,0,0,.9),
             0 26px 50px -18px rgba(0,0,0,.85),
             0 80px 140px -30px rgba(0,0,0,.70)}
.card.luz::after{background:none}
.card.luz .cardtop{color:#8A7C69}
.card.luz .chip{color:#6E6253;border-color:rgba(28,23,18,.20)}
.card.luz .lin{border-top:1px solid rgba(28,23,18,.13);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.75)}
.card.luz .lin .rot{color:#6E6253}
.card.luz .lin .val{color:#14100B}
.card.luz .lin .un{color:#8A7C69}
/* no tema claro o veu azul sobre creme vira cinza sujo: a faixa do total
   ganha profundidade descendo pro Areia, e o azul fica so no acento */
.card.luz .tot{border-top:1px solid rgba(28,23,18,.22);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.70);
  background:linear-gradient(180deg,#EFE5D0,#E2D6BB)}
.card.luz .tot .rot{color:#6E6253}
.card.luz .tot .val{color:#14100B}
.card.luz .tot .un{color:#6E6253}
.card.luz .seta{stroke:#1D43B8;opacity:1}
.card.luz .trilho{background:rgba(28,23,18,.10)}


/* --- PAINEL: o CSS vem do Tailwind compilado em shadcn-ref/saida.css, com
   as classes reais de registry/new-york-v4/ui/card.tsx. Aqui só entram a
   posição no quadro, a escala e a fonte da casa. ------------------------- */
.painel{position:absolute;left:50%;transform:translateX(-50%)}

/* lista de itens: corpo pequeno com cota, para slides de enumeração */
.item{display:block;font-weight:200;font-size:42px;letter-spacing:-.02em;
      line-height:1.46;text-align:left;padding-left:96px}
.item .cota{display:inline-block;width:56px;margin-left:-72px;
            font-size:24px;letter-spacing:.10em;color:#9C8F7D;
            vertical-align:.30em;text-shadow:none}
.itens{display:block;width:720px;margin:46px auto 0}
body.claro .item .cota{color:#6E6253}
"""

def enfase(t):
    return re.sub(r"\*(.+?)\*", r'<span class="hard">\1</span>', t)


# O cartão é desenhado com um relógio próprio, T de 0 a 1. O render estático
# pede T=1; o vídeo vai pedir um T por frame e reusar o MESMO html, então o
# que se vê aqui já é o último quadro da animação, não um desenho à parte.
CARD_JS = """
const T = __T__;
const suave = x => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
document.querySelectorAll('[data-alvo]').forEach(el => {
  const alvo = +el.dataset.alvo, ini = +el.dataset.ini, dur = +el.dataset.dur || .55;
  const p = suave((T - ini) / dur);
  // o número SOBE até o alvo em vez de aparecer pronto: é a contagem que
  // conta a história do slide, o valor final sozinho seria só um dado
  el.textContent = Math.round(alvo * p);
  const linha = el.closest('[data-slot=card]');
  if (linha) {
    linha.style.opacity = (.10 + .90 * suave((T - ini) / .30)).toFixed(3);
    linha.style.transform = 'translateY(' + (16 * (1 - suave((T - ini) / .40))).toFixed(1) + 'px)';
  }
});
const tr = document.querySelector('.trilho i');
if (tr) tr.style.width = (100 * suave(T)).toFixed(1) + '%';
"""


CARD_CLS = ("@container/card flex flex-col gap-6 rounded-xl border bg-card "
            "py-6 text-card-foreground shadow-xs bg-gradient-to-t "
            "from-primary/5 to-card")


def painel_png(C, t=1.0, saida="_painel.png", S=2):
    """Renderiza o painel SOZINHO e devolve o PNG que o slide cola por cima.

    Duas coisas justificam o documento separado:
      1. No mesmo documento do slide, o `*{margin:0;padding:0}` do preset.css
         anula o px-6/py-6 das utilities e o cartao vem achatado.
      2. Vidro precisa de fundo. O documento carrega a MESMA base do slide,
         deslocada para a posicao exata do painel, entao o backdrop-filter tem
         o que borrar e a malha de pontos continua alinhada na colagem.
    """
    cartoes = "".join(
        f'<div data-slot="card" class="{CARD_CLS}">'
        f'<div data-slot="card-header" class="grid auto-rows-min '
        f'grid-rows-[auto_auto] items-start gap-2 px-6">'
        f'<div data-slot="card-description" class="text-sm text-muted-foreground">'
        f'{m["rot"]}</div>'
        f'<div data-slot="card-title" class="leading-none font-semibold '
        f'text-2xl tabular-nums @[250px]/card:text-3xl">'
        f'<span data-alvo="{m["alvo"]}" data-ini="{m["ini"]}">{m["alvo"]}</span>'
        f' {m["un"]}</div></div></div>'
        for m in C["metricas"])

    Z = C.get("zoom", 1)
    larg = round(C["larg"] * Z)
    alt = C.get("alt", 780)
    esq = (W - larg) // 2
    tema = C.get("tema", "vega")
    vidro = tema == "vega-liquid"

    fundo = (f"background:url('BASE-vega.png') no-repeat "
             f"{-esq}px {-C['top']}px;" if vidro else "background:transparent;")
    aura = ""   # a luz do vidro passou para dentro do cartao (entrada.css)

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="shadcn-ref/saida.css">
<style>
@font-face{{font-family:'Jost';src:url(data:font/woff2;base64,__FONT__)
  format('woff2');font-weight:100 900}}
html{{margin:0}}
body{{margin:0;width:{larg}px;height:{alt}px;overflow:hidden;
  font-family:'Jost';{fundo}}}
*{{font-family:'Jost'}}
/* AURA: luz difusa atras dos cartoes. Vidro sobre preto puro nao tem o que
   refratar e vira plastico fosco; a aura da o que a lente distorce. */
.aura{{position:absolute;border-radius:50%;filter:blur(90px);z-index:0}}
.a1{{left:-14%;top:4%;width:72%;height:38%;
  background:radial-gradient(circle,rgba(60,110,255,.45),transparent 70%)}}
.a2{{right:-18%;bottom:2%;width:76%;height:42%;
  background:radial-gradient(circle,rgba(247,222,180,.32),transparent 70%)}}
.wrap{{position:relative;z-index:1;zoom:{Z}}}
</style></head><body class="{tema}">
{aura}<div class="wrap"><div class="flex flex-col gap-4">{cartoes}</div></div>
<script>{CARD_JS.replace("__T__", str(t))}</script>
</body></html>"""
    html = html.replace("__FONT__", base64.b64encode(
        (DS / "jost-variable-latin.woff2").read_bytes()).decode())
    pag = AQUI / "_painel.html"
    pag.write_text(html, encoding="utf-8")

    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--no-sandbox", f"--force-device-scale-factor={S}",
                    "--default-background-color=00000000",
                    f"--window-size={larg},{alt}", "--virtual-time-budget=4000",
                    "--allow-file-access-from-files",
                    f"--screenshot={(AQUI / saida).as_posix()}", pag.as_uri()],
                   check=True, capture_output=True)
    return AQUI / saida


def render(nome, cfg):
    tw = (AQUI / "shadcn-ref" / "saida.css").read_text(encoding="utf-8")
    css = tw + "\n" + (DS / "preset.css").read_text(encoding="utf-8")
    css = css.replace("__FONT__", base64.b64encode(
        (DS / "jost-variable-latin.woff2").read_bytes()).decode())
    css = css.replace("__BG__", "fundos/" + cfg["bg"])
    css += EXTRA + f"\n.txt{{top:{cfg['txt_top']}px}}"
    if cfg.get("corpo"):
        css += f"\n.obj{{font-size:{cfg['corpo']}px}}"

    logo = "vega-lockup-peca-tinta.svg" if cfg["claro"] else "vega-lockup-peca.svg"
    linhas = "".join(f'<span class="obj">{enfase(l)}</span>' for l in cfg["obj"])
    if cfg.get("itens"):
        linhas += '<span class="itens">' + "".join(
            f'<span class="item"><span class="cota">{i:02d}</span>{enfase(t)}</span>'
            for i, t in enumerate(cfg["itens"], 1)) + "</span>"
    if cfg.get("sub"):
        # quebra CONTROLADA por "|": o brief trata órfã tipográfica como
        # reprovação, então o subtítulo nunca é quebrado pelo navegador
        linhas += '<span class="sub">' + cfg["sub"].replace("|", "<br>") + "</span>"

    # LEGENDA EM ARCO: as linhas correm em círculos concêntricos ao globo,
    # cujo centro e raio foram medidos na máscara da estátua (sobre_base.py).
    # Cada linha é um <textPath> num semicírculo próprio; a de cima é a mais
    # externa, então a leitura vai de fora para dentro, na direção do mármore.
    arco = ""
    if cfg.get("arco"):
        A = cfg["arco"]
        g = json.load(open(A["json"]))
        linhas_arco = A["linhas"]
        paths, textos = [], []
        for i, linha in enumerate(linhas_arco):
            r = g["r"] + A["folga"] + (len(linhas_arco) - 1 - i) * A["entre"]
            paths.append(f'<path id="arc{i}" fill="none" d="M {g["cx"]-r} {g["cy"]} '
                         f'A {r} {r} 0 0 1 {g["cx"]+r} {g["cy"]}"/>')
            textos.append(
                f'<text class="arctxt"><textPath href="#arc{i}" '
                f'startOffset="50%" text-anchor="middle">{linha}</textPath></text>')
        arco = (f'<svg class="arcosvg" width="{W}" height="{H}" '
                f'viewBox="0 0 {W} {H}"><defs>{"".join(paths)}</defs>'
                f'{"".join(textos)}</svg>')
        css += (f"\n.arcosvg{{position:absolute;left:0;top:0;pointer-events:none}}"
                f"\n.arctxt{{font-family:'Jost';font-weight:{A.get('peso',300)};"
                f"font-size:{A['corpo']}px;fill:{A.get('cor','#E7DCC6')};"
                f"letter-spacing:{A.get('track','.02em')}}}")

    # camada OVER: componente da cena que fica NA FRENTE do texto. Só existe
    # porque o Image Decompose devolve os objetos separados uns dos outros.
    if cfg.get("card"):
        C = cfg["card"]
        painel_png(C, cfg.get("t", 1.0))
        cartao = (f'<img class="painel" src="_painel.png" '
                  f'style="top:{C["top"]}px;width:{round(C["larg"] * C.get("zoom", 1))}px">')
    else:
        cartao = ""

    over = (f'<img class="over" src="{cfg["over"]}">' if cfg.get("over") else "")
    if over:
        css += ("\n.over{position:absolute;left:0;top:0;width:1080px;"
                "height:1350px;pointer-events:none}")

    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<style>{css}</style></head><body class="{'claro' if cfg['claro'] else ''}">
<div class="canvas">
{'' if cfg.get("nu") else '<div class="grid"></div>'}
{'' if cfg.get("nu") else f'<div class="logo">{(DS / logo).read_text(encoding="utf-8")}</div>'}
<div class="txt">{linhas}</div>
{cartao}
{arco}
{over}
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

    saida = AQUI / f"SLIDE-{nome}.png"
    bruto = Image.open(shot).convert("RGB")            # 2160x2700 nativo
    if cfg.get("hires"):
        bruto.save(AQUI / f"SLIDE-{nome}@2x.png")
    im = bruto.resize((W, H), Image.LANCZOS)
    im.save(saida)

    # margem lateral do bloco de texto (guardrail: asserção de efeito)
    px = im.convert("L").load()
    y0, y1 = cfg["txt_top"], min(cfg["txt_top"] + 420, H)
    lim = 70 if not cfg["claro"] else 0
    def claro_em(x):
        return any((px[x, y] > 70) if not cfg["claro"] else (px[x, y] < 120)
                   for y in range(y0, y1))
    esq = next((x for x in range(W) if claro_em(x)), None)
    dirx = next((x for x in range(W - 1, -1, -1) if claro_em(x)), None)
    m = f"margens {esq}/{W-1-dirx}px" if esq is not None else "texto nao detectado"
    print(f"SLIDE-{nome}.png  {m}")

    # ÂNGULO REAL DO ARCO. Texto curvo morre quando ocupa ângulo demais: perto
    # de 180° as pontas ficam verticais e depois começam a virar de cabeça
    # para baixo. Acima de ~140° já não se lê. Medido no pixel, não estimado.
    if cfg.get("arco"):
        import math
        g = json.load(open(cfg["arco"]["json"]))
        cx, cy, r = g["cx"], g["cy"], g["r"]
        px2 = im.load()
        angs = []
        for y in range(0, int(cy)):
            for x in range(0, W, 2):
                d = math.hypot(x - cx, y - cy)
                if r + 10 < d < r + 260 and px2[x, y][0] > 120:
                    angs.append(math.degrees(math.atan2(cy - y, x - cx)))
        if angs:
            print(f"   arco ocupa {180 - 2*min(angs):.0f}° "
                  f"(alvo <=140°; acima disso a ponta vira)")

if __name__ == "__main__":
    for n in (sys.argv[1:] or list(SLIDES)):
        render(n, SLIDES[n])
