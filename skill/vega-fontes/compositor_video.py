#!/usr/bin/env python3
"""
Compositor de vídeo genérico do carrossel VEGA.

  python3 compositor_video.py <video.mp4> <slide_n> "<linha2 com *enfase*>" [txt_top]

Faz, nesta ordem:
  1. extrai frames
  2. detecta a linha do campo (fração de claros, faixa 30-62%) e alinha em 50.5%
     - linha alta demais -> estende campo preto por cima (padding invisível)
  3. clamp do preto: pixel só clampado se quase-preto em TODOS os frames
     amostrados, com erosão (o que se move nunca é engolido)
  4. costura o loop: último 1s crossfade no primeiro 1s
  5. texto centrado no vazio real (logo -> elemento que cruza), salvo override
  6. constelação em fase com o loop
  7. SLIDE<n>-final.mp4 em 1080x1350 24fps
"""
import math, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
import tempfile
SCRATCH = Path(tempfile.gettempdir()) / "vega-carrossel-work"
FPS, FADE = 24, 24
W, H = 1080, 1350
SW, SH = 2160, 2700
AURA = (29, 67, 184)
CORE = (217, 228, 255)
STARS = [(338,182,0.00,CORE),(702,130,0.30,CORE),(858,468,0.55,AURA),(234,520,0.80,CORE)]

