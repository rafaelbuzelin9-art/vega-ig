# Como rodar, do zero

Numa pasta de trabalho nova (fora do repo, ou dentro de `vega-ig/carrossel-XX`):

```bash
# 1. scripts e assets
cp <skill>/scripts/{compor.py,anima.py,captura.js} .
mkdir -p assets fundos && cp <skill>/assets/* assets/
cp assets/base-atlas.png BASE-vega.png            # o compor espera esse nome

# 2. CSS dos cartões (uma vez)
mkdir -p shadcn-ref && cd shadcn-ref
npm init -y && npm i -D tailwindcss @tailwindcss/cli && npm i puppeteer-core
cp ../assets/cards.css entrada.css
npx @tailwindcss/cli -i entrada.css -o saida.css --content "../compor.py,../anima.py"
cd ..

# 3. slide e vídeo
python compor.py volume
python anima.py volume
```

`VEGA_ASSETS` aponta de onde saem `preset.css` e a fonte. Dentro do repo
`vega-ig`, use `VEGA_ASSETS=../design-system`; fora dele o default já é
`../assets` relativo ao script.

Requisitos: Chrome em `C:\Program Files\Google\Chrome\Application\chrome.exe`,
Python com Pillow, numpy e scipy, Node 20+, ffmpeg no PATH.

## Guardrails que o compor imprime

- `margens 90/92px` — margem lateral do bloco de texto, medida no pixel. Se
  vier `texto nao detectado`, o contraste quebrou.
- `arco ocupa 138°` — só nos slides com legenda curva. Acima de 140° a ponta
  vira e não se lê.
