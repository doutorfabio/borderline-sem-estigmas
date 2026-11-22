const { chromium } = require('playwright');
const { spawn } = require('child_process');
const FPS=30, out=process.argv[2]||'work/video.mp4', only=process.argv[3];
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('http://127.0.0.1:8765/'+(process.env.PAGE||'render.html')+''); await p.evaluate(()=>window.ready);
  const TOTAL=await p.evaluate(()=>window.TOTAL);
  if(only){ for(const t of only.split(',').map(Number)){ const d=await p.evaluate(t=>{draw(t);return document.getElementById('c').toDataURL('image/png');},t);
      require('fs').writeFileSync(`work/f_${t.toFixed(2)}.png`,Buffer.from(d.split(',')[1],'base64'));} await b.close(); return; }
  const N=Math.round(TOTAL*FPS);
  const ff=spawn('ffmpeg',['-y','-f','image2pipe','-framerate',String(FPS),'-i','-','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
  for(let i=0;i<N;i++){ const d=await p.evaluate(t=>{draw(t);return document.getElementById('c').toDataURL('image/jpeg',0.97);},i/FPS);
    if(!ff.stdin.write(Buffer.from(d.split(',')[1],'base64'))) await new Promise(r=>ff.stdin.once('drain',r)); }
  ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close(); console.log('frames',N,'total',TOTAL);
})();
