const task = await taskSpace('Cutline v2 public verification');
console.log({space:task.spaceId});
const p=task.page('p1');
const urls=['https://cursor.com/pricing','https://www.descript.com/pricing','https://www.opus.pro/pricing','https://vrew.ai/en/pricing'];
const results=[];
for(const url of urls){try{await p.goto(url); const body=await p.evaluate(()=>document.body.innerText);results.push({url,text:body}); console.log({url,text:body.slice(0,15000)});}catch(e){results.push({url,error:String(e)});console.log(String(e));}}
await (await import('node:fs/promises')).writeFile('D:/orca/projects/cutline-pitch/evidence/web-v2-prices.json',JSON.stringify(results,null,2));
