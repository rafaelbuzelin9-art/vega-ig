# -*- coding: utf-8 -*-
"""BASE VEGA — o quadro pontilhado, em preto.

Medido na referência (o slide "Prompting in Replit Design", 1038x1280):
  malha 37px  →  38,5px em 1080 de largura
  ponto ~2px de diâmetro
  contraste do ponto contra o campo: 19/255 = 7,5%

Os 7,5% da referência funcionam no claro e SOMEM no Preto Cine: 7,5% sobre 246
é um cinza; sobre 5 é 24, que o feed come. Por isso a base sai em três níveis
de opacidade, para escolher com o olho e não no palpite.
"""
import base64, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
DS = AQUI.parent / "design-system"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H = 1080, 1350

MALHA = 38.5          # medido na referência
# (nome, opacidade, raio). O raio da referência é 1,05px; no preto vale testar
# um ponto mais gordo, porque a recompressão do feed come detalhe de 2px.
NIVEIS = [("20g", .20, 1.45)]      # nível travado: 30/255 de contraste real

FONTE = base64.b64encode(
    (DS / "assets" / "jost-variable-latin.woff2").read_bytes()).decode()
LOGO = (DS / "assets" / "logo-vega.svg").read_text(encoding="utf-8")
# o símbolo da marca é o monograma da v4 (V habitado por Lyra + estrela de
# seis raios). Vem de arquivo, nunca redesenhado — regra do repo da Vega.
MONO = (DS / "assets" / "vega-monograma.svg").read_text(encoding="utf-8")
MONO_W = 52           # pequeno: presença de assinatura, não de logo


def render(nome, op, RAIO):
    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Jost';src:url(data:font/woff2;base64,{FONTE}) format('woff2');
  font-weight:100 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#050505}}
.canvas{{position:relative;width:{W}px;height:{H}px;background:#050505}}
/* a malha cobre o quadro inteiro: é a folha, não só o campo do texto */
.grid{{position:absolute;inset:0;
  background-image:radial-gradient(circle at center,
     rgba(242,234,217,{op}) {RAIO}px, transparent {RAIO + .1}px);
  background-size:{MALHA}px {MALHA}px}}
/* Wordmark sozinho no topo ESQUERDO, 150px, margens 70/74 do sistema.
   O monograma saiu: com o wordmark à esquerda os dois brigavam pelo mesmo
   canto, e a marca já se apresenta inteira nas letras. */
.logo{{position:absolute;top:70px;left:74px;width:150px;line-height:0}}
.logo svg{{width:100%;height:auto;display:block}}
</style></head><body>
<div class="canvas"><div class="grid"></div>
<div class="logo">{LOGO}</div></div>
</body></html>"""
    pag = AQUI / f"_base_{nome}.html"
    pag.write_text(html, encoding="utf-8")
    shot = AQUI / f"_shot_base_{nome}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--no-sandbox", "--force-device-scale-factor=2",
                    f"--window-size={W},{H}", "--virtual-time-budget=4000",
                    "--allow-file-access-from-files",
                    f"--screenshot={shot.as_posix()}", pag.as_uri()],
                   check=True, capture_output=True)
    saida = AQUI / f"BASE-vega-{nome}.png"
    hi = Image.open(shot).convert("RGB")
    hi.save(AQUI / f"BASE-vega-{nome}@2x.png")     # 2160x2700, sem reamostrar
    hi.resize((W, H), Image.LANCZOS).save(saida)

    import numpy as np
    a = np.asarray(Image.open(saida).convert("L")).astype(np.float32)
    reg = a[700:1100, 300:800]
    print(f"BASE-vega-{nome}.png  fundo {np.percentile(reg,10):.0f}  "
          f"ponto {np.percentile(reg,99.7):.0f}  "
          f"contraste {np.percentile(reg,99.7)-np.percentile(reg,10):.0f}/255")
    return saida


def prancha(arqs):
    """Miniatura para julgar presença no feed + crop 1:1 para julgar o ponto.
    Julgar só na miniatura engana: o feed reduz, mas o olho de perto não."""
    LARG = 300
    ALT = round(LARG * H / W)
    CS = 300                                   # lado do crop 1:1
    M, G, R = 36, 22, 52
    n = len(arqs)
    board = Image.new("RGB", (M * 2 + LARG * n + G * (n - 1),
                              M * 2 + ALT + R + CS + R), (12, 11, 10))
    dr = ImageDraw.Draw(board)
    f = ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 22)
    fm = ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 18)
    for i, (arq, rot) in enumerate(arqs):
        im = Image.open(arq)
        x = M + i * (LARG + G)
        board.paste(im.resize((LARG, ALT), Image.LANCZOS), (x, M))
        dr.text((x + LARG / 2, M + ALT + 12), rot, font=f,
                fill=(226, 219, 205), anchor="ma")
        y = M + ALT + R + 10
        board.paste(im.crop((390, 500, 390 + CS, 500 + CS)), (x, y))
        dr.text((x + LARG / 2, y + CS + 10), "1:1", font=fm,
                fill=(140, 128, 110), anchor="ma")
    board.save(AQUI / "PRANCHA-base.png")
    print("PRANCHA-base.png")


if __name__ == "__main__":
    saidas = [(render(n, op, r),
               f"{int(op*100)}%" + (" · ponto gordo" if r > 1.2 else ""))
              for n, op, r in NIVEIS]
    prancha(saidas)
