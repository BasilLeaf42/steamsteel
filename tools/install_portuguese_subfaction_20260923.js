const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const eduFiles=['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt'];
const backup=path.join(root,'tools/backup_before_portuguese_subfaction_20260923');fs.mkdirSync(backup,{recursive:true});
for(const f of [...eduFiles,'data/text/export_units.txt','data/descr_rebel_factions.txt']){const src=path.join(root,f),dst=path.join(backup,f.replaceAll('/','__'));if(!fs.existsSync(dst))fs.copyFileSync(src,dst);}
const infantry=new Set(['merc_port_inf_early','merc_port_inf_mid','merc_port_inf_high']);
const cavalry=new Set(['merc_port_cav_early','merc_port_cav_mid','merc_port_cav_high']);
const remove=new Set(['merc_port_inf','merc_port_lancer']);
function editEdu(input){
 const blocks=input.replace(/\r/g,'').split(/(?=^type\s+)/m),out=[];
 for(let b of blocks){const type=b.match(/^type\s+(.+)$/m)?.[1]?.trim();if(!type){out.push(b);continue;}if(remove.has(type))continue;
  if(infantry.has(type)||cavalry.has(type)){
   b=b.replace(/^attributes\s+(.+)$/m,(m,a)=>'attributes       '+a.split(',').map(x=>x.trim()).filter(x=>x!=='no_custom').join(', '));
   b=b.replace(/^ownership\s+.+$/m,'ownership        slave, spain');
   b=b.replace(/^era\s+([012])\s+.+$/m,(m,e)=>`era ${e}            spain`);
   b=b.replace(/^stat_mental\s+.+$/m,'stat_mental      4, normal, trained');
   b=b.replace(/^stat_sec\s+[^\r\n]+$/m,(m)=>{const a=m.replace(/^stat_sec\s+/,'').split(',').map(x=>x.trim());a[0]='5';a[1]='3';return'stat_sec         '+a.join(', ');});
   b=b.replace(/^stat_cost\s+([^\r\n]+)$/m,(m,row)=>{const a=row.split(',').map(x=>x.trim());a[6]=infantry.has(type)?'5':'1';return'stat_cost        '+a.join(', ');});
   b=b.replace(/^officer\s+[^\r\n]+\n?/gm,'');
   const soldierLine=b.match(/^soldier\s+[^\r\n]+$/m)?.[0];if(!soldierLine)throw Error(`missing soldier ${type}`);
   const officers=infantry.has(type)?(type.endsWith('_high')?['officer          shk_off_1g']:['officer          shk_off_1g','officer          russia_qi']):['officer          shk_off_1g'];
   b=b.replace(soldierLine,soldierLine+'\n'+officers.join('\n'));
   if(type==='merc_port_inf_early')b=b.replace('rifled_musket_bullet_c','rifled_musket_bullet_b');
   if(type==='merc_port_inf_mid')b=b.replace(/^stat_pri\s+[^\r\n]+$/m,'stat_pri         29, 0, rifled_musket_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999').replace(/^stat_cost\s+([^\r\n]+)$/m,(m,row)=>{const a=row.split(',').map(x=>x.trim());a[1]='1200';a[2]='400';a[5]='1200';a[6]='5';a[7]='400';return'stat_cost        '+a.join(', ');});
   if(type==='merc_port_inf_high')b=b.replace('magazine_rifle_bullet_c','magazine_rifle_bullet_b');
   if(type==='merc_port_cav_mid')b=b.replace(/^stat_pri\s+[^\r\n]+$/m,'stat_pri         21, 2, rifled_musket_carbine_bullet_c, 200, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999').replace(/^stat_cost\s+([^\r\n]+)$/m,(m,row)=>{const a=row.split(',').map(x=>x.trim());a[1]='1400';a[2]='467';a[5]='1400';a[6]='1';a[7]='467';return'stat_cost        '+a.join(', ');});
  }
  out.push(b);
 }
 return out.join('').replace(/\n/g,'\r\n');
}
const canonical=editEdu(fs.readFileSync(path.join(root,eduFiles[0]),'utf8'));for(const f of eduFiles)fs.writeFileSync(path.join(root,f),canonical);

// Rebel templates formerly used the compatibility aliases; point them at the
// surviving early records before deleting those aliases.
let rebel=fs.readFileSync(path.join(root,'data/descr_rebel_factions.txt'),'utf8');
rebel=rebel.replace(/\bmerc_port_lancer\b/g,'merc_port_cav_early').replace(/\bmerc_port_inf\b/g,'merc_port_inf_early');
fs.writeFileSync(path.join(root,'data/descr_rebel_factions.txt'),rebel);

// Remove localization records belonging only to the deleted EDU aliases.
const deadKeys=new Set(['merc_port_inf','merc_port_inf_descr','merc_port_inf_descr_short','merc_port_lancer','merc_port_lancer_descr','merc_port_lancer_descr_short','merc_port_inf_compat','merc_port_inf_compat_descr','merc_port_inf_compat_descr_short','merc_port_cav_compat','merc_port_cav_compat_descr','merc_port_cav_compat_descr_short']);
let loc=fs.readFileSync(path.join(root,'data/text/export_units.txt'),'utf8').replace(/\r/g,'');
loc=loc.split(/(?=^\{)/m).filter(chunk=>{const key=chunk.match(/^\{([^}]+)\}/)?.[1];return !key||!deadKeys.has(key);}).join('');
fs.writeFileSync(path.join(root,'data/text/export_units.txt'),loc.replace(/\n/g,'\r\n'));

const check=canonical.replace(/\r/g,'');
for(const type of remove)if(new RegExp(`^type\\s+${type}$`,'m').test(check))throw Error(`duplicate remains ${type}`);
for(const type of [...infantry,...cavalry]){const b=check.split(/(?=^type\s+)/m).find(x=>x.match(/^type\s+(.+)$/m)?.[1]?.trim()===type);if(!b)throw Error(`missing ${type}`);if(/\bno_custom\b/.test(b))throw Error(`still hidden ${type}`);if(!/^ownership\s+slave, spain$/m.test(b))throw Error(`ownership ${type}`);}
console.log('Installed six-record Portuguese subfaction; deleted two compatibility EDU aliases and redirected rebel templates.');
