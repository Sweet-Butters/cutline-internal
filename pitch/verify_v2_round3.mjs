const task=await taskSpace(7);const p=task.page('p1');const out=[];
for(const url of ['https://vrew.ai/en/payment/pricepolicy','https://www.meplex.co.kr/page/reference']){
try{await p.goto(url);}catch(e){console.log(String(e));}
console.log(await p.snapshot({scope:'full_page'}));out.push({url,text:await p.evaluate(()=>document.body.innerText)});
}
await (await import('node:fs/promises')).writeFile('D:/orca/projects/cutline-pitch/evidence/web-v2-more.json',JSON.stringify(out,null,2));
