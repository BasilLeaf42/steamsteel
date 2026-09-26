const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const edbPath=path.join(root,'data/tow_steamsteel/export_descr_buildings.txt'),mirror=path.join(root,'data/export_descr_buildings.txt');
const eduPath=path.join(root,'data/tow_steamsteel/export_descr_unit.txt');
const factions=['scotland','denmark','poland','aztecs','england','france','hre','spain','portugal','sicily','normans','mongols','venice','russia','hungary','moors','teu','lith','turks','golden','egypt','timurids','cuman','bulga','cru','byzantium','papal_states','saxons'];
const fallback={scotland:['mexico'],denmark:['peru'],poland:['brazil'],aztecs:['argentina'],england:['uk'],france:['france'],hre:['prussia'],spain:['spain'],portugal:['netherlands'],sicily:['denmark'],normans:['sweden','norway'],mongols:['greece'],venice:['italy'],russia:['russia'],hungary:['austria','hungary'],moors:['morocco'],teu:['south_africa'],lith:['zululand'],turks:['ottoman'],golden:['muscat'],egypt:['persia'],timurids:['afghanistan'],cuman:['kokand'],bulga:['india'],cru:['siam'],byzantium:['china'],papal_states:['ethiopia'],saxons:['japan']};
const westernHome={scotland:['mexico'],denmark:['peru'],poland:['brazil'],aztecs:['argentina'],england:['uk'],france:['france'],hre:['prussia'],spain:['spain'],portugal:['netherlands'],sicily:['denmark'],normans:['sweden','norway'],mongols:['greece'],venice:['italy'],russia:['russia'],hungary:['austria','hungary'],teu:['south_africa']};
const europeanCore=new Set(['england','france','hre','spain','portugal','sicily','normans','mongols','venice','hungary']);
const geographyOverrides=new Map([
  ['england|uk_gurkhas_high',['india']],
  ['france|fra_spahis_mid',['north_africa']],['france|fra_zouaves_early',['north_africa']],
  ['hre|pru_kolonialreiter_high',['sub_sahara']],['hre|pru_schutztruppe_high',['sub_sahara']],
  ['spain|spa_col_inf_early',['east_indies']],['spain|spa_col_inf_high',['east_indies']],['spain|spa_col_cav_mid',['east_indies']],
  ['venice|libya_inf',['north_africa']],['golden|oma_baluchi_musketeers',['persia']],
  ['cuman|uyghur_camel_cav',['steppe']],['egypt|merc_kok_royal_cav',['steppe']],
]);
const tibetanCampaignUnits=new Set(['merc_tib_inf','merc_tib_noble_cav','mercs_tib_monks','tib_heavy_spear','tib_horse_archer','tib_militia','tib_roy_inf','tib_tribal_archer']);
const excludedCampaignSubfactions=new Set([
  'merc_port_inf_early','merc_port_inf_mid','merc_port_inf_high','merc_port_cav_early','merc_port_cav_mid','merc_port_cav_high',
  'merc_aceh_marines','merc_aceh_noble','merc_aceh_reg','merc_aceh_gold','merc_aceh_warband','merc_aceh_inf',
  'merc_tib_temple_guard','taipingguners','taiping_inf','taiping_light','taiping_w',
  'korean_archers','Korean Byeolgigun','Korean Gimagungsu','Korean Musketeers','Korean Pikemen','korean_rifles_mercs','korean_cav_mercs',
  'mahdist_inf','mahdist_camel_cav','mahdist_cav','Ethiopia Sudanese Musketeers','Ethiopia Sudanese Warriors',
  'Japan Ainu Archers','Japan Ainu Geberu','Japan Ainu Minieru','Japan Ainu Teppo',
  'Japan Heimin Mob','Japan Heimin Partisans','Japan Heimin Partisans Geberu','Japan Heimin Partisans Minieru','Japan Ishin Shishi','Japan Ronin','Japan Shizoku','Japan Teppotai Merc',
]);
const uniqueNamedCampaignExclusions=new Set(['Japan Enomoto Takeaki','Japan Hijikata Toshizo','Japan Itagaki Taisuke','Japan Jules Brunet','Japan Kondo Isami','Japan Matsudaira Katamori','Japan Saigo Takamori 1860','Japan Sakamoto Ryoma','Japan Takeda Ayasaburo','Japan Tokugawa Yoshinobu']);
const selected=new Set(factions);

