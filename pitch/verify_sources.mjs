const task = await taskSpace('Cutline pitch references');
console.log({spaceId: task.spaceId});
const p = task.page('p1');
const urls = ['https://www.descript.com/','https://www.capcut.com/','https://vrew.ai/en/','https://www.opus.pro/','https://github.com/WyattBlue/auto-editor','https://arxiv.org/abs/1804.06604','https://arxiv.org/abs/1903.11328','https://graphics.stanford.edu/papers/roughcut/','https://github.com/SYSTRAN/faster-whisper'];
const results=[];
for(const url of urls){try{await p.goto(url,{timeout:20000}); const data=await p.evaluate(()=>({title:document.title,text:document.body.innerText.slice(0,14000)}));results.push({url,...data}); console.log(JSON.stringify({url,title:data.title,text:data.text.slice(0,850)}));}catch(e){results.push({url,error:String(e)});console.log({url,error:String(e)});}}
const fs=await import('node:fs/promises');
await fs.writeFile('D:/orca/projects/cutline-pitch/external_sources.json',JSON.stringify(results,null,2));
