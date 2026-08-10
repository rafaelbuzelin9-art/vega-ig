# VEGA · IG

Tudo que produz os criativos de Instagram da VEGA: o design system, as regras,
o pipeline de composição e o primeiro carrossel aprovado como referência.

> **Definição oficial da marca** (do site): *"Da aquisição à operação. Um
> sistema só."* A Vega desenha e opera o sistema da empresa: anúncio, sistemas
> com IA e painel na mesma casa. O anúncio traz. O sistema faz. O painel mostra.

## Mapa

| Pasta | O que é | Quem consome |
|---|---|---|
| [`design-system/`](design-system/) | Brief autocontido + preset.css + 2 slides de exemplo em HTML funcional + fontes, logos e referências | **Claude Design** (arrastar a pasta no setup) e qualquer designer |
| [`skill/vega-fontes/`](skill/vega-fontes/) | A skill completa de produção: SKILL.md, os 3 compositores Python, regras e guardrails | **Claude Code** — copiar para `~/.claude/skills/` e invocar `/vega-fontes` |
| [`carrossel-01/`](carrossel-01/) | O carrossel aprovado: `final-4-slides/` (a versão postável) e `arquivo-8-slides/` (a narrativa longa original) | Referência de qualidade e régua do sistema |
| [`producao/`](producao/) | Post-mortem honesto da produção 01 — os 16 erros que geraram os guardrails | Quem for produzir o próximo |

## O sistema em 30 segundos

- Canvas 1080×1350 (4:5). Campo **preto `#050505`** ou **creme `#F2EAD9`** no
  topo até ~50,5%, com **borda reta e dura** — a linha do sistema.
- **UM elemento da cena atravessa a linha** e invade o campo (assinatura da série).
- Tipografia **Jost**: 200 nas headlines, 500 só na palavra de ênfase; glow
  proporcional ao corpo; sem glow no campo claro.
- Copy: headlines **sem pontuação**, primeira palavra de **cada linha maiúscula**,
  quebras sempre controladas; subtítulos aceitam pontuação.
- **Sistema é fixo; cenário é variável** por carrossel (o 01 usou arquitetura
  clássica com tochas — não é regra). Cenário novo precisa de: paleta compatível,
  cena silenciosa, uma fonte de vida para o loop, um elemento que cruze a linha.
- Jogo de cores ao longo do carrossel: alternar campo preto e creme.

## Fluxo de produção de um carrossel novo

1. **Ideia e layout** — Claude Design (arrastar `design-system/`) ou direto no
   Claude Code. Copy primeiro, layout depois, prancha de contato a cada 2 peças.
2. **Fundos** — prompts no padrão do brief, gerados no Higgsfield (GPT Image 2);
   motion no Seedance 2.0 (prompt só de movimento, câmera travada).
3. **Upscale** — `bytedance_video_upscale` (pro · aigc · 2k) via CLI Higgsfield.
4. **Composição** — scripts da skill: linha cravada, campo redesenhado, texto
   centrado no vazio medido, loop costurado. Piloto de 1 frame antes de lote.
5. **Entrega** — pasta com `slide N.png|mp4`, prancha de contato final.

Antes de produzir, ler [`skill/vega-fontes/references/GUARDRAILS.md`](skill/vega-fontes/references/GUARDRAILS.md) —
as 13 regras destiladas do post-mortem. A número zero: **nenhuma operação cara
sobre palpite não verificado.**
