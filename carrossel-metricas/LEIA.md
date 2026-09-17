# Carrossel · As quatro métricas

Seis telas, 1080×1350, publicado em setembro de 2026. Capa e fecho em campo
Preto Cine, montados em código. As quatro do miolo são **fichas** desenhadas à
mão sobre folha creme, geradas no ChatGPT a partir de uma folha em branco.

`final-6-slides/` é a versão postável, na ordem. `oficina/` re-renderiza a capa
e o fecho.

## O formato de ficha

O formato veio de um reel de referência que passava quinze fichas em vinte
segundos, rápido demais para qualquer uma ser lida. Aqui elas viram slide, no
tempo do leitor. A anatomia é sempre esta ordem:

1. Título em caixa alta, com **uma palavra circulada à mão** no acento âmbar
2. Tradução em uma linha, em português de dono de negócio
3. Fórmula **dentro de colchetes grandes e escrita por extenso**, nunca em símbolo
4. Exemplo com seta e o resultado sublinhado no acento
5. Três linhas de explicação, com um colchete à direita delas
6. Um desenho anotado, em linha preta com sombra cinza e o objeto principal em
   madeira quente

Regras do prompt: letra de marcador preto, *architectural print, never a
computer font*; **um acento só**, âmbar, em exatamente dois lugares (a elipse do
título e o sublinhado do resultado); cor apenas no objeto do desenho. Acento em
português funciona, então escrever tudo acentuado desde o começo.

As quatro fichas usam a **mesma conta**: R$ 500 de gasto e 50.000 impressões.
CPM R$ 10, CTR 1% com 500 cliques, 20 conversas a R$ 25, alcance de 12.500
pessoas dando frequência 4. Dá para ler as quatro como uma campanha só.

## A linha curva da capa

A legenda em arco não é posicionada à mão: ela é **calculada a partir da
imagem**. O procedimento, que levou dez rodadas para fechar:

- ler a silhueta do objeto coluna por coluna, na própria foto já posicionada
- a linha é um **teto**, não um ajuste. Mínimos quadrados passam no meio dos
  pontos e atravessam o objeto mais alto: medir a maior invasão e subir a curva
  inteira por esse tanto
- ela tem que ser **uma curva só** (parábola, emitida como `Q`). Montada como
  polilinha de muitos pontos, cada mudança de direção vira um vinco visível
- achatar a curvatura multiplicando o termo quadrático antes de aplicar o teto

E a lição maior: enquanto o objeto era assimétrico, a linha não conseguia seguir
o desenho **e** alinhar com o bloco de texto centrado ao mesmo tempo. Quem
resolveu foi trocar a imagem por um objeto simétrico, não continuar ajustando a
curva.

## Escala tipográfica

Herdada do fecho do carrossel anterior e conferida pixel a pixel contra ele:

| Elemento | Valor |
|---|---|
| Headline | Jost 200, 80px, entrelinha 1,14, `letter-spacing` −2,5%, `word-spacing` −10% |
| Ênfase | peso 500, na última palavra |
| Frase de apoio | Jost 300, 38px |
| Arco | Jost 300, 31px |
| Corpo do fecho | Jost 300, 34px, entrelinha 1,38, cor `#CFC3AE` |

## Conferência das definições

As quatro definições foram batidas contra a central de ajuda da Meta antes de
fechar, e duas afirmações caíram nessa conferência:

- **não é o maior lance que vence o leilão.** A Meta ranqueia o lance junto com
  as taxas de ação estimadas e a qualidade do anúncio, e diz por escrito que um
  anúncio mais relevante pode vencer contra lances maiores
- **CTR se mede sobre impressões, não sobre pessoas.** A primeira versão dizia
  "de cada cem pessoas", o que contradizia a própria ficha de frequência

Duas ressalvas que ficam de fora da arte e valem na legenda: frequência é
**média**, e no gerenciador o custo por conversa aparece com o nome completo,
*custo por conversa por mensagem iniciada*.

## Armadilhas de arquivo

O gerador devolve 1122×1402 quase sempre, mas devolveu 1145×1374 uma vez e o
corte centralizado comeu o colchete de uma ficha. Medir a caixa de tinta contra
a janela antes de recortar; quando não couber, redimensionar nos dois eixos.

O creme gerado é bem mais âmbar que o `#F2EAD9` do sistema. Forçar o ganho até o
creme canônico pede 1,45 no canal azul e lava o branco da luz. O certo é igualar
as fichas entre si e deixar a decisão do creme para a direção.
