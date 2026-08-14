# VEGA — Sistema de Criativos de Performance

**Complemento de `BRIEF-VEGA.md`. Não substitui nada.** O sistema (campo, linha, Jost,
paleta, regras de copy, grid, logo) continua inviolável. Este documento trata de **uma
coisa só**: como distribuir escala, peso e vazio quando a peça precisa disputar atenção
no feed, e não ser lida em tela cheia.

Fontes: `BRIEF-VEGA.md` · `skill/vega-fontes/preset.css` · `references/REGRAS.md` ·
`references/GUARDRAILS.md` · `vega-systems/MANUAL-DA-MARCA.md` · `vega-systems/brand/BRIEF.md` ·
`03-Relatorios/dossie-concorrencia-2026-08/`.
Medições: ago/2026, sobre os arquivos reais de fonte do preset.

---

## 0 · O diagnóstico, medido

A peça institucional é lida por quem parou. O anúncio é lido por quem está passando. A
diferença não é de gosto — é física, e dá para medir.

Uma arte de 1080 px ocupa **71,5 mm** na tela de um celular, lida a ~35 cm. Nessa
distância, **1 minuto de arco = 0,10 mm**: é o limite do que o olho resolve. Medindo os
corpos do preset atual nesse tamanho físico:

| Nível do preset | Corpo | x-height | Haste | Veredito |
|---|---|---|---|---|
| Ênfase (Jost 500) | 104 px | 34′ | **7,8′** | Lido em rolagem, com força |
| Headline l2 (Jost 200) | 104 px | 34′ | 2,0′ | Lido em rolagem |
| Headline objetivo (200) | 80 px | 26′ | **1,3′** | Tamanho ok, **traço no piso** |
| Linha 1 (Jost 200) | 72 px | 23′ | **1,3′** | Abaixo da rolagem |
| Subtítulo (Jost 200) | 31 px | **10′** | **0,7′** | **Não é lido. É textura.** |

Réguas: x-height ≥ 25′ = lido em rolagem · ≥ 16′ = lido por quem parou · < 16′ = decoração.
Haste ≥ 2′ = traço com presença · < 1′ = cinza, não letra.

**Três conclusões que organizam o resto do documento.**

**1. O problema não é tamanho. É tinta.** A Jost 200 a 72–80 px tem o tamanho certo e a
densidade de um fio de cabelo (1,3′, no piso da acuidade). A letra existe e não tem
presença. Foi isso que sempre pareceu "leve demais" — e é por isso que aumentar o corpo
sozinho não resolve: a Jost 200 só cruza 2′ de haste **acima de 96 px**.

**2. O subtítulo de 31 px não está sendo lido em anúncio nenhum.** 10′ de x-height, haste
de 0,7′ — abaixo do limiar de detecção. Não é um problema de tamanho corrigível: mesmo
levando o apoio para Inter 300 a 48 px chega-se a 17,6′, o que serve para quem parou e
nunca para quem rola. **Texto secundário é o prêmio de quem parou. Nunca é o trabalho de
parar.** Isso não é um defeito a consertar; é uma função a respeitar.

**3. A VEGA já tem UM hero por peça — e é o errado.** A palavra de ênfase em 500 carrega
**4× mais tinta** que o resto da linha (7,8′ contra 2,0′). No feed o olho pousa nela e
reconstrói a frase de trás para frente. O mecanismo de contraste da marca já é violento;
ele só não está apontado para o argumento.

**A resposta à pergunta central do estudo, então, não é "aumentar o volume".** É: gastar
a tinta que o sistema já produz no elemento certo, e parar de pagar por níveis
tipográficos que ninguém lê.

---

## A · HIERARQUIA TIPOGRÁFICA

### A.1 A escada de escala (1080 px de arte, 960 úteis, tracking −2,5%)

O número de caracteres é **limite duro**, não sugestão: acima dele a linha vaza ou quebra
sozinha, e órfã tipográfica é reprovação (`BRIEF-VEGA.md`).

