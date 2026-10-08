# Receita: carrossel e reel "Anúncio fraco, ok, forte" (08/out/2026)

## Arquivos
- `index.html`: os 10 slides 1080x1350. `?s=N` mostra um slide sozinho; sem parâmetro, a prancha.
- `render.sh`: exporta os slides (Chrome --headless=old a 2x + sips para 1080). Precisa do servidor: `python3 -m http.server 8791` nesta pasta.
- `reel.html`: o reel 1080x1920. Reaproveita CSS e textos do index; `render(t)` desenha o quadro do tempo t.
- `cap.mjs`: captura quadro a quadro via CDP e manda para o ffmpeg. `node --experimental-websocket cap.mjs saida.mp4 30` (ou `cap.mjs prefixo 30 0,1.5,3` para PNGs de teste).
- `assets/`: Jost variável, Inter 300/400, Anton (só na abertura do reel), lockups v5 de peça.

## Sistema visual usado
- Fundo preto: #050505, malha 38,5 px, ponto creme rgba(242,234,217,.20) r1,2, `background-position:0 0`. Conferido contra posts publicados (métricas, Horários vagos, Qual criativo).
- Fundo claro: #F2EAD9, malha 38,5, ponto preto .13. Igual a "períodos do tráfego" e "Marketing vs Branding".
- Jost 200 + UMA palavra 500 por tela; Inter 300 no corpo; logo só na capa.
- Fraco/ok/forte = magnitude: moldura 2 px creme a 40%/70%/100% e régua com estrela que cresce.

## Áudio da abertura do reel (BIIII)
```
ffmpeg -f lavfi -i "aevalsrc='0.5*sgn(sin(2*PI*740*t))+0.35*(2*mod(370*t,1)-1)+0.15*sin(2*PI*1480*t)':s=48000:d=1.15" \
 -af "afade=t=in:d=0.004,afade=t=out:st=1.12:d=0.03,asoftclip=type=hard:threshold=0.8,lowpass=f=9000,highpass=f=150,acompressor=threshold=-12dB:ratio=6:attack=1:release=40,volume=6dB,alimiter=limit=0.88:attack=0.5:release=20:level=0,aformat=channel_layouts=stereo" -ar 48000 abertura.wav
ffmpeg -i reel-mudo.mp4 -i abertura.wav -filter_complex "[1]apad[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart reel.mp4
```

## Erros desta produção e a regra de cada um
1. Copiei o acabamento da referência (blocos azuis cheios, Jost 400/600, fundo creme dominante): "fugiu da identidade". Regra: ler `vega-systems/brand/IDENTIDADE-VISUAL.md` antes de desenhar, mesmo em cópia; da referência vem só a estrutura.
2. Inventei uma aura azul que nenhum post publicado tem. Regra: efeito de luz só se existir em post aprovado.
3. Usei `fundo-preto-completo` do kit (malha 26 px) como "fundo oficial". Não é o fundo do feed. Regra: medir contra slides baixados do IG publicado.
4. Pesquisa rasa: olhei só os 2 posts mais recentes e concluí "o feed é creme". O feed tem post preto e creme. Regra: levantar todos os posts estáticos do perfil antes de concluir.
5. A tremida da abertura não aparecia: a timeline genérica sobrescrevia o `transform`. Regra: verificar movimento medindo posição em quadros do MP4, não em miniaturas.
6. Áudio: a buzina em acorde soou "tocada", e um pico passou de 0 dBFS. Regra: "susto" é uma nota única áspera; sempre medir com `ebur128=peak=true` e manter pico abaixo de -1.
7. CTA "Comenta MODEL" exige ferramenta de automação (ManyChat). Sem ferramenta, usar "Manda MODEL no direct" e a resposta instantânea nativa.
