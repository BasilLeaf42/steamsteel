const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const files=['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt'];
const backup=path.join(root,'tools/backup_before_nonwestern_custom_availability_20260923');
fs.mkdirSync(backup,{recursive:true});
for(const f of files){const dst=path.join(backup,f.replaceAll('/','__'));if(!fs.existsSync(dst))fs.copyFileSync(path.join(root,f),dst);}

const factions=new Set(['moors','lith','turks','golden','egypt','timurids','cuman','bulga','cru','byzantium','papal_states','saxons']);
const split=s=>(s||'').split(/[\s,]+/).filter(Boolean);
function parse(text){
 const out=[];
 for(const b of text.replace(/\r/g,'').split(/(?=^type\s+)/m)){
  const type=b.match(/^type\s+(.+)$/m)?.[1]?.trim();if(!type)continue;
  const category=b.match(/^category\s+(\S+)/m)?.[1]||'';
  const cls=b.match(/^class\s+(\S+)/m)?.[1]||'';
  const attrs=split(b.match(/^attributes\s+(.+)$/m)?.[1]);
  const pri=b.match(/^stat_pri\s+(.+)$/m)?.[1]||'';
  const range=+(pri.split(',')[3]||0);
  const strength=+(b.match(/^soldier\s+[^,]+,\s*([\d.]+)/m)?.[1]||0);
  const cost=(b.match(/^stat_cost\s+(.+)$/m)?.[1]||'').split(',').map(x=>x.trim());
  const eras={0:[],1:[],2:[]};for(const m of b.matchAll(/^era\s+([012])\s+(.+)$/gm))eras[m[1]].push(...split(m[2]));
  out.push({type,category,class:cls,attrs,pri,range,strength,limit:+(cost[6]||0),eras});
 }
 return out;
}
function role(u){
 if(u.category==='siege')return u.strength<=10?'light_artillery':'heavy_artillery';
 if(u.category==='cavalry')return /missile_gunpowder/.test(u.pri)&&u.range>60?'carbineers':'cavalry';
 if(u.category==='infantry'&&/missile_gunpowder/.test(u.pri))return'line';
 if(u.category==='infantry'&&!/\bmissile\b/.test(u.pri))return'melee';
 return'other';
}

let text=fs.readFileSync(path.join(root,files[0]),'utf8').replace(/\r/g,'');
// Obsolete wall-gun and hill formations remain available in earlier periods but
// do not inflate Afghanistan's late modern roster beyond five missile types.
for(const type of ['afg_pashtun_wall_gunners','afg_tajik_hillmen']){
 const escaped=type.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const blockRe=new RegExp(`(^type\\s+${escaped}\\s*$[\\s\\S]*?)(?=^type\\s+|(?![\\s\\S]))`,'m');
 text=text.replace(blockRe,block=>{
  return block.replace(/^era\s+2\s+(.+)$/m,(line,list)=>{
   const left=split(list).filter(x=>x!=='timurids');
   return left.length?`era 2            ${left.join(', ')}`:'';
  });
 });
}
// Indian firearm records remain one each. Continue the irregular gingal teams
// and Maratha musket battalions into the late roster so every period has four
// distinct firearm choices without multiplying any one record.
for(const type of ['india_militia','indian_new_musk']){
 const escaped=type.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const blockRe=new RegExp(`(^type\\s+${escaped}\\s*$[\\s\\S]*?)(?=^type\\s+|(?![\\s\\S]))`,'m');
 text=text.replace(blockRe,block=>{
  const era2=block.match(/^era\s+2\s+(.+)$/m);
  if(era2){const list=split(era2[1]);if(!list.includes('bulga'))list.push('bulga');return block.replace(/^era\s+2\s+.+$/m,`era 2            ${list.join(', ')}`);}
  const ownership=block.match(/^ownership\s+.+$/m);
  if(!ownership)throw Error(`missing ownership ${type}`);
  return block.replace(/^ownership\s+.+$/m,m=>`${m}\nera 2            bulga`);
 });
}
const units=parse(text),desired=new Map();
const inScope=u=>[0,1,2].some(e=>u.eras[e].some(f=>factions.has(f)));

// Every national record remains available. Infantry density is measured across
// the complete foot arm (firearms, melee troops, and traditional missiles), so
// every distinct infantry record starts at one rather than stacking a Western
// firearm target on top of auxiliaries. Cavalry is one and artillery two.
for(const u of units){
 if(!inScope(u)||u.attrs.includes('mercenary_unit')||u.category==='ship')continue;
 const r=role(u);
 if(u.category==='infantry'||r==='cavalry'||r==='carbineers')desired.set(u.type,1);
 else if(r==='light_artillery'||r==='heavy_artillery')desired.set(u.type,2);
 else if(u.limit<1)desired.set(u.type,1);
}