| Corpo | x-height | Haste 200 | Haste 500 | Cabe (200) | Cabe (500) | Papel em performance |
|---|---|---|---|---|---|---|
| 420 px | 137′ | 8,5′ | 30′ | **5** | 4 | Número/palavra-hero |
| 340 px | 110′ | 7,2′ | 24′ | **6** | 6 | Número-hero |
| 260 px | 85′ | 5,2′ | 19′ | **9** | 7 | Palavra-hero |
| 200 px | 65′ | 3,9′ | 14′ | **11** | 10 | Hero curto |
| 168 px | 55′ | 3,3′ | 12′ | **13** | 12 | Hero de duas linhas |
| 140 px | 46′ | 2,6′ | 10′ | **16** | 14 | Hero de três linhas |
| 120 px | 39′ | 2,6′ | 8,5′ | **19** | 18 | Piso confortável do hero |
| **104 px** | 34′ | 2,0′ | 7,8′ | **23** | 21 | **Piso do que é lido em rolagem** |
| 96 px | 31′ | 2,0′ | 7,2′ | 24 | 23 | Remate / segunda linha |
| 80 px | 26′ | 1,3′ | 5,9′ | 30 | 26 | **Só com peso ≥ 300** |
| 72 px | 23′ | 1,3′ | 5,2′ | 33 | 30 | Fora do trabalho de rolagem |
| ≤ 48 px | ≤ 16′ | 0,7′ | 3,3′ | 50+ | 45+ | Prêmio de quem parou |

### A.2 As sete regras

**R1 · A linha de 104 px é o chão, não o teto.** Em anúncio, nada abaixo de 104 px está
fazendo trabalho de rolagem. Se a informação precisa ser lida por quem passa, ela sobe
para ≥ 104. Se não precisa, ela desce para ≤ 48 e para de disputar. **A faixa de 56 a 96
px é terra de ninguém: grande demais para ser discreta, pequena demais para ser lida.**
É exatamente onde estão o l1 (72) e o headline objetivo (80) hoje.

**R2 · Quando o hero cresce, a copy encolhe primeiro.** Escala oversized não é decisão de
layout, é decisão de texto. A 168 px cabem 13 caracteres por linha; a 260 px, 9. Não
existe headline gigante com a copy do tamanho atual. **Escreva o hero contando caracteres,
antes de escolher o corpo.**

**R3 · Duas alturas tipográficas por peça. Três só com motivo escrito.** Institucional
tolera l1 + l2 + subtítulo. Anúncio não: são três apostas de atenção onde o feed concede
uma. O padrão de performance é **hero + remate**, e o remate existe para desambiguar o
hero, não para completá-lo.

**R4 · O contraste de peso é o motor, e ele já é 4:1.** Uma palavra em 500 dentro de uma
linha em 200 tem quatro vezes mais tinta. Isso basta e continua bastando. **Não subir de
500** (`REGRAS.md`: acima disso engorda e vaza a margem). O que muda em performance é
**onde** a ênfase cai: no institucional ela pontua a frase; no anúncio ela **é** o
argumento — se o leitor só ler a palavra em 500, ele tem de sair sabendo do que se trata.
Teste: tape tudo menos a palavra pesada. Sobrou uma mensagem? Passou.

**R5 · O apoio é Inter Light 300, não Jost 200 miúda.** O manual da marca já manda isso
(`brand/BRIEF.md`: Jost 200 para títulos, Inter Light 300 para apoio) e a peça CARTÃO do
dossiê já especifica assim. A Jost 200 a 31 px tem 0,7′ de haste; a Inter 300 no mesmo
corpo tem o dobro e uma x-height maior. **Não é fonte nova: é a segunda fonte do manual,
usada no lugar dela.** Custo de aprovação: zero.

