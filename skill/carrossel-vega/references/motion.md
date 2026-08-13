# Motion — cursor clicando, cartão nascendo, número subindo

Vídeo do slide 02: 1080×1350, 9s a 30fps, `VIDEO-volume.mp4` (~0,5 MB).

## Arquitetura

1. `compor.py` rasteriza o slide **sem o painel** — fundo, wordmark, headline e
   subtítulo viram o cenário fixo;
2. `anima.py` monta um HTML com esse PNG de fundo e **só o painel** por cima, em
   Tailwind, com um relógio próprio `frame(t)`;
3. `captura.js` (puppeteer-core) varre o tempo numa **única instância** do
   Chrome: `page.evaluate(t => window.frame(t))` + `screenshot` por quadro;
4. ffmpeg fecha em h264, `crf 17`, `yuv420p`, `+faststart`.

Um Chrome por quadro levaria minutos e não garante o mesmo layout entre eles.
Captura em `deviceScaleFactor 2` e o ffmpeg reduz com lanczos.

## Roteiro (em `anima.py`, no topo)

```python
NASCE  = [0.80, 1.85, 2.90, 3.95]   # um clique por cartão
EXTRAS = [5.45, 6.15, 6.85]         # segunda passada, todos no primeiro cartão
POR_MINUTO = 16                     # +1 min na confirmação = +16h no mês
```

A segunda passada é a frase da peça dita em movimento: o cursor volta ao
primeiro cartão, o minuto sobe 1→2→3→4 e o total do mês sobe **junto**,
38→54→70→86. A conta fecha em 32 confirmações por dia × 30 dias ÷ 60.

Cada cartão guarda uma lista de eventos `(instante, valor)`; o valor interpola
do anterior para o novo. É o que permite um número subir mais de uma vez.

## As curvas

- **entrada do cartão**: mola de verdade, `1 - e^(-5.4x)·cos(3.1πx)` — amplitude
  decaindo enquanto oscila. Um easing que só desacelera não dá sensação de massa.
  Junto: `translateY 30→0`, `scale .86→1`, `blur 16px→0`, opacidade em 0,16s.
- **contagem**: `outExpo`, 0,55s nos cartões e 0,95s no total (38 subindo no
  tempo de 1 vira piscada).
- **pop do número**: só DEPOIS de a contagem fechar, pulso de 16% com
  `transform-origin: 0% 60%`. Escalar durante a subida embaralha as duas
  leituras.
- **cursor**: `inOutQuint` e trajetória em **bézier com barriga** — entre dois
  cartões empilhados a linha reta lê como teleporte vertical.

## O cursor

Disco de vidro (46px) com borda creme, brilho no canto superior esquerdo e ponto
central, mais um **rastro** amortecido atrás. A seta de sistema era corpo
estranho no meio de um painel de vidro e, a 30fps, pulava de ponto a ponto.

Entra pelo topo do quadro (`[540, -120]`), pousa 0,10s antes do clique, afunda
18% no toque e sai pela borda de baixo no fim.

**A causa do "teleporte" era o tempo, não o easing:** o trajeto tinha 0,31s
porque começava tarde e chegava cedo demais. Agora usa todo o intervalo entre
uma parada e a seguinte (`ini = parada_anterior + 0.05`, `chega = parada - 0.10`).

O rastro é recalculado do zero a cada quadro (loop de 1/60 em 1/60 até `t`),
porque um seguidor com estado dependeria da ordem em que os quadros foram
renderizados — e num render quadro a quadro isso não é garantido.

## Conferência

Não assista ao MP4 para julgar: extraia instantes e monte uma prancha.

```python
for i, t in enumerate([0.35, 1.30, 2.40, 4.10, 4.90, 5.60, 6.30, 7.00]):
    subprocess.run(["ffmpeg","-y","-ss",str(t),"-i","VIDEO-volume.mp4",
                    "-frames:v","1", f"_chk/{i}.png"], capture_output=True)
```

E abra tudo com `Invoke-Item` no fim.