def detectar_linha(g):
    """borda campo->cena por fração de pixels claros, na faixa 30-62%."""
    w, h = g.size; px = g.load()
    cols = range(0, w, max(1, w//120)); n = len(list(cols))
    rows = [sum(1 for x in cols if px[x, y] > 60) / n for y in range(h)]
    y0, y1 = int(h*.30), int(h*.62)
    return max(range(y0, y1), key=lambda y: rows[y+1]-rows[y]) + 1

def montar_overlay(texto, txt_top, l1=None, claro=False):
    import base64
    css = (BASE/"preset.css").read_text()
    css = css.replace("__FONT__", base64.b64encode((ROOT/"fonts/jost-variable-latin.woff2").read_bytes()).decode())
    css = css.replace("background:url('__BG__') center/cover no-repeat;", "background:transparent;")
    css += f"\nhtml,body{{background:transparent!important}}\n.txt{{top:{txt_top}px}}"
    enf = lambda t: re.sub(r"\*(.+?)\*", r'<span class="hard">\1</span>', t)
    if texto.startswith("OBJL:"):
        # formato objetivo alinhado à esquerda: N linhas de headline + subtítulo
        partes = texto[5:].split("|")
        heads, subv = partes[:-1], partes[-1]
        css += ("\n.txt{top:190px;left:74px;right:120px;padding:0;text-align:left}"
                "\n.oh{display:block;font-weight:200;font-size:80px;line-height:1.08;white-space:nowrap}"
                "\n.oh .hard{font-weight:500;color:#F6EFDE;"
                "text-shadow:0 0 8px rgba(242,234,217,.42),0 0 24px rgba(242,234,217,.18)}"
                "\n.osub{display:block;margin-top:24px;font-weight:300;font-size:31px;"
                "letter-spacing:.01em;word-spacing:0;color:#9C8F7D;text-shadow:none}")
        linhas = "".join(f'<span class="oh">{enf(h)}</span>' for h in heads) + \
                 f'<span class="osub">{subv}</span>'
    elif texto.startswith("OBJ:"):
        # formato objetivo centrado: N linhas de headline + subtítulo
        partes = texto[4:].split("|")
        heads, subv = partes[:-1], partes[-1]
        css += ("\n.txt{top:158px}"
                "\n.oh{display:block;font-weight:200;font-size:80px;line-height:1.08;white-space:nowrap}"
                "\n.oh .hard{font-weight:500;color:#F6EFDE;"
                "text-shadow:0 0 8px rgba(242,234,217,.42),0 0 24px rgba(242,234,217,.18)}"
                "\n.osub{display:block;margin-top:24px;font-weight:300;font-size:31px;"
                "letter-spacing:.01em;word-spacing:0;color:#9C8F7D;text-shadow:none}")
        linhas = "".join(f'<span class="oh">{enf(h)}</span>' for h in heads) + \
                 f'<span class="osub">{subv}</span>' 
    elif texto.startswith("WSTACK:"):
        css += ("\n.wstack{position:absolute;left:74px;top:160px;display:flex;"
                "flex-direction:column;gap:24px;font-weight:500;font-size:48px;"
                "letter-spacing:.08em;color:#F2EAD9;"
                "text-shadow:0 0 4px rgba(242,234,217,.38),0 0 14px rgba(242,234,217,.14)}")
        palavras = texto[7:].split("|")
        linhas = '<span class="wstack">' + "".join(f"<span>{p}</span>" for p in palavras) + "</span>"
    elif texto.startswith("WORDS:"):
        css += ("\n.words{display:flex;justify-content:center;gap:18px;"
                "font-weight:500;font-size:56px;letter-spacing:.08em;color:#F2EAD9;"
                "text-shadow:0 0 5px rgba(242,234,217,.38),0 0 16px rgba(242,234,217,.14)}")
        palavras = texto[6:].split("|")
        linhas = '<span class="words">' + "".join(f"<span>{p}</span>" for p in palavras) + "</span>"
    else:
        linhas = (f'<span class="l1">{enf(l1)}</span>' if l1 else "") + f'<span class="l2">{enf(texto)}</span>'
    if claro:
        css += ("\n.osub{font-size:36px!important}"
                "\n.txt,.oh{color:#050505!important;text-shadow:none!important}"
                "\n.oh .hard{color:#050505!important;text-shadow:none!important}"
                "\n.osub{color:#6E6253!important}"
                "\n.grid{background-image:radial-gradient(circle at center,rgba(5,5,5,.10) 1.2px,transparent 1.3px)!important;"
                "-webkit-mask-image:linear-gradient(to bottom,#000 0%,#000 calc(var(--field) - 12%),transparent var(--field))}")
    logosvg = (ROOT/("vega-lockup-peca-tinta.svg" if claro else "vega-lockup-peca.svg")).read_text()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body><div class="canvas"><div class="grid"></div>
<div class="logo">{logosvg}</div>
<div class="txt">{linhas}</div>
</div></body></html>"""
    (SCRATCH/"overlay.html").write_text(html)
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless=new","--disable-gpu","--hide-scrollbars","--no-sandbox",
        "--force-device-scale-factor=2",f"--window-size={W},{H}",
        "--virtual-time-budget=4000","--default-background-color=00000000",
        f"--screenshot={SCRATCH/'overlay.png'}", f"file://{SCRATCH/'overlay.html'}"],
        check=True, capture_output=True)
    return Image.open(SCRATCH/"overlay.png").convert("RGBA")

def estrelas(n, N, out):
    ph = n / N
    st = Image.new("RGBA",(SW,SH),(0,0,0,0)); ds = ImageDraw.Draw(st)
    for x,y,phs,cor in STARS:
        a = 0.10 + 0.26*(0.5 - 0.5*math.cos(2*math.pi*(ph+phs)))
        ds.ellipse([x*2-5,y*2-5,x*2+5,y*2+5], fill=cor+(int(a*255),))
    out.alpha_composite(st.filter(ImageFilter.GaussianBlur(1.6)))

def main(video, n_slide, texto, l1=None, txt_top=None, align=0.505, claro=False):
    frames_dir = SCRATCH/"src"; frames_dir.mkdir(parents=True, exist_ok=True)
    for f in frames_dir.glob("*.jpg"): f.unlink()
    subprocess.run(["ffmpeg","-y","-i",video,"-qscale:v","2",str(frames_dir/"s%03d.jpg")],
                   check=True, capture_output=True)
    src = sorted(frames_dir.glob("s*.jpg"))
    M = len(src); N = M - FADE
    print(f"{M} frames -> ciclo {N} ({N/FPS:.2f}s)")

    f0 = Image.open(src[0]).convert("RGB")
    vw, vh = f0.size
    novo_h = int(vw*5/4)
    linha = detectar_linha(f0.convert("L"))
    topo = round(linha - align*novo_h)
    pad = max(0, -topo)
    topo = max(0, topo)
    if pad: print(f"linha alta: +{pad}px de preto no topo")
    corte_max = vh + pad - novo_h
    topo = min(topo, corte_max)
    print(f"vídeo {vw}x{vh}  linha {linha/vh*100:.1f}%  pad {pad}  topo {topo}  -> linha em {(linha+pad-topo)/novo_h*100:.1f}% (alvo {align*100:.0f}%)")

    def alinhar(im):
        if pad:
            ext = Image.new("RGB",(vw, vh+pad),(5,5,5)); ext.paste(im,(0,pad)); im = ext
        return im.crop((0, topo, vw, topo+novo_h)).resize((SW,SH), Image.LANCZOS)

    # ---- campo preto redesenhado: linha DURA matemática (como nos slides 1-3) ----
    # O vídeo+upscale amolecem a borda; em vez de clampar o que é escuro,
    # o campo inteiro acima da linha vira #050505 absoluto e só a silhueta
    # do elemento que cruza (arco/cúpula/frontão) sobrevive, com borda limpa.
    maximo = None
    for i in (0, M//4, M//2, 3*M//4, M-1):
        g = alinhar(Image.open(src[i]).convert("RGB")).convert("L")
        maximo = g if maximo is None else ImageChops.lighter(maximo, g)
    y_linha = round(align * SH)
    acima = Image.new("L", (SW, SH), 0)
    ImageDraw.Draw(acima).rectangle([0, 0, SW, y_linha - 1], fill=255)
    keep = maximo.point(lambda v: 255 if v > 16 else 0)
    keep = keep.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.MinFilter(13))  # fecha buracos internos (pedra sombreada)
    keep = keep.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(7))    # mata ruído isolado do campo

    # Só UM elemento cruza a linha (regra dos slides 1-3): fica o componente
    # conectado à linha pela região central; capitéis e topos de parede das
    # bordas são truncados na borda exata do campo.
    from collections import deque
    F = 4
    sw4, sh4 = SW//F, SH//F
    peq = keep.resize((sw4, sh4), Image.NEAREST)
    pp = peq.load()
    yl4 = min(sh4-1, round(align*sh4))
    vis = [[False]*sw4 for _ in range(sh4)]
    fila = deque()
    for x in range(int(sw4*0.22), int(sw4*0.78)):
        if pp[x, yl4-1] and not vis[yl4-1][x]:
            vis[yl4-1][x] = True; fila.append((x, yl4-1))
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < sw4 and 0 <= ny < yl4 and pp[nx,ny] and not vis[ny][nx]:
                vis[ny][nx] = True; fila.append((nx, ny))
    cen = Image.new("L", (sw4, sh4), 0); cp2 = cen.load()
    for y in range(yl4):
        for x in range(sw4):
            if vis[y][x]: cp2[x,y] = 255
    keep_bin = cen.resize((SW, SH), Image.NEAREST).filter(ImageFilter.MaxFilter(5))
    if claro:
        # campo claro: só pedra clara E conectada à linha — a interseção com o
        # brilho quebra pontes escuras do componente, então a conectividade
        # roda DE NOVO depois dela, matando ilhas órfãs
        claridade = maximo.point(lambda v: 255 if v > 20 else 0)
        claridade = claridade.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
        claridade = claridade.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
        keep_bin = ImageChops.multiply(keep_bin, claridade)
        peq2 = keep_bin.resize((sw4, sh4), Image.NEAREST)
        pp2 = peq2.load()
        vis2 = [[False]*sw4 for _ in range(sh4)]
        fila2 = deque()
        for x in range(int(sw4*0.22), int(sw4*0.78)):
            if pp2[x, yl4-1] and not vis2[yl4-1][x]:
                vis2[yl4-1][x] = True; fila2.append((x, yl4-1))
        while fila2:
            x, y = fila2.popleft()
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x+dx, y+dy
                if 0 <= nx < sw4 and 0 <= ny < yl4 and pp2[nx,ny] and not vis2[ny][nx]:
                    vis2[ny][nx] = True; fila2.append((nx, ny))
        cen2 = Image.new("L", (sw4, sh4), 0); cp3 = cen2.load()
        for y in range(yl4):
            for x in range(sw4):
                if vis2[y][x]: cp3[x,y] = 255
        keep_bin = cen2.resize((SW, SH), Image.NEAREST)
        keep_bin = ImageChops.multiply(keep_bin, claridade)
        keep_bin = keep_bin.filter(ImageFilter.MaxFilter(3))
    keep = keep_bin.filter(ImageFilter.GaussianBlur(1.1))                            # borda suave 1px
    campo_alpha = ImageChops.subtract(acima, keep)
    preto = Image.new("RGB",(SW,SH),(242,234,217) if claro else (5,5,5))

    # texto: centro do vazio (logo ~140 -> topo do elemento que cruza)
    if txt_top is None:
        g = maximo  # já alinhado, max dos frames: pega o topo mais alto que o elemento atinge
        gp = g.load()
        crown = next((y for y in range(200, int(align*SH))
                      if any(gp[x,y] > 85 for x in range(400, SW-400, 8))), int(0.4*SH))
        crown_1080 = crown/2
        meia_altura = 95 if l1 else (30 if texto.startswith("WORDS:") else 49)
        txt_top = max(150, round((140 + crown_1080)/2 - meia_altura))
        print(f"elemento cruza até y={crown_1080:.0f} -> txt_top={txt_top}")

    overlay = montar_overlay(texto, txt_top, l1, claro)
    out_dir = SCRATCH/"out"; out_dir.mkdir(exist_ok=True)
    for f in out_dir.glob("*.jpg"): f.unlink()

    for n in range(N):
        base = alinhar(Image.open(src[n+FADE]).convert("RGB"))
        k = n - (N-FADE)
        if k >= 0:
            alt = alinhar(Image.open(src[k]).convert("RGB"))
            base = Image.blend(base, alt, (k+1)/FADE)
        base.paste(preto, (0,0), campo_alpha)
        out = base.convert("RGBA")
        out.alpha_composite(overlay)
        if not claro: estrelas(n, N, out)
        out.convert("RGB").resize((W,H), Image.LANCZOS).save(out_dir/f"f{n:03d}.jpg", quality=95)
        if n % 24 == 0: print(f"frame {n}/{N}")

    mp4 = ROOT/f"SLIDE{n_slide}-final.mp4"
    subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(out_dir/"f%03d.jpg"),
        "-c:v","libx264","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart","-an",str(mp4)],
        check=True, capture_output=True)
    print("ok:", mp4)

if __name__ == "__main__":
    args = sys.argv[1:]
    l1 = args[3] if len(args) > 3 and args[3] != "-" else None
    top = int(args[4]) if len(args) > 4 and args[4] != "-" else None
    al = float(args[5]) if len(args) > 5 else 0.505
    claro = len(args) > 6 and args[6] == "claro"
    main(args[0], int(args[1]), args[2], l1, top, al, claro)