**R6 · Número é o hero mais barato que a VEGA tem.** Ele resolve os três limites de uma
vez: cabe em corpo enorme (dois dígitos entram em 340 px com folga), lê-se sem sintaxe, e
sobrevive à Jost 200 porque a 340 px a haste chega a 7,2′ — densa **sem precisar de peso**.
Um número em Jost 200 a 340 px é a peça mais VEGA e mais agressiva que o sistema permite,
ao mesmo tempo. **Trava do manual:** número sem prova é proibido (regra dura nº 1,
`MANUAL-DA-MARCA.md`). Número-hero só entra se for auditável — do painel, do print, da
conta. Sem lastro, o hero vira palavra ou frase.

**R7 · Glow proporcional, e menos dele quando o corpo é grande.** Mantido de `REGRAS.md`:
raio curto e opacidade alta; halo largo sangra para dentro da haste e faz a 200 parecer
400. Em corpos de hero (≥ 200 px) o glow em `em` já fica largo — **conferir no zoom de
100% e reduzir a opacidade antes de reduzir o raio**. No campo claro, sem glow, sempre.

### A.3 Proposta que precisa de aprovação do Rafael

O arquivo `jost-variable-latin.woff2` é variável de 100 a 900. O sistema declara 200 e
500 e nunca abriu o meio. Medido a 80 px:

| Peso | Haste | Largura da linha |
|---|---|---|
| 200 | 1,3′ | base |
| 300 | 2,6′ | **+4,3 %** |
| 350 | 3,3′ | +7,2 % |
| 500 | 5,9′ | +17,2 % |

**A lição "peso custa largura" foi medida entre 200 e 500 (+17 %) e não vale na faixa
baixa:** 200 → 300 **dobra a tinta e custa 4 % de largura**. Isso abre um nível que hoje
não existe — um corpo de 80 px legível sem virar ênfase — e resolveria a terra de ninguém
da R1 sem mexer em corpo nem em copy.

**Não usei isso nas peças de teste, e não deve entrar em produção sem decisão.** É a única
proposta deste documento que altera uma regra travada. As três direções do §Teste rodam
sem ela.

---

## B · A REGRA DO HERO

**Um criativo, um hero.** Todo o resto da composição trabalha para ele — inclusive
desaparecendo.

O hero não é o elemento mais bonito nem o mais importante da oferta. É **o único elemento
que precisa sobreviver a 0,4 segundo de rolagem**. Escolhe-se assim:

**1. Qual é a única coisa que a pessoa tem de levar se não ler mais nada?** Escreva em uma
frase. Se precisar de duas, a peça tem dois heróis e uma delas é outro anúncio.

**2. Qual é a forma mais densa dessa coisa?** Na ordem em que a VEGA deve preferir:

| Forma | Quando é a melhor | Custo |
|---|---|---|
| **Número auditável** | Existe prova (painel, print, conta) | Depende de lastro real |
| **Artefato real** (print, conversa, documento, tela) | O argumento é "isso aconteceu" | Captura limpa |
| **Objeto físico fotografado** | O argumento tem matéria (celular, papel, balcão) | Cena gerada ou foto |
| **Palavra única** | A oferta cabe em uma palavra | Grátis |
| **Frase** | Nenhuma das anteriores serve | Grátis, e é o padrão |

Frase é o fallback honesto, não o primeiro recurso. Se toda peça do mês tem frase como
hero, o problema é falta de prova, não de direção de arte — e isso é assunto de operação,
não de design (é literalmente a lacuna nº 1 do dossiê: *ninguém no nicho mostra a tela*).

**3. Todo o resto ou serve ao hero ou sai.** Regra de corte: cada elemento restante
responde "o que eu faço pelo hero?". Quem responde "eu completo a informação" **sai** —
isso é trabalho da copy do post, que tem espaço infinito e é grátis. Fica só quem
responde "eu deixo o hero mais legível, mais crível ou mais estranho".

