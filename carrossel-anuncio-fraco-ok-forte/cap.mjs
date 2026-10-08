// uso: node --experimental-websocket cap.mjs <saida.mp4> [fps] [t1,t2,...para PNGs de teste]
import {spawn} from 'node:child_process';
import fs from 'node:fs';
const [,,saida,fpsArg,testes]=process.argv; const FPS=+(fpsArg||30);
const CH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const prof=fs.mkdtempSync('/private/tmp/vega-anuncio-trabalho/prof-');
const chrome=spawn(CH,['--headless=old','--disable-gpu','--hide-scrollbars','--remote-debugging-port=9337',`--user-data-dir=${prof}`,'--window-size=1080,1920','about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let ws; for(let i=0;i<60;i++){try{const j=await (await fetch('http://127.0.0.1:9337/json')).json();const p=j.find(x=>x.type==='page');if(p){ws=p.webSocketDebuggerUrl;break}}catch{} await sleep(250)}
if(!ws){chrome.kill();throw new Error('Chrome não abriu a porta')}
const sock=new WebSocket(ws); await new Promise(r=>sock.onopen=r);
let id=0; const pend=new Map(); sock.onmessage=m=>{const d=JSON.parse(m.data); if(d.id&&pend.has(d.id)){pend.get(d.id)(d);pend.delete(d.id)}};
const cdp=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);sock.send(JSON.stringify({id:i,method,params}))});
await cdp('Emulation.setDeviceMetricsOverride',{width:1080,height:1920,deviceScaleFactor:1,mobile:false});
await cdp('Page.enable'); await cdp('Page.navigate',{url:'http://localhost:8791/reel.html'});
for(let i=0;i<80;i++){const r=await cdp('Runtime.evaluate',{expression:'window.__pronto===true',returnByValue:true}); if(r.result?.result?.value)break; await sleep(250)}
const dur=(await cdp('Runtime.evaluate',{expression:'DURACAO',returnByValue:true})).result.result.value;
const shot=async t=>{await cdp('Runtime.evaluate',{expression:`render(${t})`}); const r=await cdp('Page.captureScreenshot',{format:'png',clip:{x:0,y:0,width:1080,height:1920,scale:1}}); return Buffer.from(r.result.data,'base64')};
if(testes){ for(const t of testes.split(',')){ const f=`${saida}-${t}.png`; fs.writeFileSync(f,await shot(+t)); console.log('png',f);} }
else{
 if(fs.existsSync(saida)) fs.unlinkSync(saida);
 const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-i','-','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',saida],{stdio:['pipe','inherit','inherit']});
 const N=Math.round(dur*FPS); console.log('duração',dur.toFixed(2),'s ·',N,'quadros');
 for(let k=0;k<N;k++){ const b=await shot(k/FPS); if(!ff.stdin.write(b)) await new Promise(r=>ff.stdin.once('drain',r)); if(k%150===0) console.log('quadro',k); }
 ff.stdin.end(); await new Promise(r=>ff.on('close',r));
}
sock.close(); chrome.kill('SIGKILL'); fs.rmSync(prof,{recursive:true,force:true});
