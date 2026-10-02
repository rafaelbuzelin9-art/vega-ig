// Captura grafico.html quadro a quadro por CDP (Chrome --headless=old) e grava PNGs.
// Uso: node --experimental-websocket capturar.mjs
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';

// Uso: node --experimental-websocket capturar.mjs [nome]  (nome = grafico | grafico-b | grafico-c)
const DIR = '/private/tmp/vega-faisca-trabalho/grafico';
const NOME = process.argv[2] || 'grafico';
const HTML = `file://${DIR}/${NOME}.html?parado`;
const QUADROS = `${DIR}/quadros-${process.env.OUT || NOME}`;
const PERFIL = `${DIR}/perfil-chrome-${NOME}`;
// Sobrescreva por ambiente: DUR=8 W=480 H=854 FPS=24
const FPS = +(process.env.FPS || 30), DUR = +(process.env.DUR || 5.0), W = +(process.env.W || 1600), H = +(process.env.H || 1000), PORT = 9333;

rmSync(QUADROS, { recursive: true, force: true }); mkdirSync(QUADROS);
rmSync(PERFIL, { recursive: true, force: true });

const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless=old', `--remote-debugging-port=${PORT}`, `--user-data-dir=${PERFIL}`,
  `--window-size=${W},${H}`, '--hide-scrollbars', '--no-first-run', '--disable-gpu', 'about:blank',
], { stdio: 'ignore' });

let alvo;
for (let i = 0; i < 40; i++) {
  try { const r = await fetch(`http://127.0.0.1:${PORT}/json`); const l = await r.json(); alvo = l.find(p => p.type === 'page'); if (alvo) break; } catch {}
  await sleep(250);
}
if (!alvo) { chrome.kill(); throw new Error('Chrome não abriu a porta de depuração'); }

const ws = new WebSocket(alvo.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pend = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
const cdp = (method, params = {}) => new Promise(res => { const n = ++id; pend.set(n, res); ws.send(JSON.stringify({ id: n, method, params })); });

await cdp('Page.enable');
await cdp('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
// ALPHA=1: fundo transparente (PNG com alfa) para colar por cima do take.
if (process.env.ALPHA) await cdp('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
await cdp('Page.navigate', { url: HTML + (process.env.ALPHA ? '&alpha=1' : '') + (process.env.Q ? '&' + process.env.Q : '') });
await sleep(1200);
await cdp('Runtime.evaluate', { expression: 'document.fonts.ready' , awaitPromise: true });
// páginas que pré-carregam imagens expõem window.pronto
await cdp('Runtime.evaluate', { expression: 'window.pronto || Promise.resolve()', awaitPromise: true });
// páginas que pré-carregam imagens expõem window.pronto
await cdp('Runtime.evaluate', { expression: 'window.pronto || Promise.resolve()', awaitPromise: true });

const n = Math.round(FPS * DUR);
for (let i = 0; i < n; i++) {
  const t = i / FPS;
  await cdp('Runtime.evaluate', { expression: `window.frame(${t})` });
  const r = await cdp('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
  writeFileSync(`${QUADROS}/q${String(i).padStart(4, '0')}.png`, Buffer.from(r.result.data, 'base64'));
}
ws.close(); chrome.kill('SIGKILL');
if (!existsSync(`${QUADROS}/q${String(n - 1).padStart(4, '0')}.png`)) throw new Error('último quadro não gravou');
console.log(`${n} quadros em ${QUADROS}`);
