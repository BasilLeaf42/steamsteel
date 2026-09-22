const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'..'),eduPath=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),locPath=path.join(root,'data/text/export_units.txt');
function read(file){const b=fs.readFileSync(file);return {text:(b[0]===255&&b[1]===254?b.toString('utf16le'):b.toString('utf8')).replace(/^\uFEFF/,''),utf16:b[0]===255&&b[1]===254};}function write(file,s,t){const b=Buffer.from(t,s.utf16?'utf16le':'utf8');fs.writeFileSync(file,s.utf16?Buffer.concat([Buffer.from([255,254]),b]):b)}
const edu=read(eduPath).text,ls=read(locPath);let loc=ls.text;const esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),get=k=>(loc.match(new RegExp('^\\{'+esc(k)+'\\}([^\\r\\n]*)','m'))||[])[1]?.trim()??null;
const rows=edu.split(/(?=^type\s+)/m).filter(b=>/^type\s+/m.test(b)).map(b=>({b,type:(b.match(/^type\s+(.+)$/m)||[])[1]?.trim(),dict:(b.match(/^dictionary\s+([^\s;]+)/m)||[])[1],comment:(b.match(/^dictionary\s+\S+\s*;\s*(.+)$/m)||[])[1]?.trim()||'',cat:(b.match(/^category\s+(\S+)/m)||[])[1],soldier:(b.match(/^soldier\s+([^,]+)/m)||[])[1]}));
let added=0;const lines=[];
for(const r of rows){if(!r.dict||r.cat==='ship'||r.cat==='siege')continue;const missing=[r.dict,r.dict+'_descr',r.dict+'_descr_short'].filter(k=>get(k)===null);if(!missing.length)continue;
 const donor=rows.find(x=>x!==r&&x.soldier===r.soldier&&x.dict&&get(x.dict)!==null&&get(x.dict+'_descr_short')!==null);
 const visible=get(r.dict)||r.comment.replace(/\s*\((?:Early|Mid|Late|High);[^)]*\)\s*$/,'').trim()||r.type.replace(/_/g,' ');
 const donorShort=donor?get(donor.dict+'_descr_short'):'';const tuple=(r.comment.match(/\(([^()]*(?:Rifle|Musket|Carbine|Revolver|Pistol|Arquebus|Harquebus)[^()]*)\)\s*$/i)||donorShort.match(/\(([^()]*(?:Rifle|Musket|Carbine|Revolver|Pistol|Arquebus|Harquebus)[^()]*)\)/i)||[])[1];
 for(const k of missing){let value;if(k===r.dict)value=visible;else if(k.endsWith('_descr'))value=`${visible}.`;else value=tuple?`${visible.replace(/\s*\((?:Early|Mid|Late)\)$/,'')} (${tuple.replace(/^(?:Early|Mid|Late|High);\s*/i,'')})`:visible;lines.push(`{${k}}${value}`);added++;}
}
if(lines.length){loc=loc.replace(/\s*$/,'\r\n\r\n')+lines.join('\r\n')+'\r\n';write(locPath,ls,loc);}console.log(JSON.stringify({keysAdded:added,records:lines.length}));
