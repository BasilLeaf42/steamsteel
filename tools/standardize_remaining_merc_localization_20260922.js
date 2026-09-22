const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const p=path.join(root,'data/text/export_units.txt');
const backup=path.join(root,'tools/backup_before_remaining_subfactions_20260922/export_units.txt');
if(!fs.existsSync(backup)) throw new Error('Subfaction localization backup missing');
function readLoc(file){const b=fs.readFileSync(file);return b[0]===255&&b[1]===254?b.toString('utf16le').replace(/^\uFEFF/,''):b.toString('utf8').replace(/^\uFEFF/,'');}
let text=readLoc(p), old=readLoc(backup);
const beforeDescriptions=[...text.matchAll(/^\{([^}]+_descr)\}.*$/gm)].map(m=>m[0]);
const esc=x=>x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
function get(src,key){const m=src.match(new RegExp('^\\{'+esc(key)+'\\}([^\\r\\n]*)','m'));return m&&m[1];}
function put(key,value){const re=new RegExp('^\\{'+esc(key)+'\\}[^\\r\\n]*','m'),line='{'+key+'}'+value;if(!re.test(text))throw new Error('Missing localization key '+key);text=text.replace(re,()=>line);}

const subfactionKeys=[
 'merc_aceh_marines','merc_aceh_noble','merc_aceh_reg','merc_aceh_gold','merc_aceh_warband','merc_aceh_inf',
 'merc_tib_temple_guard','taipingguners','taiping_inf','taiping_light','taiping_w','tib_temple_guard',
 'merc_tib_noble_cav','tib_militia','merc_tib_inf','tib_horse_archer','tib_roy_inf','tib_tribal_archer','tib_heavy_spear','mercs_tib_monks',
 'korean_archers','Korean_Byeolgigun','Korean_Gimagungsu','Korean_Musketeers','Korean_Pikemen','korean_rifles_mercs','korean_cav_mercs'
];
for(const key of subfactionKeys){
 const original=get(old,key); if(original===null)throw new Error('Missing original name '+key);
 const current=get(text,key)||original;
 put(key,original);
 const equipment=(current.match(/\((.*)\)\s*$/)||[])[1];
 if(equipment) put(key+'_descr_short',`${original} (${equipment})`);
}

// Japanese display names are protected; restore them exactly and retain their established role-first short descriptions.
const japan=['Japan_Ainu_Archers','Japan_Ainu_Geberu','Japan_Ainu_Minieru','Japan_Ainu_Teppo','Japan_Heimin_Mob','Japan_Heimin_Partisans','Japan_Heimin_Partisans_Geberu','Japan_Heimin_Partisans_Minieru','Japan_Ronin','Japan_Teppotai_Merc'];
for(const key of japan){const original=get(old,key);if(original===null)throw new Error('Missing original Japanese name '+key);put(key,original);}