// Recruitment-density allocations. Values above one identify the principal
// recruiting formation while preserving at least one of every distinct type.
const extra={
 // Morocco: six total foot formations per period, including tribal infantry.
 mor_askar_early:2,mor_askar_mid:2,mor_askar_high:3,
 // Zulu: melee formations are the recruiting backbone. A spanning record makes
 // the late total seven once the early/mid minimum of six is met.
 zulu_guard:3,
 // Ottoman Empire: high density (eight firearm formations per period).
 ott_nizamiye_early:2,ott_redif_early:2,
 ott_nizamiye_mid:2,ott_redif_mid:2,
 ott_nizamiye_high:2,ott_redif_high:2,ott_hassa_high:2,
 // Oman: five total foot formations.
 oma_regular_early:3,oma_regular_mid:2,oma_regular_high:2,
 // Qajar Persia: six total foot formations.
 qaj_sarbaz_early:2,qaj_guard_early:2,qaj_sarbaz_high:2,
 // Afghanistan: lower density; the late roster already exceeds the target by
 // distinct types and therefore remains one apiece.
 afg_regular_early:2,
 // Turkestan: five total infantry formations; cavalry exception retained from its
 // documented faction distinction in AGENTS.md.
 buk_guard:2,kashgar_inf:3,kok_inf:5,kok_cav:3,kok_royal_cav:2,
 // Indian states: firearm formations remain one each; melee availability carries
 // the roster instead of multiplying the spanning Sikh firearm record.
 ind_bhutan_warrior:3,
 // Siam: five total foot formations per period.
 siam_inf:2,siam_late_inf:3,
 // Qing: eight total foot formations, including Braves, spears, and archers.
 qing_baqi_gunmen:2,qing_village_braves:2,qing_green_banner_regulars:3,
 qing_green_banner_late:2,
 // Ethiopia: missile availability rises only to five; the Fanno/Cawa-style
 // melee body supplies the remaining foot strength.
 eth_rifled_musketeers:2,ethiopian_warband:2
};
for(const [type,n] of Object.entries(extra)){
 const u=units.find(x=>x.type===type);if(!u||!inScope(u)||u.attrs.includes('mercenary_unit'))throw Error(`invalid override ${type}`);
 desired.set(type,n);
}

// Repair the two shared mercenary records accidentally altered by the Western
// pass. Mercenary/subfaction availability is outside national density totals.
desired.set('mongol_hevcav',4);
desired.set('merc_kok_royal_cav',2);

for(const [type,n] of desired){
 const escaped=type.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const re=new RegExp(`(^type\\s+${escaped}\\s*$[\\s\\S]*?^stat_cost\\s+)([^\\r\\n]+)`,'m');let hit=false;
 text=text.replace(re,(all,head,row)=>{hit=true;const a=row.split(',').map(x=>x.trim());if(a.length!==8)throw Error(`stat_cost fields ${type}`);a[6]=String(n);return head+a.join(', ');});
 if(!hit)throw Error(`missing stat_cost ${type}`);
}

const expectedFoot={
 moors:[6,6,6],lith:[6,6,7],turks:[8,8,8],golden:[5,5,5],egypt:[6,6,6],
 timurids:[5,5,5],cuman:[5,5,5],bulga:[9,8,7],cru:[5,5,5],
 byzantium:[8,8,8],papal_states:[6,7,8],saxons:[27,24,28]
};
const check=parse(text),issues=[];
for(const [f,want] of Object.entries(expectedFoot))for(const era of [0,1,2]){
 const got=check.filter(u=>u.eras[era].includes(f)&&!u.attrs.includes('mercenary_unit')&&u.category==='infantry').reduce((s,u)=>s+u.limit,0);
 if(got!==want[era])issues.push(`${f} era ${era}: total foot ${got} != ${want[era]}`);
}
const missileCapExceptions=new Set(['turks','egypt','byzantium','saxons']);
for(const f of factions)if(!missileCapExceptions.has(f))for(const era of [0,1,2]){
 // Light melee formations with a one-shot javelin precursor remain melee for
 // roster accounting; dedicated firearm/archer formations use class missile.
 const got=check.filter(u=>u.eras[era].includes(f)&&!u.attrs.includes('mercenary_unit')&&u.category==='infantry'&&u.class==='missile').reduce((s,u)=>s+u.limit,0);
 if(got>5)issues.push(`${f} era ${era}: missile infantry ${got} > 5`);
}
for(const u of check){
 if(!inScope(u)||u.attrs.includes('mercenary_unit')||u.category==='ship')continue;
 const r=role(u);
 if(u.limit<1)issues.push(`${u.type}: unavailable`);
 if((r==='cavalry'||r==='carbineers')&&u.type!=='kok_cav'&&u.type!=='kok_royal_cav'&&u.limit!==1)issues.push(`${u.type}: cavalry limit ${u.limit}`);
 if((r==='light_artillery'||r==='heavy_artillery')&&u.limit!==2)issues.push(`${u.type}: artillery limit ${u.limit}`);
}
if(issues.length)throw Error(issues.join('\n'));
const out=text.replace(/\n/g,'\r\n');for(const f of files)fs.writeFileSync(path.join(root,f),out);
console.log(`Standardized ${desired.size} non-Western/core availability records; restored two shared mercenary limits.`);
