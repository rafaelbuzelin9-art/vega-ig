#!/usr/bin/env python3
"""
Slide 2 claro — formato cartão (referência Replit):
campo creme integral, texto escuro em cima, e o vídeo do corredor
dentro de um cartão de cantos arredondados. Sem máscara de silhueta.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
import tempfile
SCRATCH = Path(tempfile.gettempdir()) / "vega-carrossel-work"
SCRATCH.mkdir(parents=True, exist_ok=True)
FPS, FADE = 24, 24
W, H = 1080, 1350
SW, SH = 2160, 2700
CREME = (242, 234, 217)

# cartão em espaço 1080 (x0,y0,x1,y1) e raio
CARD = (0, 560, 1080, 1350)
RAIO = 0

def main(video):
    src_dir = SCRATCH/"src"; src_dir.mkdir(exist_ok=True)
    for f in src_dir.glob("*.jpg"): f.unlink()
    subprocess.run(["ffmpeg","-y","-i",video,"-qscale:v","2",str(src_dir/"s%03d.jpg")],
                   check=True, capture_output=True)
    src = sorted(src_dir.glob("s*.jpg"))
    M = len(src); N = M - FADE
    print(f"{M} frames -> ciclo {N} ({N/FPS:.2f}s)")

    f0 = Image.open(src[0]); vw,vh = f0.size
    cw, ch = (CARD[2]-CARD[0])*2, (CARD[3]-CARD[1])*2
    # cover-crop do vídeo no cartão, focado na faixa do corredor (sem o campo preto do topo)
    esc = cw / vw
    alt_fonte = round(ch / esc)
    y_fonte = min(vh - alt_fonte, round(vh*0.42))
    print(f"cartão {cw//2}x{ch//2}  crop do vídeo: y={y_fonte}..{y_fonte+alt_fonte}")

    mask = Image.new("L", (cw, ch), 0)
    if RAIO:
        ImageDraw.Draw(mask).rounded_rectangle([0,0,cw-1,ch-1], radius=RAIO*2, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    else:
        ImageDraw.Draw(mask).rectangle([0,0,cw-1,ch-1], fill=255)

    # overlay de texto/logo/grid reutiliza o compositor em modo claro
    sys.path.insert(0, str(BASE))
    import compositor_video as cv
    overlay = cv.montar_overlay(
        "OBJ:Como sua empresa|atrai vende e *opera*|Mapeamos o fluxo inteiro antes de qualquer ferramenta.",
        158, None, claro=True)

    out_dir = SCRATCH/"out"; out_dir.mkdir(exist_ok=True)
    for f in out_dir.glob("*.jpg"): f.unlink()
    base_cream = Image.new("RGB", (SW, SH), CREME)

    for n in range(N):
        fr = Image.open(src[n+FADE]).convert("RGB")
        k = n - (N-FADE)
        if k >= 0:
            fr = Image.blend(fr, Image.open(src[k]).convert("RGB"), (k+1)/FADE)
        recorte = fr.crop((0, y_fonte, vw, y_fonte+alt_fonte)).resize((cw, ch), Image.LANCZOS)
        quadro = base_cream.copy()
        quadro.paste(recorte, (CARD[0]*2, CARD[1]*2), mask)
        out = quadro.convert("RGBA")
        out.alpha_composite(overlay)
        out.convert("RGB").resize((W, H), Image.LANCZOS).save(out_dir/f"f{n:03d}.jpg", quality=95)
        if n % 24 == 0: print(f"frame {n}/{N}")

    mp4 = ROOT/"SLIDE2-final.mp4"
    subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(out_dir/"f%03d.jpg"),
        "-c:v","libx264","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart","-an",str(mp4)],
        check=True, capture_output=True)
    print("ok:", mp4)

if __name__ == "__main__":
    main(sys.argv[1])
