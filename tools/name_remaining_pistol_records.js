const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const names={
  us_front_inf:'Union State Militia (Colt Army Model 1860 revolver and sabre)',
  mx_pistoleer:'Mexican Hussars (Revolver Lefaucheux Modelo 1858 and sabre)',
  l_pith_cav_aztecs:'Argentine Cavalry (Remington Model 1875 revolver and sabre)',
  fra_hus_2_aztecs:'Argentine General and Staff (Lefaucheux M1854 revolver and sabre)',
  rus_cos_hussar:'Tartar Auxiliaries (Smith & Wesson No. 3 Russian Model revolver and sabre)',
  rus_imp_cav:'General i Shtab (Smith & Wesson No. 3 Russian Model revolver and sabre)',
  aus_ulhans:'General und Stab (Gasser-Revolver M1870 und Saebel)',
  balk_cav:'Husaren (Gasser-Revolver M1870 und Saebel)',
  otto_cav_golden:'al-Khayyala al-Sultaniyya (Beaumont-Adams revolver and sabre)',
  omani_cav:'al-Khayyala al-Sultaniyya (Beaumont-Adams revolver and sabre)',
  rus_sib_cossacks:'Gholaman-e Shah (Colt Model 1851 Navy revolver and shamshir)',
  Japan_Saigo_Takamori_1860:'Saigo Takamori (Lefaucheux Mle.1858 revolver and katana)'
};
function change(text){
  let s=text.replace(/\r\n/g,'\n');
  for(const [key,name] of Object.entries(names))s=s.replace(new RegExp(`^dictionary\\s+${key}.*$`,'m'),`dictionary       ${key} ; ${name}`);
  const starts=[...s.matchAll(/^type\s+(\S+)/gm)],i=starts.findIndex(x=>x[1]==='qing_carbs');
  if(i>=0){const end=i+1<starts.length?starts[i+1].index:s.length,old=s.slice(starts[i].index,end);let b=old;
    b=b.replace(/^class\s+\S+$/m,'class            missile')
      .replace(/^stat_pri\s+.*$/m,'stat_pri         13, 2, magazine_rifle_carbine_bullet_c, 240, 40, missile, missile_gunpowder, piercing, none, smokeless_shot_set, 25, 1')
      .replace(/^attributes\s+.*$/m,'attributes       free_upkeep_unit, sea_faring, hide_forest, can_withdraw, guncavalry, gunmen, start_not_skirmishing, cannot_skirmish, stakes')
      .replace(/^formation\s+.*$/m,'formation        2, 2, 4, 4, 3, square')
      .replace(/^stat_fire_delay\s+.*$/m,'stat_fire_delay  0')
      .replace(/^stat_ground\s+.*$/m,'stat_ground      0, 0, 0, 0');
    s=s.slice(0,starts[i].index)+b+s.slice(end);
  }
  return s.replace(/\n/g,'\r\n');
}
const c=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),r=path.join(root,'data/export_descr_unit.txt'),edu=change(fs.readFileSync(c,'utf8'));
fs.writeFileSync(c,edu);fs.writeFileSync(r,edu);

const lp=path.join(root,'data/text/export_units.txt'),raw=fs.readFileSync(lp);let loc=raw.slice(raw[0]===255&&raw[1]===254?2:0).toString('utf16le').replace(/\r\n/g,'\n');
for(const [key,name] of Object.entries(names))loc=loc.replace(new RegExp(`^\\{${key}_descr_short\\}.*$`,'m'),`{${key}_descr_short}${name}`);
loc=loc.replace(/^\{qing_carbs_descr_short\}.*$/m,'{qing_carbs_descr_short}Beiyang Dragoons (Hanyang 88 cavalry carbine)');
fs.writeFileSync(lp,Buffer.concat([Buffer.from([255,254]),Buffer.from(loc.replace(/\n/g,'\r\n'),'utf16le')]));
console.log('Named every remaining fixed pistol record and corrected Beiyang Dragoons to a true carbine profile.');
