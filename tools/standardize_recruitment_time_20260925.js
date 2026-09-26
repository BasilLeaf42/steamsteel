const fs=require('fs');
const eduPaths=['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt'];
const loc=new Map();
for(const line of fs.readFileSync('data/text/export_units.txt','utf8').split(/\r?\n/)){const m=line.match(/^\{([^}]+)\}(.*)$/);if(m)loc.set(m[1],m[2]);}

function rewrite(text){
  const nl=text.includes('\r\n')?'\r\n':'\n', final=text.endsWith('\n'), lines=text.split(/\r?\n/), records=[]; let r=null;
  function finish(){if(!r)return; const long=loc.get(`${r.dictionary}_descr`)||''; const q=(long.match(/Quality:\s*([^\\\r\n]+)/i)?.[1]||'').trim().toLowerCase();
    const command=/(?:^|,\s*)general_unit(?:\s*,|$)/.test(r.attributes);
    let quality='regular';
    if(/elite/.test(q))quality='elite';
    else if(/militia|levy|irregular|reserve/.test(q)||r.attributes.split(',').map(x=>x.trim()).includes('free_upkeep_unit'))quality='militia';
    else if(r.training==='highly_trained'&&r.morale>=5)quality='elite';
    r.quality=quality;r.command=command;records.push(r);r=null;}
  for(let i=0;i<lines.length;i++){const line=lines[i];let m;
    if((m=line.match(/^type\s+(.+?)\s*$/))){finish();r={type:m[1],dictionary:'',category:'',attributes:'',morale:0,discipline:'',training:'',costIndex:-1,cost:null};}
    else if(r&&(m=line.match(/^dictionary\s+([^;\s]+)/)))r.dictionary=m[1];
    else if(r&&(m=line.match(/^category\s+(.+?)\s*$/)))r.category=m[1];
    else if(r&&(m=line.match(/^attributes\s+(.+?)\s*$/)))r.attributes=m[1];
    else if(r&&(m=line.match(/^stat_mental\s+(\d+)\s*,\s*([^,]+)\s*,\s*([^,\s]+)/))){r.morale=+m[1];r.discipline=m[2].trim();r.training=m[3].trim();}
    else if(r&&(m=line.match(/^stat_cost\s+(.+)$/))){r.costIndex=i;r.cost=m[1].split(',').map(x=>x.trim());}
  }finish();
  const counts={militia:0,regular:0,elite:0,command:0,untouched:0,changed:0};
  for(const u of records){if(!u.cost||u.cost.length<8)throw Error(`Invalid stat_cost: ${u.type}`);
    if(u.category==='ship'||u.category==='siege'){counts.untouched++;continue;}
    let wanted;if(u.command){wanted=1;counts.command++;}else{wanted={militia:2,regular:3,elite:4}[u.quality]+(u.category==='cavalry'?1:0);counts[u.quality]++;}
    if(+u.cost[0]!==wanted){u.cost[0]=String(wanted);lines[u.costIndex]=`stat_cost        ${u.cost.join(', ')}`;counts.changed++;}
  }
  let out=lines.join(nl);if(!final&&out.endsWith(nl))out=out.slice(0,-nl.length);return{out,counts,records};
}
let expected=null;
for(const p of eduPaths){const result=rewrite(fs.readFileSync(p,'utf8'));if(expected!==null&&result.out!==expected)throw Error(`EDU mirror mismatch before write: ${p}`);expected=result.out;fs.writeFileSync(p,result.out,'utf8');console.log(`${p}: ${JSON.stringify(result.counts)}`);}
