const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/index.html');await p.evaluate(()=>window.ready);
const DUR=await p.evaluate(()=>DUR),FPS=60,N=Math.round(DUR*FPS);
const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','60','-i','-','-i','track.wav',
 '-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-profile:v','high','-movflags','+faststart',
 '-af','afade=t=out:st='+(DUR-0.3)+':d=0.3','-c:a','aac','-b:a','192k','-t',String(DUR),'protocolo-7-dias-motion.mp4'],{stdio:['pipe','inherit','inherit']});
for(let i=0;i<N;i++){const buf=await p.evaluate(t=>{seek(t);return document.getElementById('c').toDataURL('image/png').split(',')[1];},i/FPS);
 if(!ff.stdin.write(Buffer.from(buf,'base64')))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('frames',N);})();
