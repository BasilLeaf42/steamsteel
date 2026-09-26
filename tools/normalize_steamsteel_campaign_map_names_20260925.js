const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const mapPath=path.join(root,'data/world/maps/map_steamsteel/descr_regions.txt');
const runtime=path.join(root,'data/text/imperial_campaign_regions_and_settlement_names.txt');
const canonical=path.join(root,'data/text/text_steamsteel/imperial_campaign_regions_and_settlement_names.txt');
const decode=p=>{const b=fs.readFileSync(p);return b[0]===0xff&&b[1]===0xfe?b.subarray(2).toString('utf16le'):b.toString('utf8');};
const mapLines=fs.readFileSync(mapPath,'utf8').replace(/\r/g,'').split('\n'),regions=[];
for(let i=0;i<mapLines.length;i++)if(/^[A-Za-z0-9_]+_Province\s*$/.test(mapLines[i]))regions.push({region:mapLines[i].trim(),settlement:mapLines[i+1].trim()});
const source=decode(runtime),lines=source.replace(/\r/g,'').split('\n'),latest=new Map();
for(const line of lines){const m=line.match(/^\{([^}]+)\}\s*(.*)$/);if(m)latest.set(m[1],m[2].trim());}
const corrections=new Map([
  ['Dakota_Province','Great Lakes States'],
  ['Utah_Province','Southwest Territories'],
  ['Nuevo_Mexico','Tucson'],
  ['Cholula_Province','New Granada'],
  ['Mozambique_Province','Mozambique'],
  ['Ajan_Province','Khorasan'],
  ['Cracow','Lemberg'],
  ['Muramamsk','Kola'],
  ['NFinlande','Helsingfors'],
]);
for(const [k,v]of corrections)latest.set(k,v);
const active=new Set(regions.flatMap(x=>[x.region,x.settlement]));
for(const k of active)if(!latest.has(k)||!latest.get(k))throw new Error(`Missing active map localisation: ${k}`);
const kept=lines.filter(line=>{const m=line.match(/^\{([^}]+)\}/);return !m||!active.has(m[1]);});
while(kept.length&&kept.at(-1)==='')kept.pop();
kept.push('',';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;','; Steam & Steel authoritative active campaign map names (deduplicated)',';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;');
const emitted=new Set();
for(const x of regions)for(const k of[x.region,x.settlement])if(!emitted.has(k)){kept.push(`{${k}}${latest.get(k)}`);emitted.add(k);}
const output='\ufeff'+kept.join('\r\n')+'\r\n';
fs.writeFileSync(canonical,Buffer.from(output,'utf16le'));fs.copyFileSync(canonical,runtime);
console.log(`Normalized ${emitted.size} active region/settlement keys; canonical and runtime copies written.`);
