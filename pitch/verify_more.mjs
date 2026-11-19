const task=await taskSpace(5);const p=task.page('p1');
const fs=await import('node:fs/promises');
const path='D:/orca/projects/cutline-pitch/external_sources.json';
const rows=JSON.parse(await fs.readFile(path,'utf8'));
for(const url of ['https://www.opus.pro/','https://cursor.com/','https://helpx.adobe.com/premiere/desktop/edit-projects/edit-video-using-text-based-editing/detect-and-delete-pauses-in-transcripts.html']){
try{await p.goto(url,{waitUntil:'domcontentloaded',timeout:20000});const data=await p.evaluate(()=>({title:document.title,text:document.body.innerText.slice(0,14000)}));rows.push({url,...data});console.log({url,title:data.title,text:data.text.slice(0,1300)});}catch(e){console.log({url,error:String(e)});}}
await fs.writeFile(path,JSON.stringify(rows,null,2));
