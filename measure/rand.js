const fs=require('fs');const ref=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));const pred=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));const D=7293.06;
const uni=a=>{a=a.map(c=>[c.in,c.out]).sort((x,y)=>x[0]-y[0]);const o=[];for(const s of a){if(o.length&&s[0]<=o[o.length-1][1])o[o.length-1][1]=Math.max(o[o.length-1][1],s[1]);else o.push([...s]);}return o;};
const tot=a=>a.reduce((s,x)=>s+x[1]-x[0],0);const R=uni(ref.clips);
const ov=(a,b)=>{let i=0,j=0,s=0;while(i<a.length&&j<b.length){s+=Math.max(0,Math.min(a[i][1],b[j][1])-Math.max(a[i][0],b[j][0]));if(a[i][1]<b[j][1])i++;else j++;}return s;};
const lens=pred.clips.map(c=>c.out-c.in);let f=[];for(let k=0;k<2000;k++){const cl=lens.map(L=>{const s=Math.random()*(D-L);return {in:s,out:s+L};});const P=uni(cl);const o=ov(P,R);const p=o/tot(P),r=o/tot(R);f.push(2*p*r/(p+r));}
f.sort((a,b)=>a-b);console.log(JSON.stringify({mean:f.reduce((a,b)=>a+b)/f.length,p05:f[100],p95:f[1900]}));
