const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const root=__dirname;const types={'.html':'text/html','.png':'image/png','.woff2':'font/woff2','.js':'text/javascript'};
const srv=http.createServer((q,r)=>{const p=path.join(root,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);r.end();return;}r.writeHead(200,{'Content-Type':types[path.extname(p)]||'application/octet-stream'});r.end(d);});}).listen(0);
(async()=>{const port=srv.address().port;const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1080},deviceScaleFactor:1});
 pg.on('console',m=>console.log('console:',m.text()));pg.on('pageerror',e=>console.log('ERR',e.message));
 await pg.goto(`http://localhost:${port}/index.html`);await pg.waitForFunction(()=>window.READY===true||false,{timeout:20000}).catch(async e=>{console.log('not ready')});
 const [out,...frames]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
 const el=await pg.$('#stage');
 for(const fr of frames){const f=parseFloat(fr);await pg.evaluate(f=>window.seek(f),f);await pg.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
   await el.screenshot({path:path.join(out,`f${String(fr).padStart(3,'0')}.png`)});}
 console.log(JSON.stringify(await pg.evaluate(()=>window.M&&{lock:M.lock,kp:M.kp,word:M.word})));
 await b.close();srv.close();})();
