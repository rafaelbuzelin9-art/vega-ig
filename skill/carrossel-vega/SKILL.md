---
name: carrossel-vega
description: >-
  Produz slides e vídeos do carrossel da Vega Systems no preset "Carrossel Atlas":
  quadro Preto Cine com malha de pontos e wordmark, headline em Jost com palavra em
  glow, subtítulo 38px, e painéis de dado construídos com o CARD REAL do shadcn
  (registry new-york-v4) em tema liquid glass com a paleta da marca. Inclui o motor
  de composição (Chrome headless + PIL), o recorte de arte sobre a base, e a
  animação de cursor clicando com números que sobem (puppeteer quadro a quadro +
  ffmpeg). Use para: criar ou refazer slide do carrossel da Vega, montar painel de
  métricas na identidade, animar um slide, copiar um componente de UI de referência
  para dentro da peça. NOT for: filme de marca de 20-30s (filme-editorial), prompt
  de imagem IA (image-prompt-builder), copy das placas (juri-de-copy).
  Triggers — "slide do carrossel", "carrossel da vega", "carrossel atlas", "slide 02",
  "painel de métricas vega", "card liquid glass", "anima o slide", "cursor clicando",
  "preset atlas", "base vega", "refazer o slide".
---

# Carrossel Vega — preset Carrossel Atlas

Sistema fechado em 12/08/2026 nos slides 01 e 02 do carrossel 02. Formato
1080×1350 (4:5), entrega também em 2160×2700.

**Fonte da verdade:** repo `vega-ig` (github.com/rafaelbuzelin9-art/vega-ig),
pasta `design-system/presets/carrossel-atlas/` e a produção em `carrossel-02/`.
Os arquivos aqui em `assets/` são cópias autônomas, para a skill funcionar mesmo
fora do repo.

## O que existe aqui

| pasta | conteúdo |
|---|---|
| `assets/` | `base-atlas.png` (+@2x), `preset.css`, `cards.css`, `jost-variable-latin.woff2`, `vega-lockup.svg` |
| `scripts/` | `compor.py` (slide), `anima.py` (vídeo), `captura.js` (quadro a quadro) |
| `references/` | `sistema.md` (medidas e regras), `componentes.md` (o card e os temas), `motion.md` (a animação) |

## Fluxo

**1. Preparar o CSS dos cartões** (uma vez por máquina):

```bash
cd <pasta-de-trabalho> && mkdir -p shadcn-ref && cd shadcn-ref
npm init -y && npm i -D tailwindcss @tailwindcss/cli && npm i puppeteer-core
cp <skill>/assets/cards.css entrada.css
npx @tailwindcss/cli -i entrada.css -o saida.css --content "../compor.py,../anima.py"
```

**2. Compor o slide.** Copie `scripts/compor.py`, declare o slide no dicionário
`SLIDES` e rode `python compor.py <nome>`. Ele monta HTML, screenshota no Chrome
em 2x, reduz para 1080×1350 e imprime as margens laterais do texto como
guardrail.

**3. Animar** (opcional): `python anima.py <nome>` varre o tempo com puppeteer e
fecha o MP4 no ffmpeg.

**Sempre abrir o resultado** com `Invoke-Item` logo depois de gerar. O Rafael
não vê o que só é lido pela ferramenta.

## As cinco regras que não se negociam

1. **A base entra intacta.** A arte se sobrepõe, nunca corta nem escurece o
   quadro. Campo pintado como faixa lê como retângulo cortando a peça.
2. **Subtítulo 38px peso 300** (`#CFC3AE`). A 31px e peso 200 ele sumia no feed.
   Quebra de linha do subtítulo é controlada por `|`, nunca pelo navegador.
3. **Componente de UI se copia do código, não do olho.** Baixe o registry
   (`ui.shadcn.com/r/styles/new-york-v4/<bloco>.json`), leia as classes, meça o
   computed style no navegador. Estimar proporção pelo screenshot erra tudo.
4. **Sombra não existe em fundo preto.** Profundidade vem de borda clara, de
   superfície mais clara que a base, ou de luz.
5. **Nunca inventar dado.** Rótulo e valor saem da copy aprovada; badge,
   variação e linha de apoio só entram se o Rafael der o número.

## Antes de construir, travar a direção

Projeto criativo da Vega começa por direção, não por build. Proponha conceitos
divergentes, reaja junto, e só depois componha. Ver `references/sistema.md` para
o arco do carrossel 02 e o que já foi descartado (mármore gerado por IA, cartão
de vidro estilo Apple, card claro chapado).
