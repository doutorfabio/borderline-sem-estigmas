// node render.js pagina.html saida idx N  (60 fps, 3 subquadros por quadro)
const { chromium } = require('playwright'); const path=require('path'); const {spawn}=require('child_process');
const [f,out,idx,N]=process.argv.slice(2); const FPS=60,SUB=3;
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+path.resolve(f)); await p.evaluate(()=>document.fonts.ready);
  const DUR=await p.evaluate(()=>DUR); const total=Math.round(DUR*FPS), per=Math.ceil(total/N), f0=idx*per, f1=Math.min(total,f0+per);
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(FPS*SUB),'-c:v','png','-i','-',
    '-vf',`tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB-1})',setpts=N/(${FPS}*TB)`,'-r',String(FPS),
    '-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p',`${out}_${idx}.mp4`],{stdio:['pipe','inherit','inherit']});
  for(let k=f0;k<f1;k++) for(let s=0;s<SUB;s++){ await p.evaluate(t=>seek(t),(k+s/SUB)/FPS);
    const buf=await p.screenshot({type:'png'}); if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); }
  ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close(); })();