const names={
 merc_us_farmer_cav:['Settler Cavalry','Settler Cavalry (Burnside Carbine)'],merc_ap_front_cav:['Indian Scout Cavalry','Indian Scout Cavalry (Spencer M1860 Carbine)'],
 merc_apache_inf:['Apache Mercenaries','Apache Mercenaries (M1819 Hall Rifle)'],merc_uru_inf:['Uruguayan Infantry','Uruguayan Infantry (Pattern 1853 Enfield Rifle-Musket)'],
 merc_para_foot:['Paraguayan Infantry','Paraguayan Infantry (Brown Bess Percussion Musket)'],merc_us_farmers:['Filibusters','Filibusters (Lorenz Model 1854 Rifle-Musket)'],
 merc_port_inf_early:['Fuzileiros Portugueses (Early)','Fuzileiros Portugueses (Espingarda Enfield 14 mm m/1859)'],merc_port_inf_mid:['Fuzileiros Portugueses (Mid)','Fuzileiros Portugueses (Espingarda Snider 14 mm m/1872)'],
 merc_port_inf_high:['Fuzileiros Portugueses (Late)','Fuzileiros Portugueses (Espingarda de Infantaria Kropatschek 8 mm m/1886)'],merc_port_cav_early:['Carabineiros Portugueses (Early)','Carabineiros Portugueses (Westley-Richards 11 mm m/1867 Carbine, Sabre)'],
 merc_port_cav_mid:['Carabineiros Portugueses (Mid)','Carabineiros Portugueses (Snider m/1873 Carbine, Sabre)'],merc_port_cav_high:['Carabineiros Portugueses (Late)','Carabineiros Portugueses (Kropatschek 8 mm m/1886 Carbine, Sabre)'],
 merc_port_inf_compat:['Fuzileiros Portugueses','Fuzileiros Portugueses (Espingarda Enfield 14 mm m/1859)'],merc_port_cav_compat:['Carabineiros Portugueses','Carabineiros Portugueses (Westley-Richards 11 mm m/1867 Carbine, Sabre)'],
 merc_bhutan_warrior:['Bhutanese Warriors','Bhutanese Warriors (Sword and Shield)'],merc_papa_bows:['Melanesian Scouts','Melanesian Scouts (Composite Bow)'],
 merc_burmese_inf:['Burmese Irregulars','Burmese Irregulars (Pattern 1853 Enfield Rifle-Musket)'],merc_indian_fanatic:['Akali Warriors','Akali Warriors (Javelins, Sword and Shield)'],
 merc_maori_spearmen:['Maori Warriors','Maori Warriors (Spears and Shields)'],merc_maori_musketeers:['Maori Musketeers','Maori Musketeers (Brown Bess Percussion Musket)'],
 merc_arab_sailors:['Khedival Infantry','Khedival Infantry (No. 1 Remington .43 Egyptian Rifle)'],merc_fra_blacks:['Askari','Askari (Remington M1868 Rifle)'],
 merc_eng_for_cav:['Khedival Cavalry','Khedival Cavalry (Martini-Henry Carbine, Sabre)'],merc_fra_for_cav:['Spahis','Spahis (Carabine modèle 1866 Chassepot, Sabre)'],
 merc_mongol_bows:['Mongol Bowmen','Mongol Bowmen (Composite Bow)'],merc_pol_hussars:['Polish Hussars','Polish Hussars (Percussion Carbine, Sabre)'],
 merc_polish_inf:['Polish Infantry','Polish Infantry (Dreyse M/41 Needle Gun)'],merc_georgian_inf:['Georgian Mercenaries','Georgian Mercenaries (M1844 Percussion Musket, Sword)'],
 merc_serb_inf:['Serbian Infantry','Serbian Infantry (M1854 Percussion Rifle-Musket)'],merc_bulgarian_inf:['Bulgarian Infantry','Bulgarian Infantry (Lorenz Model 1854 Rifle-Musket)'],
 merc_kok_royal_cav:['Tartar Cavalry','Tartar Cavalry (Lance and Sabre)'],merc_kashgar_inf:['Kashgar Musketeers','Kashgar Musketeers (M1844 Percussion Musket)'],
 merc_rus_georgian_cav:['Caucasian Cavalry','Caucasian Cavalry (Lance and Sabre)'],merc_zulu_spearmen:['Xhosa Impi','Xhosa Impi (Spear and Shield)'],
 merc_sikh_warriors:['Ex-Company Sikh Sepoys','Ex-Company Sikh Sepoys (Martini-Henry Rifle, Sword and Shield)'],merc_fra_inf_ch:['Chilean Infantry','Chilean Infantry (M1842T Minié Rifle-Musket)'],
 merc_arab_brigade:['Bedouin Irregulars','Bedouin Irregulars (Trade Musket and Sword)'],merc_balk_cav_ch:['Chilean Hussars','Chilean Hussars (Sabre)'],
 merc_siam_agent:['Mercenary Siamese Arquebusiers','Mercenary Siamese Arquebusiers (Matchlock Arquebus)'],merc_uk_sailor:['Merchant Marine','Merchant Marine (Snider-Enfield Rifle)']
};
for(const [key,[name,short]] of Object.entries(names)){put(key,name);put(key+'_descr_short',short);}
put('merc_viet_early_inf_descr_short','Fanno (Javelins and Mace)');
put('merc_zulu_rifles','Tribal Auxiliaries');put('merc_zulu_rifles_descr_short','Tribal Auxiliaries (Martini-Henry Rifles)');

const afterDescriptions=[...text.matchAll(/^\{([^}]+_descr)\}.*$/gm)].map(m=>m[0]);
if(beforeDescriptions.join('\n')!==afterDescriptions.join('\n'))throw new Error('A full description changed');
fs.writeFileSync(p,text);
console.log(`Updated remaining mercenary short descriptions and restored ${subfactionKeys.length+japan.length} protected subfaction names; full descriptions unchanged.`);
