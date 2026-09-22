const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),edu=fs.readFileSync(path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),'utf8').replace(/\r/g,'');
const starts=[...edu.matchAll(/^type\s+(\S+)/gm)],bad=[];let total=0;
for(let i=0;i<starts.length;i++){
 const t=starts[i][1],b=edu.slice(starts[i].index,i+1<starts.length?starts[i+1].index:edu.length),p=((b.match(/^stat_pri\s+(.+)$/m)||[])[1]||'').split(',').map(x=>x.trim());
 if(!/^category\s+cavalry$/m.test(b)||+p[3]!==60||+p[4]!==15||p[5]!=='missile')continue;
 total++;const d=(b.match(/^dictionary\s+(.+)$/m)||[])[1]||'';
 if(!/(?:Adams|Lefaucheux|Colt|LeMat|Smith & Wesson|Zündnadelpistole|Bodeo|Gasser|Pistol m\/1850|Revolver m\/1871|Revolver M1873|Remington Model 1875)/i.test(d))bad.push(`${t}\t${d}`);
}
console.log(`Fixed pistol rows: ${total}; unnamed or generic: ${bad.length}`);if(bad.length)console.log(bad.join('\n'));
process.exitCode=bad.length?1:0;
