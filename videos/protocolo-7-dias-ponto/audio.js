const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+require('path').resolve('audio.html'));
const s=await p.evaluate(()=>window.makeAudio());fs.writeFileSync('track.wav',Buffer.from(s,'base64'));await b.close();})();
