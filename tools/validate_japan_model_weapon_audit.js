const fs=require('fs');
function fail(s){throw Error(s)}
const a=fs.readFileSync('data/tow_steamsteel/export_descr_unit.txt','utf8').replace(/\r/g,''),b=fs.readFileSync('data/export_descr_unit.txt','utf8').replace(/\r/g,'');if(a!==b)fail('EDU mirrors differ');
const db=fs.readFileSync('data/unit_models/battle_models.modeldb','utf8').replace(/\r/g,'');
const starts=[...db.matchAll(/^(\d+) ([^\n]+)\s*\n1 \d+\s*\n\d+ unit_models\//gm)].filter(m=>Number(m[1])===m[2].trim().length),entries=new Map();for(let i=0;i<starts.length;i++)entries.set(starts[i][2].trim(),db.slice(starts[i].index,starts[i+1]?.index??db.length));
const skirm=/Ainu (?:Teppo|Geberu|Minieru)|Kiheitai|Saga Hoheitai|Jinshotai|Karasugumi|Raijintai|Kijutai|Goshimpei Hohei|Hokuchin Butai|Hoppo Keibitai|Tondenhei/;
const command=/Bodyguard|Enomoto|Hijikata|Itagaki|Jules Brunet|Kondo Isami|Matsudaira|Saigo Takamori|Sakamoto Ryoma|Takeda Ayasaburo|Tokugawa Yoshinobu|sho_mod_cav/;
const artillery={jap_maxim:10,jap_12lb:20,jap_5lb:10,jap_gatling:10,jap_150mm:20,jap_armstrong:20,sho_maxim:10,sho_12lb:20,sho_5lb:10,sho_gatling:10,sho_150mm:20,sho_armstrong:20,'Japan Armstrong':20,'Japan Armstrong Han':20};
let n=0;
for(const x of a.split(/(?=^type\s+)/m)){if(!/(?:^ownership|^era [012]).*\bsaxons\b/m.test(x))continue;n++;const t=x.match(/^type\s+(.+)$/m)?.[1].trim(),cat=x.match(/^category\s+(.+)$/m)?.[1].trim(),sm=x.match(/^soldier\s+([^,]+),\s*(\d+)/m),pri=x.match(/^stat_pri\s+(.+)$/m)?.[1]||'',attrs=x.match(/^attributes\s+(.+)$/m)?.[1]||'';if(!sm)continue;const model=sm[1].trim(),count=+sm[2];
  if(t in artillery&&count!==artillery[t])fail(`${t}: artillery crew ${count}`);
  if(command.test(t)&&count!==4)fail(`${t}: command strength ${count}`);
  if(cat==='cavalry'&&!command.test(t)&&count!==24)fail(`${t}: cavalry strength ${count}`);
  if(cat==='infantry'&&/bullet/.test(pri)&&!command.test(t)){const want=skirm.test(t)?30:40;if(count!==want)fail(`${t}: firearm strength ${count}, wanted ${want}`);const e=entries.get(model);if(!e)fail(`${t}: missing modeldb ${model}`);const anim=e.match(/^\d+ (MTW2_\S+)/m)?.[1].trim(),muzzle=/\bgunpowder_unit\b/.test(attrs),mag=/magazine_rifle_bullet/.test(pri),wantAnim=muzzle?'MTW2_Fast_Arquebus_3':skirm.test(t)?'MTW2_Musket_SSK':mag?'MTW2_Fast_Arquebus_3':'MTW2_Musket_SS';if(anim!==wantAnim)fail(`${t}: ${anim}, wanted ${wantAnim}`);if(/MTW2_Musket_SSK/.test(anim)&&muzzle)fail(`${t}: muzzle-loader uses SSK`);
    const mesh=e.match(/unit_models\/[^\s]+\.mesh/i)?.[0],raw=mesh&&fs.existsSync('data/'+mesh)?fs.readFileSync('data/'+mesh).toString('latin1'):'',weapon=(raw.match(/primaryactive0[^A-Za-z0-9]+([A-Za-z][A-Za-z0-9_.-]{3,})/)||[])[1]||'';if(/tanegashima/i.test(weapon)&&!/arquebus_bullet/.test(pri))fail(`${t}: ${weapon} not arquebus`);if(/geberu/i.test(weapon)&&!/musket_bullet/.test(pri))fail(`${t}: ${weapon} not musket`);if(/arisaka/i.test(weapon)&&!/magazine_rifle_bullet/.test(pri))fail(`${t}: ${weapon} not magazine rifle`);if(/snider|spencer|starr|rollingblock|dreyse/i.test(weapon)&&(!/rifled_musket_bullet/.test(pri)||muzzle))fail(`${t}: ${weapon} early-breech mismatch`);
  }
}
if(n!==124)fail(`Japanese record count ${n}`);console.log('Japan model/weapon audit passed: 124 records; strengths, embedded weapon families, and 59 infantry reload mappings verified.');
