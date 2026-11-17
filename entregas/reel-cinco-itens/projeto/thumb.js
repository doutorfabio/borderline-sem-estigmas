const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:2});
 await p.goto('file://'+path.resolve(__dirname,'comp/thumb.html')); const info=await p.evaluate(()=>window.ready); console.log(JSON.stringify(info));
 await p.screenshot({path:path.resolve(__dirname,'thumb/thumb_2x.png')}); await b.close();})();
