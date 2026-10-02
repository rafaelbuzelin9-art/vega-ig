# Reel do Faísca (publicado em 02/out/2026)

Reel 9:16 de 51,9 s sobre o agente de WhatsApp da gráfica parceira (o agente real chama
Tico; no vídeo virou **Faísca**, filhote de fênix em pixel art). Sem faturamento, sem
nome do cliente. Fonte dos números: `Tico_resultados_WhatsApp.pdf` (Drive, pasta do post).

## Onde está cada coisa

| O quê | Onde |
|---|---|
| Takes (Seedance 2.5, 480p), elements, upscale final | Higgsfield, projeto `@vegasystems/faisca` + histórico de jobs |
| Narração gravada pelo Rafael (8 m4a) e PDF dos números | Drive `Mãe/Vega/Posts/13 Reel - Faisca/` |
| Ferramentas de pós (gráfico, telas, cartelas, legenda, capturador) | esta pasta, `grafico/` |
| Vídeo publicado | Instagram da VEGA (e o job de upscale no Higgsfield) |

Nada de mídia neste repositório.

## Como o corte foi montado (ffmpeg, 24 fps, crf 14)

Takes de 480x854. Tudo via filtro `concat` com streams explícitos (o demuxer de concat
deu 236 s de duração fantasma).

| Trecho | Receita |
|---|---|
| C1 TV | take inteiro (5 s) |
| C2 laptop | `trim 0–3 setpts 0.5` + `3–6 setpts 1.6`; gráfico A compacto na tela por `tela-c2.html?inicio=1.35`; último 1 s com zoom-out pro preto (PIL, escala 1→0.3 + brilho→0) |
| C3 celular | `0–2.4 /2` (chegada no escuro em 2x) + `2.4–2.6` normal + `2.6–5 ×2.5` (mensagens em câmera lenta); áudio `atempo` correspondente |
| Mergulho | sequel do C3, `-ss 2.65 -t 2.1` |
| Cartela | último quadro do mergulho congelado + `cartela-gelo.html?t1=1.3&t2=1.6`, 6,4 s |
| C5 dinheiro | `trim 2.2–4.6 /2.1818` + resto normal (4,58 s) |
| C6 loja | `trim 0–3.6 /1.6` + resto normal |
| C7 rua | C7a + C7b concatenados e `setpts /1.12`, `atempo 1.12` |
| Fim | `cartela-fim.html` (véu 0,55 + logo v5 creme), 2,4 s |

Narração: m4a do gravador → `silenceremove` nas duas pontas, `highpass 80`,
`acompressor -20dB 2.5:1`, `loudnorm I=-16 TP=-1.5`. Som dos takes a `volume 0.4`.
Mix: `amix inputs=9 normalize=0`, cada faixa com `adelay`. Deixas (s): T1 1,30 · T2 7,17 ·
T3 12,33 · T4 18,71 · T5 22,80 · T6 30,38 · T7 34,06 · T8 (atempo 1,12) 38,71.

## Legenda queimada

`grafico/legenda.html` renderizado com `capturar.mjs` (`ALPHA=1 DUR=51.9 W=480 H=854 FPS=24`)
e colado com `overlay=format=auto`. Texto = fala dele **palavra por palavra** (ele reprovou a
versão resumida). Tempos por `whisper-cli -m ggml-small.bin -l pt -ml 1 -sow -oj`, conferidos
com faster-whisper medium. Estilo: Jost 200 creme #F2EAD9 30 px, UMA palavra em 500 por
frase, faixa `rgba(4,4,4,.42)` raio 12, `bottom:196px`, `text-wrap:balance`, fundido 0,12 s.

## Telas compostas

- Gráfico: `grafico.html?compacto=1` (1600x1000, renderizado a 30 fps) → canvas 640x400 com
  `imageSmoothingQuality=high` → `matrix3d` (homografia) para os 4 cantos da tela lidos em
  ampliação 6x. Cantos lidos no olho, não por máscara automática.
- Tela do celular (`tela-c3c4.html`, `rastrear.py` com ECC do OpenCV) foi feita e depois
  **removida** do corte: ele preferiu o take cru.

## Upscale (custos lidos na tela em 02/out, 52 s 480p 9:16)

ByteDance Upscale Pro 1080p 30 fps = 10,38 cr (usado) · ByteDance 2K = 20,76 · Topaz 1x = 77.
Pela UI `higgsfield.ai/upscale`: input de arquivo escondido (`find "hidden file input"` +
file_upload, limite 10 MB → reencodar crf 17). O botão pago é do Rafael.

## Erros desta produção e a regra que ficou

1. **"Celular nunca desliza" no prompt matou o tremelique** que ele gostava. Não negar
   movimento que o take anterior já tinha; descrever o que muda, não o que congela.
2. **Tela preta sobre o celular** (3 rodadas de homografia + rastreio) e no fim ele
   mandou tirar. Antes de compor sobre objeto que se move, perguntar se o take cru serve.
3. **Legenda resumida**: ele quer a fala literal. Transcrever, não escrever.
4. **Áudio do WhatsApp (PTT opus)** é inservível para narração; gravar no gravador e
   mandar o arquivo.
5. **"Esse é o Faísca" tem que entrar quando ele aparece** (deixa pela imagem, não pelo
   começo do take).
6. **/private/tmp evaporou com o reinício** e levou a oficina; as ferramentas só voltaram
   porque estavam no transcript. Subir a pasta de ferramentas pro GitHub no fim de cada
   sessão, não no fim do projeto.
7. **Saldo caiu 19,35 e não 10,38** no upscale: provável clique duplo. Conferir o
   histórico de jobs antes de clicar de novo.
8. `blend=lighten` em yuv420p vira rosa (usar `format=gbrp`), e overlay RGBA é mais
   simples que blend.
9. bash 3 do Mac não tem array associativo: cálculos de deixa em Python.
10. ChatGPT via Chrome: `type` longo congela a aba; colar pela área de transferência.
