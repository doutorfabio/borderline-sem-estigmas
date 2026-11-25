const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const root=__dirname;const types={'.html':'text/html','.png':'image/png','.woff2':'font/woff2'};
const srv=http.createServer((q,r)=>{const p=path.join(root,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);r.end();return;}r.writeHead(200,{'Content-Type':types[path.extname(p)]||'application/octet-stream'});r.end(d);});}).listen(0);
const N=+process.argv[2],W=+process.argv[3],out=process.argv[4];fs.mkdirSync(out,{recursive:true});
(async()=>{const port=srv.address().port;const b=await chromium.launch();
 await Promise.all([...Array(W).keys()].map(async w=>{const pg=await b.newPage({viewport:{width:1080,height:1080},deviceScaleFactor:1});
  pg.on('pageerror',e=>console.log('ERR',e.message));
  await pg.goto(`http://localhost:${port}/index.html`);await pg.waitForFunction(()=>window.READY===true,{timeout:30000});
  const el=await pg.$('#stage');
  const LIST=process.argv[5]?process.argv[5].split(',').flatMap(r=>{const[a,b]=r.split('-').map(Number);return [...Array((b??a)-a+1).keys()].map(k=>a+k);}):[...Array(N).keys()];
  for(let j=w;j<LIST.length;j+=W){const i=LIST[j];await pg.evaluate(f=>window.seek(f),i/2);await pg.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
    await el.screenshot({path:path.join(out,`${String(i).padStart(4,'0')}.png`)});}
 }));await b.close();srv.close();console.log('done');})();
