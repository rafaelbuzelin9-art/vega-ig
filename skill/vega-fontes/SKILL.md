---
name: vega-fontes
description: Produz carrosséis de Instagram da VEGA no sistema visual aprovado — campo preto/creme com linha dura, Jost, cenário variável por carrossel (o 01 foi arquitetura clássica com tochas), loops de vídeo. Cobre prompts de geração (Higgsfield), composição de stills e vídeos com texto, costura de loop e upscale. Use quando o pedido for novo carrossel VEGA, novo slide, ajuste de texto/linha/campo numa peça existente, ou adaptação do sistema para outro formato.
---

# Carrossel VEGA — sistema de produção

Pipeline validado no carrossel 01 (ago/2026). A regra de ouro: **generativo só no fundo; tipografia, logo, campo, linha e loop são código.**

## Arquitetura da peça (1080×1350, 4:5)

```
CAMPO (preto #050505 ou creme #F2EAD9) ─ linha DURA em ~50.5% (ajustável por slide)
├── grid de pontos 26px (creme 10% no escuro / preto 10% no claro)
├── logo topo-esq caixa 250px (vega-lockup.svg no escuro / vega-lockup-tinta.svg no claro)
├── texto Jost centrado  +  UM elemento da cena cruzando a linha (assinatura)
CENA (gerada) ─ arquitetura clássica, tochas âmbar, loop de vídeo
```

## Fluxo completo de um slide

1. **Prompt de imagem** (usuário roda na UI Higgsfield, GPT Image 2, 3:4, 4 variações).
   Estrutura STYLE/SUBJECT/COMPOSITION/LIGHT; **sem bloco negativo** (restrições em
   afirmação: `uninhabited`, `bare unmarked stone`, `never white`). Style key fixo +
   frase de cruzamento comprovada: `Only the <elemento> rises past the dividing
   line, breaking it clearly against the black, while all the rest of the black
   field stays pure and empty.` Ver `references/REGRAS.md`.
2. **Motion** (opcional): usuário salva a imagem como element e anima no Seedance 2.0
   (6s · 1080p · Auto). Prompt SÓ de movimento, câmera travada, lista nominal do que
   congela, `never white`, `the sky never brightens` em noturnos.
3. **Upscale** (vídeo): CLI autenticado —
   `higgsfield generate create bytedance_video_upscale --video <raw.mp4> --model_version pro --preset aigc --resolution 2k --fps 24 --wait`
4. **Composição**: scripts desta skill (rodar da pasta do projeto, que precisa ter
   `fonts/`, `vega-lockup*.svg`, `preset.css` — ou usar os desta skill).
   - Still: `python3 render.py <n>` (config no dicionário `SLIDES` do script)
   - Vídeo: `python3 compositor_video.py <video.mp4> <n> "<modo:texto>" [l1|-] [txt_top|-] [align] [claro]`
   - Claro com cena full-bleed sem cruzamento: `python3 card_claro.py <video.mp4>` (edite CARD/RAIO/texto no script)
5. Entregar em pasta `Downloads/VEGA - .../slide N.png|mp4`.

## Modos de texto do compositor

| Modo | Sintaxe | Uso |
|---|---|---|
| padrão | `"Como ela *atrai*"` + arg l1 opcional | frase única ou 2 linhas (l1 72px + l2 104px) |
| `OBJ:` | `OBJ:linha1\|linha2\|...\|subtítulo` | objetivo centrado, N linhas 80px + sub |
| `OBJL:` | idem | objetivo alinhado à esquerda |
| `WORDS:` | `WORDS:A\|B\|C` | palavras em fileira (Jost 500, 56px, gap 18) |
| `WSTACK:` | idem | palavras empilhadas à esquerda |

`*palavra*` = ênfase (Jost 500 + glow curto). `claro` como último argumento inverte o
campo para creme (texto Preto Cine, sub Sépia 40, logo tinta, sem constelação).

## O que o compositor faz sozinho

- Detecta a linha do campo (fração de claros, faixa 30–62%) e crava no alvo
  (`align`, padrão 0.505); linha alta demais → **padding de campo invisível**.
- Redesenha o campo com **borda dura matemática**; acima da linha sobrevive só o
  componente conectado à linha pela região central (a assinatura de UM elemento).
  No claro, interseção com brilho + segunda conectividade (mata lascas e ilhas).
- Costura o **loop** (último 1s crossfade no primeiro) e mantém a constelação em
  fase com o ciclo.
- Centra o texto no vazio real medido (logo → topo do elemento que cruza).

## Decisões que já foram tomadas (não reabrir sem pedido)

Ver `references/REGRAS.md` para a lista completa: tipografia e tracking, regra de
copy (sem pontuação nos headlines, inicial maiúscula por linha; subtítulos aceitam
pontuação), glow proporcional ao corpo, iluminação de tochas em interiores, paleta,
e as lições de produção (glow largo engorda letra, peso custa largura, upscale de
IA nunca por cima de tipografia, starfield exige reamostragem única).

## Guardrails de produção (obrigatório)

Antes de produzir, ler `references/GUARDRAILS.md` — 13 regras destiladas do
post-mortem da produção 01, organizadas por momento do fluxo. As inegociáveis:
handshake de todo arquivo recebido (ecoar nome/dimensões/conteúdo antes de
medir), piloto de 1 frame antes de qualquer lote, menu de opções só com
candidatos pré-validados (texto real composto), desistência em 2 rodadas com a
alternativa simples como candidata A, conclusão só pelo artefato verificado, e
prancha de contato do conjunto a cada 2-3 peças.

## Troubleshooting rápido

- **Filtro de copyright no Seedance** (falso positivo Parthenon): retry 2-3×; trocar
  vocabulário (`building/gable`, nunca `temple/Doric` no motion); espelhar o element;
  último recurso Kling 3.0.
- **Linha fora do alcance do corte**: o padding automático resolve linha alta;
  linha baixa clampa no limite físico (~54–59%) — aceitar ou regerar.
- **Artefato no campo claro**: é lasca de preto do vídeo na máscara — o pipeline
  atual já intersecta com brilho e refaz conectividade; se persistir, usar
  `card_claro.py` (linha reta, sem cruzamento — sempre limpo).
