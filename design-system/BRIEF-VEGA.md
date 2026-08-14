# Kit de Design VEGA — para Claude (claude.ai)

Você vai desenhar slides de carrossel de Instagram da VEGA como **artifacts HTML**
de 1080×1350 (4:5). Este brief é a fonte da verdade — não invente fora dele.
As imagens `ref-slide1..4.jpg` são o carrossel 01 aprovado: a régua do SISTEMA (o cenário grego delas é exemplo, não regra).


## Quem é a VEGA (definição oficial — do site)

"Da aquisição à operação. Um sistema só." A Vega desenha e opera o sistema da
empresa: anúncio, sistemas com IA e painel na mesma casa. O anúncio traz. O
sistema faz. O painel mostra. Frentes atuais: Software e IA, Marketing e Site.
(No copy criativo, "Operação, Aquisição, Marca" pode aparecer como lente sobre
a empresa DO CLIENTE — não confundir com as frentes da VEGA.)

## Sistema × Cenário — a separação que governa tudo

O SISTEMA é fixo e faz qualquer post parecer VEGA. O CENÁRIO é variável por
carrossel — o 01 usou arquitetura clássica greco-romana com tochas; os próximos
podem habitar qualquer universo visual, desde que o cenário obedeça 4 condições:

1. Paleta compatível com a da marca (dominante quente/neutra; azul só como raro)
2. Cena "silenciosa": sem letras, sem pessoas reconhecíveis, sem ruído visual
3. Uma fonte de vida para o motion (chama, nuvem, água, luz — algo que respire em loop)
4. Um elemento vertical capaz de cruzar a linha do campo (a assinatura da série)

SISTEMA (inviolável): canvas 4:5 · campo preto/creme com linha dura ~50,5% ·
elemento cruzando · Jost 200/500 com tracking e glow proporcionais · paleta hex ·
regras de copy · grid de pontos · logo 150px topo-esquerdo · jogo de cores
alternando campo ao longo do carrossel.

Tom: **calmo · caro · editorial · preciso**. Na dúvida, menos.

## Paleta (hex exatos, nada fora dela)

| Papel | Hex |
|---|---|
| Preto Cine (fundo escuro padrão) | `#050505` |
| Creme (texto no escuro; campo do slide claro) | `#F2EAD9` |
| Creme quente (palavra de ênfase) | `#F6EFDE` |
| Areia (acento discreto) | `#E7DCC6` |
| Sépia Claro (subtítulo no escuro) | `#9C8F7D` |
| Sépia 40 (subtítulo no claro) | `#6E6253` |
| Azul Vega (raro; nunca texto sobre preto) | `#1D43B8` |

Nunca `#000000` nem `#FFFFFF`. Azul só como aura/detalhe, jamais tinta de texto.

## Tipografia — Jost (arquivo em assets/jost-variable-latin.woff2)

- Headline: **Jost 200** (ExtraLight). Ênfase: **uma palavra** por bloco em
  **Jost 500** + cor `#F6EFDE`.
- Corpos de referência (1080px de largura): capa l1 72px / l2 104px;
  formato objetivo: linhas de 80px + subtítulo 31px (36px no claro).
- Tracking: letra −2,5%, palavra −10% (nas headlines).
- Glow no escuro, proporcional ao corpo: `text-shadow: 0 0 0.17em rgba(242,234,217,.30), 0 0 0.53em rgba(242,234,217,.14)`;
  ênfase: `0 0 0.10em rgba(242,234,217,.45), 0 0 0.30em rgba(242,234,217,.20)`.
  **No claro: texto `#050505` SEM glow.**

## Regras de copy (invioláveis)

- Headlines **sem nenhuma pontuação**; quebras de linha fazem o papel das vírgulas.
- **Primeira palavra de cada linha maiúscula** (inclusive linhas de continuação).
- Subtítulos podem ter pontuação. Uma ênfase por bloco.
- Quebras de linha sempre controladas — nunca deixar o navegador quebrar sozinho
  (órfã tipográfica é reprovação).

## Geometria do slide

- Canvas 1080×1350. Campo (preto ou creme) no topo até **~50,5%** da altura,
  com **borda inferior reta e dura** — é a linha do sistema.
- Grid de pontos no campo: raio ~1.2px, malha 38,5px, cor do texto a 25% de opacidade,
  esvaindo antes da linha.
- Logo no topo-esquerdo, 150px de largura, margens 70px/74px
  (assets/logo-vega.svg no escuro, logo-vega-tinta.svg no claro).
- Texto centrado no campo, no meio do vazio entre a logo e o elemento da cena.
- **Assinatura da série: UM elemento da cena atravessa a linha** e invade o campo
  (cabeça de busto, frontão, cúpula...). Nos mockups HTML, simule a cena com um
  bloco/imagem placeholder e indique onde o elemento cruzaria.
- Jogo de cores do carrossel: alternar campo preto e campo creme entre slides
  (carrossel 01: preto → creme → preto → céu estrelado no fechamento).

## O que você entrega no claude.ai

Artifacts HTML 1080×1350 (um por slide, ou um carrossel navegável) usando a fonte
via @font-face (o usuário anexa o woff2, ou use fallback `Jost, sans-serif` do
Google Fonts). Cena de fundo = placeholder (gradiente quente âmbar/sépia ou a
ref-slideN.jpg) — a cena final é gerada fora (Higgsfield) e composta no pipeline
local do usuário, junto com vídeo/loop. Seu papel: **layout, hierarquia, copy e
variações** — rápido de iterar, fiel ao sistema.

## Checklist antes de mostrar qualquer slide

- [ ] Linha do campo reta, ~50,5%
- [ ] Caixa correta em toda linha · zero pontuação em headline
- [ ] Uma ênfase por bloco (500 + creme quente)
- [ ] Glow proporcional (nunca em px fixos de outro corpo) · claro sem glow
- [ ] Nada de branco/preto puros · azul nunca como texto
- [ ] Margens ≥ 60px · texto nunca encosta no elemento que cruza
