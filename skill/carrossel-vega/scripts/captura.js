// Varre o tempo quadro a quadro numa única instância do Chrome.
// Abrir um Chrome por frame custaria minutos; aqui a página carrega uma vez e
// só o relógio anda, o que também garante que todo frame venha do mesmo layout.
const puppeteer = require("./shadcn-ref/node_modules/puppeteer-core");
const path = require("path");
const fs = require("fs");

const [N, FPS, ESCALA] = process.argv.slice(2).map(Number);
const AQUI = __dirname;
const FRAMES = path.join(AQUI, "_frames");

(async () => {
  const browser = await puppeteer.launch({
    executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    headless: "new",
    args: ["--allow-file-access-from-files", "--no-sandbox", "--hide-scrollbars",
           "--disable-gpu", "--font-render-hinting=none"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: ESCALA });
  await page.goto("file:///" + path.join(AQUI, "_anim.html").replace(/\\/g, "/"),
                  { waitUntil: "networkidle0" });
  await page.evaluateHandle("document.fonts.ready");

  for (let i = 0; i < N; i++) {
    const t = i / FPS;
    await page.evaluate((t) => window.frame(t), t);
    await page.screenshot({
      path: path.join(FRAMES, "f" + String(i + 1).padStart(4, "0") + ".png"),
      omitBackground: false,
    });
    if ((i + 1) % 30 === 0) process.stdout.write(`  ${i + 1}/${N} quadros\n`);
  }
  await browser.close();
  console.log(`${fs.readdirSync(FRAMES).length} quadros escritos`);
})();
