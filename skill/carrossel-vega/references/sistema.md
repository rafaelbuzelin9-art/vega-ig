# Sistema visual — preset Carrossel Atlas

## O quadro

`base-atlas.png` (1080×1350) e `@2x` (2160×2700):

- Fundo **Preto Cine `#050505`**
- Malha de pontos de **38,5px** a **20%**, ponto de raio **1,45**, contraste
  30/255. Medida na referência do Replit; os 7,5% do original somem no preto.
- **Wordmark VEGA 150px no topo ESQUERDO**, margens 70/74. Sem monograma.

A base é gerada por `base.py` no repo. Aqui ela vem pronta: **não regerar**.

## Paleta (identidade v4)

| cor | hex | uso |
|---|---|---|
| Preto Cine | `#050505` | fundo, sempre |
| Creme | `#F2EAD9` | valores, arestas de luz, palavra em glow |
| Areia | `#E7DCC6` | rótulos, luz quente do vidro |
| Azul Vega | `#1D43B8` | acento único, luz fria do vidro |
| Sépia 40 | `#6E6253` | apoio em campo claro |
| Subtítulo | `#CFC3AE` | só o subtítulo do slide |

Banido: sparkle de 4 pontas, glitter, gradiente colorido, fundo claro em peça de
marca, **branco puro** dentro do componente.

## Tipografia

Jost variable (100–900), embutida em base64 no CSS.

| elemento | corpo | peso | notas |
|---|---|---|---|
| headline `.obj` | 80px | 200 | `letter-spacing:-.025em`, `word-spacing:-.10em` |
| palavra-chave | 80px | 500 | marcada com `*asterisco*`, ganha glow |
| subtítulo `.sub` | **38px** | **300** | `#CFC3AE`, `line-height:1.34`, quebra por `\|` |
| lista `.item` | 42px | 200 | com cota `.cota` de 24px |

`txt_top` do slide 01 e 02 = **165**. Manter para o carrossel não "pular" de
slide a slide.

## Legenda em arco (slide 01)

As linhas correm em semicírculos concêntricos ao globo do Atlas, medido na
máscara do recorte (`sobre_base.py` devolve `cx, cy, r` num JSON).

- ângulo ≈ comprimento do texto ÷ raio. **Acima de ~140° a ponta vira.**
  O compositor mede o ângulo real no pixel e imprime.
- colar no globo custa corpo: cada 10px de aproximação pede ~4px a menos de
  fonte.
- linhas do arco devem ter o **mesmo número de caracteres** (o júri reprovou
  assimetria 32/29).

## Recorte de arte sobre a base

Quando a peça leva imagem (o Atlas, mármore, qualquer objeto):

1. gerar com fundo preto de estúdio;
2. `image_decompose --mode standard` no Higgsfield, ou máscara por luminância
   (portão suave 8→26; corte agressivo desconecta partes);
3. usar a camada só como **máscara** — a cor vem sempre da imagem original;
4. tapar **só furos pequenos** (<4000px²): o vão entre braço e globo também é
   buraco fechado;
5. **nunca ficar só com o maior componente** — a peça perde a esfera, e na pilha
   perde a placa que cai. Filtrar por área < 1% do maior;
6. escalar pela **largura**, não pela altura: presença é largura ocupada; altura
   resolve sangrando pela borda de baixo.

## Arco do carrossel 02

capa (tese) → volume → virada → sistema → freio → fecho.

| slide | copy fechada |
|---|---|
| 01 capa | "Talvez o problema nunca / Tenha sido uma **pessoa**" + arco "Você troca a agência, o time. / O resultado continua o mesmo." |
| 02 volume | "O problema não é a tarefa / É o **volume**" + "Um minuto por confirmação. Dois por retomada. \| Cinco por horário vago. Dezenas de vezes, todos os dias." |
| 03 virada | "O que se repete todo dia / Vira **estrutura**" |
| 04 sistema | "Quatro coisas deixaram / De depender de alguém **lembrar**" + 4 itens |
| 05 freio | "E o que ele nunca faz / **Sozinho**" |
| 06 fecho | "Trocar de gente conserta um dia / Trocar o processo conserta o **mês**" |

## O que já foi testado e DESCARTADO

Não repropor sem motivo novo:

- **Mármore gerado por IA para o slide 02** (clepsidra virou chafariz, ampulheta
  é clichê de produtividade, pilha de tabuletas ficou boa mas o Rafael quer
  pegada de tela/produto).
- **Card de vidro estilo Apple desenhado à mão** (raio 44px, corpo gigante):
  parecia widget de apresentação, não software. Reprovado duas vezes.
- **Card claro chapado** sobre o preto: sem profundidade, lê como adesivo.
- **UI gerada por IA**: Nano Banana Pro acerta a estética e inventa o texto
  miúdo ("Mermiting", "Tyarıe"). Só passa tela com 3-4 palavras e número grande.
- **Badges e linhas de apoio inventadas** ("32×/dia", "Toda vez que marcam"):
  o Rafael cortou. Só o que a copy já afirma.

## Referência de linguagem

Post do **repl.it** `DbmAzJqDlzJ`. Slides 2 a 4 de lá são vídeo com a mesma
estrutura: base intacta + logo topo-esquerda + headline de 2 linhas com uma
palavra em bold + subtítulo + **card do produto em movimento** sangrando pelo
rodapé. É de onde vem a malha de pontos e o formato do carrossel.
