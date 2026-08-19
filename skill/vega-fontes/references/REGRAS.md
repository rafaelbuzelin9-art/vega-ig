# Preset — Carrossel VEGA v1

Travado no slide 1 em 05/ago/2026. Fonte da verdade: `build/preset.css`.

## Como renderizar

```bash
python3 build/render.py      # todos
python3 build/render.py 2    # só o slide 2
```

Antes: salve o fundo gerado em `fundos/slideN-raw.png` e adicione a entrada em `SLIDES`, dentro de `render.py`. Ênfase se marca com asterisco: `Entendemos a *empresa*`.

## Valores travados

| | |
|---|---|
| Canvas | 1080×1350 (4:5) |
| Fundo | gerado em 3:4, cortado pelo topo |
| Preto | `#050505` — preto puro é levantado no render |
| Grid | pontos 38,5px, creme a 25%, ponto 1,2px, de borda a borda (v2, 13/ago/2026) |
| Logo | `vega-lockup.svg` (v5), caixa 250px, topo 43 / esq 47 — tinta na margem 74, cap na linha 101 |
| Texto | centralizado, topo 170, entrelinha 105% |
| Linha 1 | Jost 200, 72px, `#F2EAD9` |
| Linha 2 | Jost 200, 104px, `nowrap` |
| Ênfase | Jost 500, `#F6EFDE` |
| Tracking | letra −2,5% · palavra −10% |
| Glow geral | `0 0 18px .30` + `0 0 55px .14` |
| Glow da ênfase | `0 0 10px .45` + `0 0 30px .20` |

## Campo de pontos — v2 (13/ago/2026)

O fundo-base novo (`VEGA-fundo-base.png`, 1080×1350) virou o padrão do campo
escuro. Medido do arquivo e reproduzido em CSS, não em imagem — assim escala
para qualquer formato sem borrar o ponto:

```css
background-image:radial-gradient(circle at center,rgba(242,234,217,.25) 1.2px,transparent 1.3px);
background-size:38.5px 38.5px;   /* 28 colunas em 1080, primeiro centro em x=19 */
```

Piso `#050505`, pontos de borda a borda (o v1 esvaía 12% antes da linha; a
classe `.grid.esvai-v1` guarda esse comportamento para refazer peça antiga).
Conferência numérica contra o arquivo: piso 5, pico (61,59,55) contra
(60,58,55) do alvo. Logo do fundo-base = `vega-lockup.svg` caixa 250px, topo 43 / esq
74 — igual ao preset, não mudou.

## Cinco coisas aprendidas — não repetir

**Glow largo engorda a letra.** Halo de 60px+ sangra para dentro das hastes e o olho lê como fonte mais grossa. Raio curto com opacidade alta brilha sem engordar. Foi o que fazia a Jost 200 parecer 400.

**Tracking em `em` vai nas linhas, não no contêiner.** `em` resolve contra o `font-size` do próprio elemento. No `.txt`, que não tem corpo declarado, herda 16px e o valor vira fração de pixel.

**Peso custa largura.** `empresa` em 500 força a linha 2 a 104px; em 200 ela cabe em 108px. Corpo grande e peso alto não coexistem no máximo.

**Tamanho e peso são independentes.** Aumentar o corpo de uma linha não deve levar o peso junto — a referência aumenta `Design` mantendo 200, e reserva peso para uma palavra só.

**Ênfase por luz é mais discreta que por peso.** Se a palavra precisa firmar, 500 resolve; acima disso vira mancha.

## Regra de copy (todas as peças)

- **Nenhuma pontuação** — sem vírgula, sem ponto final
- **Inicial maiúscula na primeira palavra de cada linha**
- Ex.: `Depois` / `Conectamos tudo` · `Antes da tecnologia` / `Entendemos a empresa`

## Regra de iluminação — áreas internas (slides 4+)

Aprovada no slide 4, vale para TODA cena interna do carrossel (5, 6, 7):
tochas em suportes de ferro como fonte de luz primária, chamas altas e vivas
em âmbar/ouro (nunca branco), pools de luz quente na pedra, bolsões de sombra
profunda entre os elementos. No prompt, o bloco LIGHT deve carregar:

```
lit primarily by its torches — strong dancing firelight in deep amber and
gold, throwing warm pools across the stone. Pockets of deep shadow give the
fire room to breathe. The flames burn bright but stay amber and gold, never
white.
```

## Prompt — style key dos fundos

Prefixo idêntico nos 8 slides:

```
STYLE: Cinematic classical photography, warm golden hour light, cream marble
and limestone, amber and sepia palette, 50mm, fine film grain. Editorial,
restrained, expensive.
```

Sem bloco de negativas — os modelos Higgsfield não expõem `negative_prompt`.
As restrições vão como afirmação, no fim do bloco LIGHT:

```
Silent and uninhabited. Every element antique. The palette stays entirely in
warm cream, amber and sepia. Softest highlight is warm cream. Bare, unmarked
stone surfaces.
```

Proporção `3:4` no Higgsfield — 4:5 não existe lá. O corte é feito no render.

## Camadas por slide

1. **Fundo** — Higgsfield, sem texto, sem traço azul, sem logo
2. **Grid + logo + texto** — este preset
3. **Traço azul** — SVG animado, núcleo `#D9E4FF` sobre aura `#1D43B8` (slides 2–7)
4. **Composição em vídeo** — `ffmpeg overlay`, nos slides com movimento

## Formatos objetivos (versão 4 slides, ago/2026)

- Headline 80px Jost 200, N linhas controladas (nunca deixar quebra automática —
  órfã tipográfica); subtítulo 31px escuro / 36px claro, Sépia Claro #9C8F7D no
  preto, Sépia 40 #6E6253 no creme, pontuação permitida só no subtítulo.
- Campo claro: creme #F2EAD9, texto Preto Cine #050505 sem glow, logo tinta.
- Jogo de cores do carrossel 4: preto → creme → preto → céu estrelado.
- Estrutura clara full-bleed (card_claro.py): creme em cima com linha reta,
  cena até as bordas embaixo — usar quando o cruzamento não for viável.

## Upscale

- Vídeo: bytedance_video_upscale, model_version pro, preset aigc, 2k, fps 24 (CLI).
- Nunca upscalar por cima de tipografia composta — sempre o fundo cru, texto depois.
- Still 2480px de fonte não precisa de upscale para entrega 1080.
- Céu estrelado: UMA reamostragem da fonte nativa + UnsharpMask leve
  (estrela sub-pixel morre a cada resize extra).


## Sistema × Cenário (decisão de ago/2026)

O universo visual (cenário) é VARIÁVEL por carrossel — grego foi o do 01, não é
regra. Todo cenário novo precisa de: paleta compatível (quente/neutra), cena
silenciosa (sem letras/pessoas), uma fonte de vida para o loop (chama/nuvem/
água/luz), e um elemento vertical que cruze a linha. O SISTEMA (campo, linha,
tipografia, paleta, copy, grid, logo, jogo preto/creme) é o que não muda.
