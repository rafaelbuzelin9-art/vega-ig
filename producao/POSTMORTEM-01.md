# Fatos crus da sessão de produção (carrossel VEGA 01, 05-06/ago/2026)

Registro honesto dos erros e retrabalhos, escrito pelo assistente para análise
de post-mortem. Contexto: produção de um carrossel IG (8 slides, depois reduzido
a 4) com fundos gerados por IA (Higgsfield), composição de texto/campo por
código (Chrome headless + PIL + ffmpeg), vídeos em loop.

## Iterações e erros, em ordem

1. GLOW ENGORDANDO LETRA (2×). O halo de text-shadow largo (60px) fez a Jost 200
   parecer bold; usuário suspeitou de fonte errada. Diagnóstico via folha de
   prova. MESMO ERRO voltou semanas... horas depois nas palavras de 56px do
   slide 6 (halo de 10px, proporcionalmente 2× maior). A regra "glow escala com
   o corpo" só foi generalizada na segunda ocorrência.
2. TRACKING NO CONTÊINER SEM font-size: letter-spacing em `em` aplicado num div
   sem corpo declarado → resolveu contra 16px herdado, efeito ~zero. Duas
   rodadas de ajuste "sem efeito" até medir a largura renderizada e achar a causa.
3. TRAÇO AZUL v1 tímido demais (3px numa área de 680px) → refeito com 5 camadas
   de vida (v2) → usuário descartou o traço inteiro no fim. Tempo gasto em algo
   eliminado; a pergunta "esse elemento sobrevive no telefone?" não foi feita
   antes de construir.
4. DETECTOR DE LINHA: 3 falhas distintas. (a) maior salto de brilho pegou degrau
   de escadaria (94%/96%); (b) faixa de busca 30-62% não continha a linha real
   do slide 6 em zoom (linha em ~27%); (c) fração-de-claros confundida por
   nuvens no slide 7. Cada falha rendeu corte errado e re-render.
5. SLIDE 6, CADEIA DE RETRABALHO: usuário escolheu zoom C56 pela chama → só
   depois descobri que as 3 palavras não cabiam no preto naquele zoom (cúpula
   alta demais). Mocks: palavras na cúpula, empilhado com 2 palavras na parede,
   empilhado estrito vazando (offset absoluto duplicado). Usuário matou o plano
   e mandou voltar à versão anterior. Causa raiz: ofereci níveis de zoom SEM
   testar o encaixe do texto em cada um.
6. LINHA DURA NOS VÍDEOS, 3 RODADAS: v1 limiar 30 mordeu pedra sombreada
   (manchas roídas); v2 fechou buracos mas deixou capitéis das bordas furando a
   linha; v3 componente-conectado resolveu. Cada rodada = re-render de 3 vídeos.
   A verificação por frames pegou cada defeito (bom), mas os defeitos eram
   antecipáveis com um teste em 1 frame antes do lote.
7. CAMPO CLARO (creme), 6 RODADAS até o usuário desistir do recorte: bolsões de
   preto do vídeo dentro da máscara (invisíveis no preto, gritantes no creme) →
   fix criou vazamentos de creme nos vãos escuros → linha baixa colidiu texto
   com arco (geometria não calculada antes) → ilhas órfãs pós-interseção →
   serrilhado do anel. Usuário: "falhou, refaz sem o 3d". A alternativa limpa
   (linha reta, cena full-bleed — que a própria referência Replit usa) só foi
   oferecida como fallback, não como primeira opção.
8. ORQUESTRAÇÃO: usei `nohup &` DENTRO de um comando já em background → a
   notificação de conclusão veio do lançador, não do trabalho → declarei fix
   concluído, chequei arquivos velhos no meio da troca e tirei conclusão errada
   de um crop. Corrigido com monitor de verdade na segunda vez.
9. COPYRIGHT SEEDANCE: prompt de motion com "temple" gatilhou ip_detected
   (falso positivo Parthenon). Diagnóstico levou 2 rodadas porque primeiro
   entendi que o bloqueio era na geração de IMAGEM (era no MOTION) — o usuário
   precisou corrigir minha leitura.
10. ARQUIVO ERRADO 2×: peguei "o mais novo de Downloads" e era outra coisa
    (imagem do slide 6 quando esperava o 7; céu do 8 idem). Sem confirmação de
    nome/tamanho antes de medir, medi geometria de arquivo errado e reportei
    números sem sentido.
11. REENQUADRE DO SEEDANCE: em 2 vídeos o modelo mudou o enquadre do element
    (aproximou/deslocou linha) apesar de "locked camera" — coordenadas
    pré-calculadas (porta, traço) quebraram; descoberto só na composição.
12. MONOTONIA DOS 8 SLIDES: o usuário só sentiu o problema com o carrossel
    inteiro pronto → pivô para 4 slides (refação de estrutura). Nunca montei
    uma prancha de contato (os 8 lado a lado) durante a produção, que teria
    exposto a repetição cedo.
13. DERIVA DAS PRÓPRIAS REGRAS: os slides objetivos (formato novo) saíram com
    linhas de continuação em minúscula, violando a regra de caixa travada no
    PRESET; e o "?" do CTA ficou como exceção não resolvida. Só o painel de
    juízes pegou, no fim.
14. PAINEL DE JUÍZES: passei restrição imprecisa (limite de 20 chars aplicado a
    uma linha que na arte real é de 72px e cabia) — juízes reportaram violação
    inexistente junto das reais.
15. CÉU ESTRELADO: composição com duas reamostragens matou estrelas sub-pixel;
    usuário viu perda de qualidade. Refeito com reamostragem única + unsharp.
16. RITMO COM O USUÁRIO: em um momento executei um plano que ele tinha mandado
    abortar (mid-turn: "N é para executar o plano preto" chegou enquanto eu já
    rodava o render do plano preto estrito).

## O que funcionou (para não jogar fora)

- Separação generativo/determinístico (fundo IA, texto/campo/loop código).
- Verificação por frame antes de declarar pronto (pegou todos os defeitos).
- Medição em vez de olhômetro (centros de texto, margens, linhas).
- Padding de campo invisível para cravar a linha; costura de loop por crossfade.
- Folha de prova tipográfica com controle de fallback.
- Pipeline reutilizável ao fim (skill com 3 compositores + regras).
