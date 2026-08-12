# Preset **Carrossel Atlas**

Sistema visual do carrossel 02 da Vega Systems, fechado em 12/08/2026.
Nasceu do slide da capa (o Atlas de mármore) e virou o padrão dos slides
seguintes. Formato 1080×1350 (4:5), entrega também em 2160×2700.

## Peças

| arquivo | o que é |
|---|---|
| `base-atlas.png` / `@2x` | o quadro: Preto Cine `#050505`, malha de pontos de 38,5px a 20% com ponto de raio 1,45 (contraste 30/255) e o wordmark VEGA de 150px no topo esquerdo, margens 70/74 |
| `preset-atlas.css` | tipografia e grade do slide (Jost embutida, canvas, `.obj`, `.sub`) |
| `cards.css` | entrada do Tailwind v4 com os tokens do shadcn e os temas de cartão, inclusive o `vega-liquid` |

## Regras que o preset carrega

**A base entra intacta.** A arte só se sobrepõe, nunca corta nem escurece o
quadro. Foi o campo pintado como faixa que lia como retângulo cortando o Atlas.

**Tipografia.** Headline `.obj` em 80px peso 200, com a palavra-chave em peso
500 e glow. Subtítulo `.sub` em **38px peso 300** cor `#CFC3AE` (a 31px e peso
200 ele sumia no feed). Quebra de linha do subtítulo sempre controlada por `|`,
nunca pelo navegador.

**Cartões de dado.** A geometria é a do `card.tsx` do shadcn (registry
`new-york-v4`), medida no código e não a olho: raio 14px (`--radius` 0.625rem
+ 4), borda 1px, padding 24, gap 8 no header e 24 no card, descrição 14/400 com
line-height 20, título 30/600 tabular com `letter-spacing: normal`, sombra
`0 1px 2px rgba(0,0,0,.05)`. Só os **tokens de cor** mudam.

**Tema `vega-liquid`.** Vidro sobre o Preto Cine: `backdrop-filter` com blur e
saturação, aresta de luz em cima, sulco escuro embaixo, reflexo especular
diagonal e a luz colorida dentro do cartão. Cores da marca: Azul Vega `#1D43B8`
no alto à esquerda, Areia `#E7DCC6` na quina de baixo, arestas e valores em
Creme `#F2EAD9`, rótulo em Areia a 78%. Sem branco puro.

## Três armadilhas que custaram rodadas

1. **Sombra não existe em fundo preto.** O `shadow-xs` está lá, mas preto sobre
   `#050505` é invisível. Profundidade vem de borda clara, de superfície mais
   clara que a base ou de luz.
2. **Tailwind e `preset-atlas.css` não convivem no mesmo documento**: o
   `*{margin:0;padding:0}` anula `px-6/py-6` e o valor do cartão some. O painel
   é renderizado num documento só dele e colado no slide como PNG com alpha.
3. **Com `!important` a ordem das cascade layers inverte** e CSS fora de layer
   perde para as utilities. O bloco do vidro mora dentro de `@layer utilities`.

## Como rodar

```bash
cd carrossel-02/shadcn-ref && npm install          # tailwindcss v4 + geist
npx @tailwindcss/cli -i entrada.css -o saida.css --content "../compor.py"
cd .. && python compor.py volume                    # slide 02
python finais.py                                    # entrega 1x e 2x
```
