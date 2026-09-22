const fs=require('fs'),path=require('path'),R=path.resolve(__dirname,'..');
const eduFiles=['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt'];
const militia=/Heimin|Ainu|Byakkotai|Korean|Teppotai Merc/;
const elite=/Yumitai|Seishi|Satsuma|Yamagunitai|Shinsengumi|Kaiso|Denshutai|Goshimpei|Kijutai|Battotai|Kenyotai|Shogitai|Bodyguard|Enomoto|Hijikata|Itagaki|Jules Brunet|Kondo Isami|Matsudaira|Saigo Takamori|Sakamoto Ryoma|Takeda Ayasaburo|Tokugawa Yoshinobu|sho_mod_cav/;
const skirm=/Ainu (?:Teppo|Geberu|Minieru)|Kiheitai|Saga Hoheitai|Jinshotai|Karasugumi|Raijintai|Kijutai|Goshimpei Hohei|Hokuchin Butai|Hoppo Keibitai|Tondenhei/;
const sharp=/Kijutai/;
const lateB=/(?:1880|1890|1900|1905)|Bodyguard IJA/;
const pistol=/Bodyguard|Revolver Kihei|Enomoto|Hijikata|Itagaki|Jules Brunet|Kondo Isami|Matsudaira|Saigo Takamori|Sakamoto Ryoma|Takeda Ayasaburo|Tokugawa Yoshinobu/;
const artilleryCounts={jap_maxim:10,jap_12lb:20,jap_5lb:10,jap_gatling:10,jap_150mm:20,jap_armstrong:20,sho_maxim:10,sho_12lb:20,sho_5lb:10,sho_gatling:10,sho_150mm:20,sho_armstrong:20,'Japan Armstrong':20,'Japan Armstrong Han':20};
const preservedCounts={'korean_archers':64,'Japan Yumitai':48,'Japan Ainu Archers':64};
const melee80=/Korean Pikemen|Japan (?:Kachi|Battotai|Ishin Shishi|Kenyotai|Ronin|Shogitai)/;
const cav24=/Korean Gimagungsu|korean_cav_mercs|(?:^| )Kihei(?: |$)|Ryukihei|Seishi/;
const command4=/Bodyguard|Enomoto|Hijikata|Itagaki|Jules Brunet|Kondo Isami|Matsudaira|Saigo Takamori|Sakamoto Ryoma|Takeda Ayasaburo|Tokugawa Yoshinobu|sho_mod_cav/;
const qbase={militia:{acc:0,cost:-200},regular:{acc:1,cost:0},elite:{acc:2,cost:200}};
const tiers=['c','b','a','s'];
const families={arquebus:['arquebus_bullet',160,900],musket:['musket_bullet',200,1000],rifled:['rifled_musket_bullet',220,1200],rifle:['rifle_bullet',240,1500],magazine:['magazine_rifle_bullet',260,1800],rifledCarbine:['rifled_musket_carbine_bullet',220,1200],rifleCarbine:['rifle_carbine_bullet',240,1500],magazineCarbine:['magazine_rifle_carbine_bullet',260,1800],musketCarbine:['musket_carbine_bullet',200,1000]};
const earlyBreech=/Korean Byeolgigun|Satsuma Hoheitai|Hokokutai|Yamagunitai|Saga Hoheitai|Jinshotai|Nagaoka Hoheitai|Shohotai|Gakuheitai|Raijintai|Shinsengumi|Shizoku|Suzakutai 1870|Kaiso Shinsengumi|Shinsenryodan|Rikuguntai 1870|Rikusentai 1870|Goshimpei Hohei|Denshutai Kihei|Goshimpei Kihei 1870|Ryukihei 1870|Ryukihei Shogun 1870/;
function spec(t){
  if(pistol.test(t))return null;
  if(t==='Japan Denshutai Kihei'||/Goshimpei Kihei 1870|Ryukihei 1870|Ryukihei Shogun 1870/.test(t))return ['rifledCarbine','breech'];
  if(/Goshimpei Kihei 1880/.test(t))return ['rifleCarbine','breech'];
  if(/Goshimpei Kihei (?:1890|1900|1905)/.test(t))return ['magazineCarbine','magazine'];
  if(/Ryukihei 1880/.test(t))return ['rifleCarbine','breech'];
  if(/Ryukihei (?:1890|1900|1905)/.test(t))return ['magazineCarbine','magazine'];
  if(t==='korean_cav_mercs')return ['musketCarbine','muzzle'];
  if(/Ainu Teppo|Heimin Partisans$/.test(t))return ['arquebus','muzzle'];
  if(/Teppotai|Sampeitai|Byakkotai|Ainu (?:Geberu|Minieru)|Heimin Partisans (?:Geberu|Minieru)|Korean Musketeers/.test(t))return ['musket','muzzle'];
  if(/Shotai|Kiheitai|Karasugumi|Kijutai|Kaga Hoheitai|Matsushiro Hoheitai|Keishitai|Suzakutai$|Yukantai|korean_rifles_mercs/.test(t))return ['rifled','muzzle'];
  if(earlyBreech.test(t))return ['rifled','breech'];
  if(/Denshutai(?: 1870)?$|Kaiso Shinsengumi|Shinsenryodan|Goshimpei 1870|Ezo Rikuguntai 1890|(?:Hoppo Keibitai|Tondenhei) 1870|(?:Rikuguntai|Rikusentai|Ezo Rikuguntai|Goshimpei|Hoppo Keibitai|Tondenhei) 1880/.test(t))return ['rifle','breech'];
  if(/(?:Rikuguntai|Rikusentai|Goshimpei|Hokuchin Butai) (?:1890|1900|1905)|Ezo Rikuguntai (?:1900|1905)/.test(t))return ['magazine','magazine'];
  return null;
}
function setAttrs(b,action){let a=(b.match(/^attributes\s+(.+)$/m)?.[1]||'').split(',').map(x=>x.trim()).filter(Boolean).filter(x=>x!=='gunpowder_unit');if(action==='muzzle')a.push('gunpowder_unit');return b.replace(/^attributes\s+.*$/m,'attributes       '+a.join(', '));}
for(const rel of eduFiles){const p=path.join(R,rel);let s=fs.readFileSync(p,'utf8').replace(/\r/g,'');s=s.split(/(?=^type\s+)/m).map(b=>{const t=b.match(/^type\s+(.+)$/m)?.[1]?.trim();if(!t||!/(?:^ownership|^era [012]).*\bsaxons\b/m.test(b))return b;
  let count=null;if(t in artilleryCounts)count=artilleryCounts[t];else if(t in preservedCounts)count=preservedCounts[t];else if(t==='Japan Heimin Mob')count=96;else if(/Koheitai/.test(t))count=16;else if(command4.test(t))count=4;else if(cav24.test(t)||/^category\s+cavalry/m.test(b))count=24;else if(melee80.test(t))count=80;else if(skirm.test(t))count=30;else if(/^category\s+infantry/m.test(b)&&/^stat_pri\s+.*bullet/m.test(b))count=40;if(count!==null)b=b.replace(/^soldier\s+([^,]+),\s*\d+/m,`soldier          $1, ${count}`);
  if(pistol.test(t)&&/^stat_pri\s+.*bullet/m.test(b)){b=b.replace(/^stat_pri\s+.*$/m,'stat_pri         20, 2, magazine_rifle_bullet_c, 60, 15, missile, missile_gunpowder, piercing, none, musket_shot_set, 25, 1');return setAttrs(b,'breech')}
  const sp=spec(t);if(!sp)return b;const [key,action]=sp,F=families[key],isCav=/^category\s+cavalry/m.test(b),isSk=skirm.test(t),isSharp=sharp.test(t),q=militia.test(t)?'militia':elite.test(t)?'elite':'regular',Q=qbase[q],tierPenalty=lateB.test(t)?0:-1,conversionPenalty=earlyBreech.test(t)?-1:0;let ai=Q.acc+tierPenalty+(isSharp?2:isSk?1:0)-(isCav?1:0)+conversionPenalty;ai=Math.max(0,Math.min(3,ai));const range=F[1]+(isSk?40:0)-(isCav?20:0);b=b.replace(/^stat_pri\s+([^,]+),\s*([^,]+),\s*[^,]+,\s*\d+/m,`stat_pri         $1, $2, ${F[0]}_${tiers[ai]}, ${range}`);b=setAttrs(b,action);if(!isCav)b=b.replace(/^formation\s+.*$/m,isSk?'formation        1.4, 1.8, 2.8, 3.6, 3, square':action==='magazine'?'formation        1.2, 1.4, 2.4, 2.8, 3, square':action==='breech'?'formation        1.2, 1.2, 2.0, 2.4, 3, square':'formation        1.2, 1.2, 1.2, 1.2, 3, square');let total=F[2]+Q.cost+(isSharp?200:0)+(isCav?200:0);b=b.replace(/^stat_cost\s+(.+)$/m,(z,row)=>{const a=row.split(',').map(x=>x.trim());a[1]=a[5]=String(total);a[2]=a[7]=String(Math.round(total/3));a[3]=a[4]='100';return 'stat_cost        '+a.join(', ')});return b}).join('');fs.writeFileSync(p,s.replace(/\n/g,'\r\n'))}