**4. Teste de contato.** Reduza a peça a 71,5 mm (ou rode a prova de telefone do
`GUARDRAILS.md` #5, que é mais dura: 60 mm). Se dois elementos disputam o primeiro pouso
do olho, mate um. Se nenhum pousa, não há hero.

**O que isso derruba do hábito atual:** l1 + l2 + subtítulo + elemento que cruza a linha
são quatro focos. No institucional isso é ritmo; no feed é empate.

---

## C · AS QUATRO COMPOSIÇÕES

Não são templates. São quatro maneiras de organizar campo, linha e vazio em torno de um
tipo de hero. Todas mantêm a assinatura da série: **UM elemento cruza a linha do campo.**

### C1 · DECLARAÇÃO — o hero é a frase
Campo ocupando 60–70 % da altura (mais alto que o institucional), hero em 140–200 px em
duas ou três linhas, remate em 96 px com a única ênfase, vazio largo embaixo, cena
reduzida a uma faixa com um elemento cruzando.
**Mecanismo:** contraste de escala contra vazio. É o cartão de 1.300 dias do dossiê, com
identidade.
**Usar quando:** não há prova ainda; a mensagem é um princípio ou uma objeção.
**Não usar quando:** existe artefato disponível — é desperdiçar prova.

### C2 · PROVA — o hero é a interface
O print real (conversa, painel, canvas de fluxo, gerenciador) **é o elemento que cruza a
linha**: entra pelo campo, atravessa e desce para a cena. Borda dura, sem moldura de
celular, sem cursor, sem barra de tarefas. Hero tipográfico curto acima (≤ 140 px, ≤ 16
caracteres) nomeando o que se está vendo.
**Mecanismo:** materialidade + prova. Interrompe porque não parece anúncio.
**Usar quando:** o argumento é "isso é real e você pode auditar".
**Regra dura:** o print é recorte nativo, nunca tela fotografada. É o defeito exato que o
dossiê registra no líder de 699 dias — e acabamento é a cunha declarada da VEGA. **Ser
documental nunca é ser desleixado.**

### C3 · OBJETO — o hero é a coisa
Objeto real (celular, papel, post-it, quadro, documento) em crop agressivo, cruzando a
linha e **saindo pela borda do quadro**. Texto todo de um lado, alinhado à esquerda,
assimétrico. Campo pode ser creme — o objeto escuro vira o contraste.
**Mecanismo:** escala + corte + assimetria. O elemento parcialmente fora do quadro faz o
olho completar, e completar é parar.
**Usar quando:** a dor tem matéria; ou quando a série precisa de respiro depois de duas
peças pretas.
**Não usar quando:** o objeto é genérico. Celular flutuando em fundo liso é banco de
imagens com outra paleta.

### C4 · MEDIDA — o hero é o número
Número em 260–420 px, Jost 200 (não 500 — nesse corpo a 200 já é densa e a 500 vira
mancha), centrado ou alto no campo. Uma linha de 88–104 px embaixo dizendo do que o
número é. Nada mais.
**Mecanismo:** contraste entre dado enorme e explicação mínima. É o formato mais raro do
mercado — o dossiê varreu duas categorias que vendem número e **não achou um único
gráfico ou contador**.
**Usar quando:** há número auditável.
**Trava:** sem lastro, não sobe. Ver R6.

**Sobre o vídeo:** a lacuna nº 3 do dossiê é que *tipografia animada pura não apareceu uma
única vez* em nenhuma peça longeva dos dois mercados — e é exatamente o que o compositor
da skill já sabe fazer. Qualquer uma das quatro composições vira loop de 9–12 s com
movimento só no campo (deriva lenta, letra que se constrói, constelação em fase). Isso é
uma vaga de leilão, não uma opinião estética.

---

## D · POLIDA × DOCUMENTAL

Duas intensidades da mesma identidade. **Não são duas marcas, e a escolha não é de gosto:
é sobre o que a peça está pedindo que o leitor acredite.**

| | **POLIDA** | **DOCUMENTAL** |
|---|---|---|
| Material principal | Cena gerada, mockup, diagrama, tipografia | Print, foto de objeto, papel, tela, conversa |
| Pede que o leitor acredite | no critério de quem fez | no fato que aconteceu |
| Melhor em | princípio, objeção, posicionamento, oferta | prova, demonstração, bastidor, "tá rodando hoje" |
| Composições | C1, C4 | C2, C3 |
| Risco | virar bonito e vazio | virar desleixado |

**Quando cada uma para o scroll melhor.** A polida ganha em público frio e topo: é a que
constrói a percepção de casa cara, e é o único registro em que a VEGA não parece "mais um
anúncio". A documental ganha em público que já viu a marca e em qualquer argumento que
dependa de crença — porque o print é o único elemento do feed que não parece comprado.

**O que NÃO muda entre as duas (é isso que faz as duas parecerem VEGA):**

1. Campo com **linha dura**, e **um elemento cruzando** — no documental, o próprio
   artefato é quem cruza.
2. Paleta e piso `#050505` / `#F2EAD9`. Nunca preto ou branco puros.
3. Jost com o tracking do preset e **uma** ênfase por bloco.
4. Regras de copy: headline sem pontuação (exceto pergunta), inicial maiúscula por linha.
5. Logo 150 px, topo-esquerda, na posição travada. Sem contador de slide, sem segundo selo.
6. Grid de pontos e o vazio como material.

**A cor que vem de dentro do artefato.** Um print real traz verde de WhatsApp, azul de
sistema, vermelho de badge. **Isso não é cor de marca — é cor do documento, e ela pode
ficar**, porque removê-la destrói justamente a credibilidade que motivou usar o print. A
regra: a cor estranha só existe **dentro** dos limites do artefato, nunca vaza para o
campo, nunca vira elemento gráfico, nunca é usada por decisão estética. Se der para
enquadrar de modo que apareça pouca, melhor. O banido continua banido: gradiente colorido
de SaaS, glow neon, azul Vega como tinta de texto.

---

## E · FAZER / EVITAR

### FAZER

- **Um hero.** Se em dúvida entre dois, produza duas peças.
- **Contar caracteres antes de escolher o corpo** (tabela A.1).
- **Subir o hero para ≥ 104 px**, e de preferência ≥ 140.
- **Descer o apoio para ≤ 48 px em Inter 300** e aceitar que ele não será lido em rolagem.
- **Gastar o vazio.** Espaço negativo grande contra um elemento grande é o contraste mais
  caro que existe e o que mais parece VEGA.
- **Cortar com agressividade** e deixar o elemento sair do quadro.
- **Usar o print nativo** quando houver prova.
- **Deixar o artefato cruzar a linha** — é como a série continua sendo a série.
- **Nascer com 4 variações do gancho.** O dossiê inteiro mostra que a falha nº 1 dos
  longevos é rodar anos com uma variação só.
- **Rodar a prova de telefone antes de refinar qualquer coisa** (`GUARDRAILS.md` #5).

### EVITAR

- **Três níveis tipográficos** por inércia do preset institucional.
- **Corpos entre 56 e 96 px** carregando informação que precisa ser lida.
- **Subtítulo como muleta** — se o hero precisa dele para fazer sentido, o hero está errado.
- **Peso acima de 500**, ou mais de uma ênfase por bloco.
- **Glow largo** para dar presença. Engorda a letra e mata a Extra-light.
- **Aumentar tudo.** Contraste é diferença; se tudo cresce, nada aparece.
- **Cor nova para chamar atenção.** A tinta da VEGA é escala, peso e vazio.
- **Tela fotografada** no lugar de captura nativa, e **moldura de celular** em volta do print.
- **Número sem prova**, mesmo que ilustrativo. Regra dura nº 1 do manual.
- **Contador de slide, botão falso, seta gigante, círculo, ícone, gradiente, holograma,
  cérebro de IA, sparkle de 4 pontas.** Nenhum deles ganha um leilão que a escala não ganhe.

**O único recurso agressivo que este estudo aprova, e por quê:** o **crop com sangramento**
(elemento cortado pela borda do quadro, C3). Não é efeito — é composição, tem 80 anos de
uso editorial, e funciona porque uma forma incompleta obriga o olho a completá-la, o que
custa uma fração de segundo a mais de permanência. É a única coisa da lista de "mecanismos
de impacto" que atravessa o filtro *calmo · caro · editorial · preciso* sem arranhão.

---

## Teste — uma mensagem, três direções

**Mensagem** (frase canônica do manifesto, `MANUAL-DA-MARCA.md` §06): *o lead que ficou
sem resposta não reclama, só compra do concorrente.*

Renderizadas em `assets/perf-tres-direcoes.jpg` — cada uma a 100 % e na prova de telefone.
As cenas são placeholder, como manda o `BRIEF-VEGA.md` para mockup.

### Direção 1 · DECLARAÇÃO (C1, polida)
Campo preto até 66,5 %. Hero **"Ele não / reclama"** em Jost 200 a 168 px, duas linhas
centradas (7 e 7 caracteres — folga de quase o dobro do limite). Remate **"Só compra do
`concorrente`"** a 96 px, com a única ênfase em 500 na última palavra: quem lê só a
palavra pesada já sabe do que se trata (teste da R4). Uma cúpula da cena cruza a linha.
Rodapé: filete de 112 px e *"O lead sem resposta de ontem"* em Inter 300 a 30 px — apoio
assumidamente ilegível em rolagem, ali para quem parou.
**Por que para o scroll:** três linhas de tinta clara sobre 40 % de vazio preto. É a
peça mais barata de produzir e a que mais constrói marca.

### Direção 2 · PROVA (C2, documental)
Hero tipográfico curto no topo: **"14 horas"** a 140 px + *"De silêncio no seu `WhatsApp`"*
a 64 px. O print da conversa entra a 45 % da altura, **atravessa a linha do campo** e desce
até 90 % — o artefato é o elemento que cruza. Dentro dele: um balão do cliente às 18:42, o
vazio, e o carimbo 09:07 no dia seguinte. **O hero real é o espaço em branco entre os dois
horários.**
**Por que para o scroll:** não parece anúncio. E ocupa a lacuna nº 1 do dossiê — ninguém
no nicho mostra a tela.
**Trava:** o "14 horas" só sobe com print real. Sem ele, esta direção não existe.

### Direção 3 · OBJETO (C3, documental em campo claro)
Campo creme até 52 %, quebrando o ritmo preto da série. Hero **"Ninguém / respondeu"** a
140 px alinhado à esquerda, com a ênfase 500 na segunda linha (peso no campo claro,
sem glow, texto Preto Cine). Celular real fotografado à direita, cruzando a linha **e
saindo pela borda direita do quadro** — o badge vermelho de 14 não lidas é a cor do
documento, contida dentro do objeto. Filete e *"Ontem, entre 18h42 e 09h07"* em Inter 300.
**Por que para o scroll:** inversão de campo + corte sangrado + assimetria. Numa sequência
de anúncios pretos, esta é a que muda o ritmo.

**O que as três provam:** mesma frase, mesma fonte, mesma paleta, mesma linha, mesma logo,
mesma regra de copy — e três peças que ninguém confunde entre si. A variação veio de
**qual é o hero** e **quanto vazio ele recebe**, não de recurso novo.

---

## Pendências

1. **Peso intermediário (§A.3)** — decisão do Rafael. Sem ela, o piso de 104 px vale
   integralmente e a faixa 56–96 px fica proibida para informação de rolagem.
2. **Prova para os números.** C4 e a direção 2 dependem de print auditável. Enquanto não
   existir, o repertório de heróis da VEGA é frase e objeto — metade da força do sistema.
3. **Loop tipográfico.** A lacuna nº 3 do dossiê está aberta e o compositor já faz. Falta
   decidir se entra no primeiro ciclo.

*VEGA · Sistema de criativos de performance · v1 · Belo Horizonte, 13/08/2026*
