const task=await taskSpace(7);const p=task.page('p1');const out=[];
for(const url of ['https://vrew.ai/en/','https://www.opus.pro/pricing']){
 try{await p.goto(url);}catch(e){console.log(String(e));}
 console.log({url,text:(await p.evaluate(()=>document.body.innerText)).slice(0,1000),links:await p.evaluate(()=>Array.from(document.querySelectorAll('a')).filter(a=>/pric/i.test(a.textContent)).map(a=>({text:a.textContent,url:a.href})).slice(0,10))});
 out.push({url,text:await p.evaluate(()=>document.body.innerText)});
}
await (await import('node:fs/promises')).writeFile('D:/orca/projects/cutline-pitch/evidence/web-v2-prices2.json',JSON.stringify(out,null,2));