function parseEdu(s){const map=new Map();let r=null;for(const line of s.split(/\r?\n/)){let m;if((m=line.match(/^type\s+(.+)$/))){if(r)map.set(r.type,r);r={type:m[1].trim(),dictionary:'',category:'',klass:'',attributes:'',training:'',morale:0,discipline:'',projectile:'',cost:[],eras:new Map()};}else if(!r)continue;else if((m=line.match(/^dictionary\s+([^;\s]+)(?:\s*;\s*(.*))?/))){r.dictionary=m[1];r.label=m[2]||'';}else if((m=line.match(/^category\s+(.+)$/)))r.category=m[1].trim();else if((m=line.match(/^class\s+(.+)$/)))r.klass=m[1].trim();else if((m=line.match(/^attributes\s+(.+)$/)))r.attributes=m[1];else if((m=line.match(/^stat_mental\s+(\d+)\s*,\s*([^,]+)\s*,\s*([^,\s]+)/))){r.morale=+m[1];r.discipline=m[2].trim();r.training=m[3].trim();}else if((m=line.match(/^stat_pri\s+[^,]+\s*,\s*[^,]+\s*,\s*([^,\s]+)/)))r.projectile=m[1];else if((m=line.match(/^stat_cost\s+(.+)$/)))r.cost=m[1].split(',').map(x=>x.trim());else if((m=line.match(/^era\s+([012])\s+(.+)$/)))r.eras.set(+m[1],m[2].split(',').map(x=>x.trim()).filter(Boolean));}if(r)map.set(r.type,r);return map;}
const edu=parseEdu(fs.readFileSync(eduPath,'utf8'));
let text=fs.readFileSync(edbPath,'utf8').replace(/\r/g,'');

// Capture the surviving legacy roster, geography, family, and artillery tier before removal.
const info=new Map();let building='',level='';
for(const line of text.split('\n')){let m;if((m=line.match(/^building\s+(\S+)/)))building=m[1];if((m=line.match(/^\s{8}(\S+)\s+(?:city|castle)\s+requires\b/)))level=m[1];if(!/^\s*recruit_pool\s+/.test(line))continue;
  const u=line.match(/recruit_pool\s+"([^"]+)"\s+(\S+)\s+(\S+)\s+(\S+)/),fm=line.match(/factions\s*\{([^}]*)\}/);if(!u||!fm)continue;const unit=u[1],def=edu.get(unit);if(!def||def.category==='ship')continue;
  for(const f of fm[1].split(',').map(x=>x.trim()).filter(Boolean).filter(x=>selected.has(x))){const k=`${f}|${unit}`;if(!info.has(k))info.set(k,{faction:f,unit,geos:new Set(),legacyLines:[],families:new Set(),artMin:99});const x=info.get(k);x.legacyLines.push(line);x.families.add(building);const g=line.match(/(?<!not\s)hidden_resource\s+(\w+)/);if(g)x.geos.add(g[1]);const max=+u[4];if(building==='cannon'&&max>=1){const idx={gunsmith:0,cannon_maker:1,cannon_foundry:2,royal_arsenal:3}[level];if(idx!==undefined)x.artMin=Math.min(x.artMin,idx);}}
}
// EDU era membership is the authoritative national campaign roster. Legacy EDB membership is not.
const eligibleCore=(d,f)=>d.category!=='ship'&&!d.attributes.split(',').map(v=>v.trim()).includes('no_custom')&&!d.attributes.split(',').map(v=>v.trim()).includes('mercenary_unit')&&!excludedCampaignSubfactions.has(d.type)&&!uniqueNamedCampaignExclusions.has(d.type)&&!/custom battles? only/i.test(d.label||'')&&[...d.eras.values()].some(list=>list.includes(f));
for(const [key,x] of info)if(!eligibleCore(edu.get(x.unit),x.faction)&&!tibetanCampaignUnits.has(x.unit))info.delete(key);
for(const faction of factions)for(const d of edu.values())if(eligibleCore(d,faction)){const k=`${faction}|${d.type}`;if(!info.has(k))info.set(k,{faction,unit:d.type,geos:new Set(fallback[faction]),legacyLines:[],families:new Set(),artMin:99});}
// Campaign exception: Tibetan formations are recruitable by both Qing and Turkestan.
for(const faction of ['byzantium','cuman'])for(const unit of tibetanCampaignUnits){const k=`${faction}|${unit}`;if(!info.has(k))info.set(k,{faction,unit,geos:new Set(['tibet']),legacyLines:[],families:new Set(['barracks']),artMin:99});}
// Other custom-battle subfactions do not enter campaign building recruitment.
for(const [key,x] of info)if(excludedCampaignSubfactions.has(x.unit))info.delete(key);
// Building recruitment excludes EDU mercenaries; Tibet is the sole approved regional exception.
for(const [key,x] of info)if(edu.get(x.unit)?.attributes.split(',').map(v=>v.trim()).includes('mercenary_unit')&&!tibetanCampaignUnits.has(x.unit))info.delete(key);

