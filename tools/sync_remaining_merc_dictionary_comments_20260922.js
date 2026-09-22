const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),cp=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),rp=path.join(root,'data/export_descr_unit.txt'),lp=path.join(root,'data/text/export_units.txt');
let edu=fs.readFileSync(cp,'utf8'),loc=fs.readFileSync(lp,'utf8');
const types=['merc_us_farmer_cav','merc_ap_front_cav','merc_apache_inf','merc_uru_inf','merc_para_foot','merc_us_farmers','merc_port_inf_early','merc_port_inf_mid','merc_port_inf_high','merc_port_cav_early','merc_port_cav_mid','merc_port_cav_high','merc_port_inf','merc_port_lancer','merc_bhutan_warrior','merc_papa_bows','merc_burmese_inf','merc_indian_fanatic','merc_maori_spearmen','merc_maori_musketeers','merc_arab_sailors','merc_fra_blacks','merc_eng_for_cav','merc_fra_for_cav','merc_mongol_bows','merc_pol_hussars','merc_polish_inf','merc_georgian_inf','merc_serb_inf','merc_bulgarian_inf','merc_kok_royal_cav','merc_kashgar_inf','merc_rus_georgian_cav','merc_zulu_spearmen','merc_sikh_warriors','merc_fra_inf_ch','merc_arab_brigade','merc_balk_cav_ch','merc_siam_agent','merc_uk_sailor'];
for(const type of types){
 const re=new RegExp('(^type\\s+'+type+'\\s*$[\\s\\S]*?^dictionary\\s+(\\S+)\\s*;)[^\\r\\n]*','m');
 const m=edu.match(re);if(!m)throw new Error('Missing dictionary line '+type);
 const key=m[2],lm=loc.match(new RegExp('^\\{'+key+'_descr_short\\}([^\\r\\n]*)','m'));
 if(!lm)throw new Error('Missing short localization '+key);
 edu=edu.replace(re,(all,prefix)=>prefix+' '+lm[1]);
}
fs.writeFileSync(cp,edu);fs.writeFileSync(rp,edu);
console.log('Synchronized 40 EDU dictionary comments with their standardized short descriptions.');