const dbp=path.join(R,'data/unit_models/battle_models.modeldb');let db=fs.readFileSync(dbp,'utf8').replace(/\r/g,'');
function starts(){return [...db.matchAll(/^(\d+) ([^\n]+)\s*\n1 \d+\s*\n\d+ unit_models\//gm)].filter(m=>Number(m[1])===m[2].trim().length)}
function block(name){const a=starts(),i=a.findIndex(m=>m[2].trim()===name);if(i<0)throw Error('Missing model '+name);return {start:a[i].index,end:a[i+1]?.index??db.length,text:db.slice(a[i].index,a[i+1]?.index??db.length)}}
function setAnim(name,anim,tail=''){const q=block(name);if(!/^\d+ MTW2_[^\n]+$/m.test(q.text))throw Error('Missing primary animation '+name);const txt=q.text.replace(/^\d+ MTW2_[^\n]+$/m,`${anim.length} ${anim}${tail}`);db=db.slice(0,q.start)+txt+db.slice(q.end)}
const desired=new Map();for(const rel of [eduFiles[0]]){const s=fs.readFileSync(path.join(R,rel),'utf8').replace(/\r/g,'');for(const b of s.split(/(?=^type\s+)/m)){if(!/(?:^ownership|^era [012]).*\bsaxons\b/m.test(b))continue;const t=b.match(/^type\s+(.+)$/m)?.[1]?.trim(),m=b.match(/^soldier\s+([^,]+)/m)?.[1]?.trim();if(!t||!m||pistol.test(t)||/^category\s+cavalry/m.test(b))continue;const sp=spec(t);if(!sp)continue;const anim=sp[1]==='muzzle'?'MTW2_Fast_Arquebus_3':skirm.test(t)?'MTW2_Musket_SSK':sp[1]==='magazine'?'MTW2_Fast_Arquebus_3':'MTW2_Musket_SS';if(desired.has(m)&&desired.get(m)!==anim)throw Error(`Animation conflict ${m}: ${desired.get(m)} vs ${anim}`);desired.set(m,anim)}}
for(const [m,a] of desired)setAnim(m,a);if(desired.has('korean_rifles'))setAnim('korean_rifles',desired.get('korean_rifles'),' 9 MTW2_Pike');fs.writeFileSync(dbp,db.replace(/\n/g,'\r\n'));
console.log(`Finalized Japanese weapon/model audit: ${desired.size} infantry model animations aligned; meshes unchanged.`);
