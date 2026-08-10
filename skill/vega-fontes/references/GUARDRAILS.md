# Guardrails de produção — post-mortem do carrossel 01

Síntese de três analistas (engenharia, design, colaboração) sobre os 16 erros
registrados da primeira produção. Regra-mãe, unânime: **nenhuma operação cara
sobre palpite não verificado — o teste de um minuto vem antes da construção,
sempre.** Organizado por momento do fluxo.

## Na ingestão de qualquer arquivo do diretor

1. **Handshake de arquivo.** Antes de medir ou compor: ecoar nome, dimensões ou
   duração, tipo e uma descrição de 5 palavras do conteúdo + o slide presumido
   ("recebi X.mp4, 834×1112, 6s, corredor de tochas — é o motion do slide 4?").
   Conteúdo não bate com a expectativa → parar e perguntar. **Proibido operar
   sobre "o mais novo de Downloads" sem esse eco** (2 medições de arquivo errado
   na sessão 01).
2. **Re-medir no artefato entregue, nunca no prometido.** O Seedance reenquadra
   mesmo com "locked camera": rodar o detector no frame 0 do vídeo e comparar
   com o element; delta > 1,5% do quadro → recalcular todas as coordenadas
   (porta, coroa, âncoras) a partir do vídeo.
3. **Detector de linha com invariante.** Depois do argmax: ≥98% dos pixels acima
   da linha abaixo do limiar. Falhou → frame anotado + abortar com aviso, nunca
   cortar no palpite (escadaria a 94%, linha fora da faixa e nuvens enganaram o
   detector 3× na sessão 01).

## Antes de oferecer opções ao diretor

4. **Menu pré-validado / encaixe antes de enquadre.** Toda opção de zoom, crop
   ou layout é testada contra as restrições duras ANTES de entrar no menu — o
   texto real (corpo e tracking do preset) composto sobre cada candidato. Opção
   onde o texto não cabe não é oferecida. Aprovação colhida sobre opção inviável
   é retrabalho garantido + custo de matar um plano já escolhido (cadeia do
   slide 6).
5. **Prova de telefone.** Elemento visual novo (traço, ornamento, corpo novo)
   nasce como mock estático avaliado em largura de tela de celular (~60mm)
   antes de qualquer engenharia. Não sobrevive → não se constrói (traço azul:
   construído em 5 camadas, morto pelo diretor depois).

## Durante a construção

6. **Piloto de 1 frame antes de lote.** Qualquer render de 2+ peças roda primeiro
   num único frame representativo — incluindo o pior caso (bordas, sombras,
   capitéis) — com inspeção visual. Só então o lote. (As 3 rodadas da linha dura
   custaram re-render de 3 vídeos cada; o defeito aparecia num frame de 3s.)
7. **Desistência em 2 rodadas.** Mesma abordagem falhando 2 rodadas seguidas com
   defeito novo na mesma fronteira = material resistindo. Na 3ª, o default é
   trocar de layout, com a alternativa simples (idealmente a que a referência
   já valida) como candidata A — não como fallback. Diretor autoriza no máximo
   1 rodada extra, explicitamente. (Campo claro: 6 rodadas até o diretor matar.)
8. **Regra aprendida vira código no mesmo dia.** Descobriu regra (glow ∝ corpo,
   caixa por linha)? Ela entra no preset/checklist NA HORA — regra em prosa
   reincide (o glow engordou letra 2× antes de virar regra; a caixa travada foi
   violada pelo formato novo e só o painel de juízes pegou).
9. **Asserção de efeito.** Todo ajuste de parâmetro tipográfico fecha com medição
   antes/depois (largura, margens). Delta ~zero = parâmetro não aplicado
   (letter-spacing em `em` num contêiner sem font-size resolveu contra 16px).

## Ao concluir

10. **Conclusão só pelo artefato.** Notificação de processo/lançador nunca é
    evidência — "pronto" exige o arquivo final verificado (mtime posterior ao
    disparo, frames contados, 1 frame inspecionado). Proibido `nohup &` dentro
    de job já em background (gerou notificação falsa e diagnóstico sobre arquivo
    velho). Durante troca de arquivos em andamento, não medir nada.
11. **Trava de disparo.** Antes de qualquer operação cara: reler a última
    mensagem do diretor (mensagem mid-turn pode ser um abort), anunciar em uma
    linha o que vai rodar. Ambiguidade sobre QUAL artefato/etapa ("o bloqueio
    foi na imagem ou no motion?") = 1 pergunta binária antes de diagnosticar —
    custa uma linha, errar custa uma rodada.

## Ao delegar (juízes, subagentes)

12. **Restrição ancorada.** Cada regra passada a um juiz vai com fonte
    (arquivo/linha), unidade da arte real (px e corpo, não proxy de contagem de
    caracteres) e um exemplo que passa. O pipeline mede encaixe; o juiz julga
    estética. Relatório de subagente é conferido contra a arte antes de virar
    retrabalho (um juiz da sessão 01 auditou uma restrição que não existia na
    arte porque foi passada em proxy).

## No conjunto (carrossel/série)

13. **Prancha de contato contínua.** A cada slide aprovado, montar o mosaico de
    todos os slides existentes e revisar com o diretor a cada 2-3 peças, com a
    pergunta explícita de conjunto ("repetitivo? ritmo?"). Monotonia estrutural
    descoberta com a peça pronta custou o pivô de 8→4 slides; no mosaico ela
    aparecia no slide 3.
