// node render.js idx nWorkers  -> parte_idx.mp4 (180 subquadros/s, tmix=3 -> 60 fps)
const { chromium } = require('playwright'); const path=require('path'); const {spawn}=require('child_process');
const T = require('./tempos.json'); const FPS=60, SUB=3;
const idx=+process.argv[2], N=+process.argv[3];
const total=Math.ceil(T.duracao_total*FPS); const per=Math.ceil(total/N);
const f0=idx*per, f1=Math.min(total,f0+per);
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+path.resolve('render.html')); await p.evaluate(()=>document.fonts.ready);
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(FPS*SUB),'-c:v','png','-i','-',
    '-vf',`tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB-1})',setpts=N/(${FPS}*TB)`,'-r',String(FPS),
    '-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p',`parte_${idx}.mp4`],{stdio:['pipe','inherit','inherit']});
  for(let f=f0; f<f1; f++) for(let s=0;s<SUB;s++){
    const t=(f + s/SUB)/FPS;
    await p.evaluate(t=>seek(t),t);
    const buf=await p.screenshot({type:'png'});
    if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
  }
  ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close(); console.log('ok',idx,f0,f1);
})();
