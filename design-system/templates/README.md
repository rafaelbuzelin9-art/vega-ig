# Campo VEGA — templates de formato

O **campo** é o quadro escuro com textura de pontos onde o texto senta. Ele nunca
foi um arquivo de imagem: nasce de `../preset.css`. Esta pasta entrega o campo
já montado nos dois formatos de publicação, para quem precisa do asset pronto
em vez do código.

| Arquivo | O que é |
|---|---|
| `campo-feed-1080x1350.html` | Template editável, feed 4:5. Abre no navegador, troca o texto. |
| `campo-reel-1080x1920.html` | Template editável, reel 9:16. |
| `campo-feed-1080x1350.png` | Overlay PNG com alfa: campo + grid + logo, cena transparente. |
| `campo-reel-1080x1920.png` | Idem, no 9:16. |
| `build-campo.py` | Regera os quatro. Roda com `python3 build-campo.py`. |

## Como usar

**Os PNG são overlays.** Área da cena 100% transparente — joga por cima de
qualquer fundo (Photoshop, Figma, CapCut, Premiere) e o campo se encaixa com a
linha no lugar certo. Não têm texto, de propósito: o texto é por peça.

**Os HTML são a fonte editável.** A fonte vai embutida em base64, então o
arquivo é autossuficiente — não precisa instalar Jost. Para trocar o texto,
mexa só no bloco `.txt`:

```html
<span class="l1">Antes da tecnologia</span>
<span class="l2">Entendemos a <b class="hard">empresa</b></span>
```

`l1` é a linha menor (72px), `l2` a maior (104px), e `<b class="hard">` marca a
palavra de ênfase — **uma por bloco**. Para exportar, print da página em
1080 de largura, ou use `../../skill/vega-fontes/render.py`.

## O que muda entre feed e reel — e o que não muda

Os dois têm **1080px de largura**. Como todo o sistema tipográfico é calibrado
nessa largura, **corpo, peso, tracking, glow, grid e logo são idênticos** nos
dois formatos. Não há versão "reel" da tipografia.

Só a altura muda, e com ela a posição absoluta da linha:

| | Feed 4:5 | Reel 9:16 |
|---|---|---|
| Canvas | 1080×1350 | 1080×1920 |
| Linha do campo | 682px | 970px |
| ...em porcentagem | **50,5%** | **50,5%** |
| Topo do bloco de texto | 170px | 456px |

Os 170px do feed são o valor travado no slide 1. Os 456px do reel **não foram
inventados**: saem da regra do brief — texto centrado no vazio entre a base da
logo e a linha. Se você mudar o número de linhas do texto, recalcule por essa
regra (ou rode o `build-campo.py`), não por gosto.

## Reel — áreas de segurança do Instagram

A interface do app cobre parte da tela. No campo isso não incomoda, porque:

- O bloco de texto vive entre 456px e ~640px, bem dentro da faixa livre.
- A logo em 70/74 fica acima do texto e abaixo do gradiente do topo.
- A faixa de baixo (~450px finais), onde entram legenda, áudio e botões, cai
  **na cena**, não no campo — mantenha ali só pedra e luz, nada que precise ser lido.

Regra prática: nada legível abaixo de 1470px nem à direita de 960px.

## A linha continua sendo a linha

Borda inferior reta e dura, **um** elemento da cena atravessando. Isso vale nos
dois formatos — é a assinatura da série. Ver `../BRIEF-VEGA.md`.
