const {chromium}=require('/opt/node-tools/node_modules/playwright');const {spawn}=require('child_process');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/index.html');await p.evaluate(()=>window.ready);
const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate','60','-c:v','png','-i','-','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-force_key_frames','12','-bf','0','-x264-params','zones=721,899,q=51:keyint=600','-r','60','video.mp4']);
let still=null;
for(let f=0;f<900;f++){const t=f/60; let buf;
 if(t>=12&&still){buf=still}else{await p.evaluate(t=>window.seek(t),t);buf=await p.screenshot({type:'png'}); if(f===720) still=buf;}
 if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end(); await new Promise(r=>ff.on('close',r)); console.log('pops',JSON.stringify(await p.evaluate(()=>window.__pops))); await b.close();})();
