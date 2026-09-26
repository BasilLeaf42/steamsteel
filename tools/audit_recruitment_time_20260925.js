const fs=require('fs');
const s=fs.readFileSync('data/tow_steamsteel/export_descr_unit.txt','utf8'),m=fs.readFileSync('data/export_descr_unit.txt','utf8');
const rows=[];let r=null;
for(const line of s.split(/\r?\n/)){let x;if((x=line.match(/^type\s+(.+)$/))){if(r)rows.push(r);r={type:x[1],category:'',attributes:'',time:null};}else if(r&&(x=line.match(/^category\s+(.+)$/)))r.category=x[1];else if(r&&(x=line.match(/^attributes\s+(.+)$/)))r.attributes=x[1];else if(r&&(x=line.match(/^stat_cost\s+(\d+)/)))r.time=+x[1];}if(r)rows.push(r);
const badCommand=rows.filter(x=>/(?:^|,\s*)general_unit(?:\s*,|$)/.test(x.attributes)&&x.category!=='ship'&&x.category!=='siege'&&x.time!==1);
const badRange=rows.filter(x=>x.category==='infantry'&&!/(?:^|,\s*)general_unit(?:\s*,|$)/.test(x.attributes)&&![2,3,4].includes(x.time)||x.category==='cavalry'&&!/(?:^|,\s*)general_unit(?:\s*,|$)/.test(x.attributes)&&![3,4,5].includes(x.time));
console.log(JSON.stringify({records:rows.length,mirrorsMatch:s===m,badCommand:badCommand.map(x=>x.type),badLandRange:badRange.map(x=>x.type),distribution:Object.fromEntries([...new Set(rows.map(x=>x.time))].sort((a,b)=>a-b).map(t=>[t,rows.filter(x=>x.time===t).length]))},null,2));
if(s!==m||badCommand.length||badRange.length)process.exitCode=1;