// Remove only selected faction access from non-ship rows, preserving other owners.
const kept=[];
for(const line of text.split('\n')){if(/^;remaining factions standardized recruitment\b/.test(line))continue;if(!/^\s*recruit_pool\s+/.test(line)){kept.push(line);continue;}const um=line.match(/recruit_pool\s+"([^"]+)"/),fm=line.match(/factions\s*\{([^}]*)\}/);const def=um&&edu.get(um[1]);if(!fm||def?.category==='ship'){kept.push(line);continue;}const owners=fm[1].split(',').map(x=>x.trim()).filter(Boolean),next=owners.filter(x=>!selected.has(x));if(next.length===owners.length){kept.push(line);continue;}if(next.length)kept.push(line.replace(fm[0],`factions { ${next.join(', ')}, }`).trimEnd());}
text=kept.join('\n');

const eventName=y=>y===1880?'military_reforms_1':y===1900?'military_reforms_2':`military_reforms_${y}`;
const condition=(start,end)=>{const p=[];if(start)p.push(`event_counter ${eventName(start)} 1`);if(end)p.push(`not event_counter ${eventName(end)} 1`);return p;};
const eraWindow=eras=>{const a=[...eras].sort();if(a.join()==='0')return[0,1870];if(a.join()==='1')return[1870,1890];if(a.join()==='2')return[1890,0];if(a.join()==='0,1')return[0,1890];if(a.join()==='1,2')return[1870,0];return[0,0];};
const round5=y=>Math.round(y/5)*5;
function explicitEras(def,f,legacy){const own=[];for(const [e,list]of def.eras)if(list.includes(f))own.push(e);if(own.length)return new Set(own);const t=def.type;if(/_early$/.test(t))return new Set([0]);if(/_mid$/.test(t))return new Set([1]);if(/_(?:high|late)$/.test(t))return new Set([2]);const joined=legacy.join(' ');if(/event_counter military_reforms_1890 1/.test(joined)&&!/not event_counter military_reforms_1890 1/.test(joined))return new Set([2]);if(/event_counter military_reforms_1870 1/.test(joined)&&/not event_counter military_reforms_1890 1/.test(joined))return new Set([1]);if(/not event_counter military_reforms_1870 1/.test(joined))return new Set([0]);return new Set([0,1,2]);}
function year(def){const ys=[...(def.label||'').matchAll(/\b(18\d{2}|19\d{2})\b/g)].map(x=>+x[1]).filter(x=>x>=1850&&x<=1905);return ys.length?round5(ys[ys.length-1]):null;}
function quality(def){const tok=def.attributes.split(',').map(x=>x.trim());if(tok.includes('free_upkeep_unit'))return'militia';if(def.training==='highly_trained'&&def.morale>=5)return'elite';return'regular';}
function family(def,x){if(/(?:^|,\s*)general_unit(?:\s*,|$)/.test(def.attributes))return'professional_military';if(def.category==='siege')return'cannon';if([...x.families].includes('port')||/marine|marines|sailor|naval/i.test(`${def.type} ${def.label}`))return'port';return'barracks';}
function geography(x,d,fam,n){
  const key=`${x.faction}|${x.unit}`;
  if(geographyOverrides.has(key))return geographyOverrides.get(key);
  if(tibetanCampaignUnits.has(x.unit))return['tibet'];
  if(x.faction==='saxons')return['japan'];
  if(x.faction==='papal_states')return['ethiopia'];
  const geos=x.geos.size?[...x.geos]:fallback[x.faction];
  const home=westernHome[x.faction]||[];
  if(fam==='barracks'&&d.category==='infantry'&&n>=2&&geos.some(g=>home.includes(g))){
    if(europeanCore.has(x.faction))return['europe'];
    return[...new Set([...geos,'europe'])];
  }
  return geos;
}
const tuples={1:[[1,.01,1],[1,.03,1],[1,.06,1],[1,.10,1]],2:[[1,.02,1],[1,.06,1],[2,.12,2],[2,.20,2]],3:[[1,.03,1],[1,.09,1],[2,.18,2],[3,.30,3]],4:[[1,.04,1],[1,.12,1],[3,.24,3],[4,.40,4]],5:[[1,.05,2],[2,.15,2],[3,.30,3],[5,.50,5]]};
const levels={barracks:[['militia_drill_square',0],['militia_barracks',1],['army_barracks',2],['royal_armoury',3]],port:[['port',0],['shipwright',1],['dockyard',2],['naval_drydock',3]],professional_military:[['military_academy',0],['officers_academy',1]],cannon:[['gunsmith',0],['cannon_maker',1],['cannon_foundry',2],['royal_arsenal',3]]};
const additions=new Map(),fmt=n=>Number.isInteger(n)?String(n):String(n).replace(/^0\./,'.');
function row(f,u,a,r,m,parts){return `\trecruit_pool "${u}"  ${fmt(a)}   ${fmt(r)}   ${fmt(m)}  0  requires factions { ${f}, }${parts.length?' and '+parts.join(' and '):''}`;}
function add(key,line){if(!additions.has(key))additions.set(key,[]);additions.get(key).push(line);}

