# Componentes — o card do shadcn dentro da peça da Vega

## De onde ele veio

Referência escolhida pelo Rafael: **`dashboard-01` do shadcn**
(`ui.shadcn.com/blocks/dashboard`, o "Acme Inc."), depois de duas reprovações de
cartão desenhado à mão. O componente **não é imitado, é o deles**: mesmo markup,
mesmo CSS, só os tokens de cor mudam.

Para buscar de novo, ou trocar de bloco:

```bash
curl -s "https://ui.shadcn.com/r/styles/new-york-v4/dashboard-01.json" -o d1.json
curl -s "https://ui.shadcn.com/r/styles/new-york-v4/card.json"        -o card.json
curl -s "https://ui.shadcn.com/r/colors/neutral.json"                 -o cores.json
```

## Medidas oficiais (medidas no computed style, não estimadas)

| propriedade | valor |
|---|---|
| raio | **14px** (`--radius` 0.625rem + 4, via `--radius-xl`) |
| borda | 1px `oklch(0.922 0 0)` |
| padding | 24px (py-6 / px-6) |
| gap header (descrição → título) | 8px |
| gap card (header → footer) | 24px |
| descrição | 14px, peso 400, `oklch(0.556 0 0)`, line-height 20px |
| título | 30px, peso **600**, tabular-nums, line-height 30px, `letter-spacing: normal` |
| sombra | `shadow-xs` = `0 1px 2px rgba(0,0,0,.05)` |
| degradê | `bg-gradient-to-t from-primary/5 to-card` — escurece o **pé**, neutro |
| grade | `gap-4` (16px), `@xl/main:grid-cols-2`, `@5xl/main:grid-cols-4` |

O markup, com os componentes `Card*` expandidos:

```html
<div data-slot="card" class="@container/card flex flex-col gap-6 rounded-xl border
     bg-card py-6 text-card-foreground shadow-xs bg-gradient-to-t from-primary/5 to-card">
  <div data-slot="card-header" class="grid auto-rows-min grid-rows-[auto_auto]
       items-start gap-2 px-6">
    <div data-slot="card-description" class="text-sm text-muted-foreground">Confirmação</div>
    <div data-slot="card-title" class="leading-none font-semibold text-2xl tabular-nums
         @[250px]/card:text-3xl"><span class="valor">1</span> min</div>
  </div>
</div>
```

## Temas (em `assets/cards.css`)

Todos entram pelos **mesmos tokens** do shadcn, então a geometria nunca muda.

- `vega` — card creme `#F7F1E3` sobre o Preto Cine. Contraste alto, mas chapado.
- `vega-halo` — o claro com contorno fechado e luz difusa em volta.
- `vega-dark` — os tokens dark do próprio shadcn (`card oklch(0.205)`, borda
  branca 10%). Profundidade correta e discreta.
- **`vega-liquid` — o ESCOLHIDO.** Vidro: `backdrop-filter: blur(22px)
  saturate(170%) brightness(1.10)`, aresta de luz de 1,5px em cima, sulco escuro
  embaixo, reflexo especular diagonal e um segundo reflexo curto na quina de
  baixo (é ele que dá espessura). Luz **dentro** do cartão: Azul Vega no alto à
  esquerda, Areia na quina de baixo. Raio sobe para 28px. Texto em Creme, rótulo
  em Areia a 78%.

## Quatro armadilhas que custaram rodadas

1. **Tailwind e `preset.css` não convivem no mesmo documento.** O
   `*{margin:0;padding:0}` do preset anula `px-6/py-6` e o valor do cartão some.
   Solução: o painel é renderizado num **documento só dele** e colado no slide
   como PNG (`painel_png` no `compor.py`).
2. **Com `!important` a ordem das cascade layers INVERTE**, e CSS fora de layer
   fica com a menor prioridade — o `bg-gradient-to-t` do Tailwind vencia o
   gradiente do vidro. O bloco do vidro mora dentro de `@layer utilities`.
3. **`font-family:'Jost'` tem que ser declarado no componente**, senão ele cai em
   serifa (o preset não alcança o documento do painel).
4. **Vidro precisa de fundo.** O documento do painel carrega a MESMA base do
   slide, deslocada para a posição exata (`background: url(base) -esq -top`),
   senão o `backdrop-filter` não tem o que borrar e o vidro vira plástico fosco.
   Como a base é a mesma, a malha continua alinhada quando o PNG é colado.
5. **Luz colorida fica DENTRO do cartão.** No documento, atrás dos cartões, ela
   vaza pelos vãos e denuncia o retângulo colado no slide.

## Layout do painel no quadro 4:5

Sem o badge e o rodapé do original, o card largo fica com um vazio à direita.
No formato **vertical** (coluna única, escolha do Rafael para o slide 02):

```python
"card": {"top": 580, "larg": 300, "zoom": 1.52, "alt": 780, "tema": "vega-liquid",
         "metricas": [{"rot": "Confirmação", "alvo": 1, "un": "min", "ini": 0.06}, ...]}
```

`larg` é a largura ANTES do zoom; o zoom amplia a geometria inteira do shadcn
sem distorcer proporção. Em fileira de quatro, os cards ficam magros num 4:5;
em 2×2 funcionam bem (é como o próprio `dashboard-01` se reorganiza fora de tela
larga).