// Refine firearm early/mid/late successor boundaries from the named weapon year.
const windows=new Map();
for(const x of info.values()){const d=edu.get(x.unit),eras=explicitEras(d,x.faction,x.legacyLines);windows.set(`${x.faction}|${x.unit}`,eraWindow(eras));}
const groups=new Map();for(const x of info.values()){const d=edu.get(x.unit);if(!(d.category==='infantry'||(d.category==='cavalry'&&d.klass==='missile'))||d.projectile==='no')continue;const m=x.unit.match(/^(.*)_(early|mid|high)$/);if(!m)continue;const k=`${x.faction}|${m[1]}`;if(!groups.has(k,))groups.set(k,{});groups.get(k)[m[2]]=x;}
for(const g of groups.values()){let mid=g.mid?year(edu.get(g.mid.unit)):null,high=g.high?year(edu.get(g.high.unit)):null;if(mid&&mid<=1862)mid=1870;if(high&&high<=mid)high=1890;if(g.early&&g.mid)windows.set(`${g.early.faction}|${g.early.unit}`,[0,mid||1870]);if(g.mid)windows.set(`${g.mid.faction}|${g.mid.unit}`,[mid||1870,g.high?(high||1890):0]);if(g.high)windows.set(`${g.high.faction}|${g.high.unit}`,[high||1890,0]);}

const reports=[];
for(const f of factions){const units=[...info.values()].filter(x=>x.faction===f);let normal=0,replen=0;
  for(const x of units){const d=edu.get(x.unit),fam=family(d,x),q=quality(d),n=Math.max(1,Math.min(5,+d.cost[6]||1)),geos=geography(x,d,fam,n),win=condition(...windows.get(`${f}|${x.unit}`));
    for(const [lev,i]of levels[fam]){let allowed=true,norm;
      if(fam==='barracks'){const min={militia:0,regular:1,elite:2}[q];allowed=i>=min;norm=tuples[n][i];}
      else if(fam==='port'){norm=tuples[n][i];}
      else if(fam==='professional_military'){norm=i===0?[1,.05,1]:[1,.10,1];}
      else {const min=x.artMin===99?(/maxim|150mm|pompom/i.test(x.unit)?2:/12lb/i.test(x.unit)?0:1):x.artMin;allowed=i>=min;norm=i===0?[1,.02,2]:i===1?[1,.06,2]:i===2?[1,.10,2]:[2,.20,2];}
      if(allowed)for(const g of geos){add(`${fam}/${lev}`,row(f,x.unit,...norm,[`hidden_resource ${g}`,...win]));normal++;}
      add(`${fam}/${lev}`,row(f,x.unit,+(n*.2).toFixed(2),+(n*.02).toFixed(2),.99,win));replen++;
    }
  }reports.push({faction:f,units:units.length,normal,replen});
}
for(const [k,v]of additions)v.unshift(`;remaining factions standardized recruitment ${k}`);
function install(source,wanted){const lines=source.split('\n');let b='';for(let i=0;i<lines.length;i++){let m;if((m=lines[i].match(/^building\s+(\S+)/)))b=m[1];if(!(m=lines[i].match(/^\s{8}(\S+)\s+(?:city|castle)\s+requires\b/)))continue;const k=`${b}/${m[1]}`,rows=wanted.get(k);if(!rows)continue;let c=i;while(c<lines.length&&lines[c].trim()!=='capability')c++;let o=c+1;while(o<lines.length&&lines[o].trim()!=='{')o++;let depth=1,z=o+1;for(;z<lines.length;z++){for(const ch of lines[z]){if(ch==='{')depth++;else if(ch==='}')depth--;}if(!depth)break;}if(depth)throw Error(`Unclosed ${k}`);lines.splice(z,0,...rows);i=z+rows.length;wanted.delete(k);}if(wanted.size)throw Error(`Unresolved: ${[...wanted.keys()]}`);return lines.join('\n');}
text=install(text,additions);if(!text.endsWith('\n'))text+='\n';const tmp=edbPath+'.remaining.tmp';fs.writeFileSync(tmp,text);fs.renameSync(tmp,edbPath);fs.copyFileSync(edbPath,mirror);console.log(JSON.stringify(reports,null,2));
