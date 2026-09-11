const fs=require('fs'),path=require('path');
const p=path.resolve(__dirname,'../data/text/export_units.txt');
const buf=fs.readFileSync(p),bom=buf[0]===255&&buf[1]===254,head=bom?2:0;
let text=buf.slice(head).toString('utf16le');
for(const [type,name] of [['ita_milizia_early','Guardia Nazionale Mobile'],['ita_milizia_mid','Milizia Mobile'],['ita_milizia_high','Milizia Mobile']]){
 text=text.replace(new RegExp(`^\\{${type}\\}.*$`,'m'),`{${type}}${name} (${type.endsWith('early')?'Early':type.endsWith('mid')?'Mid':'Late'})`);
 text=text.replace(new RegExp(`^\\{${type}_descr\\}.*$`,'m'),`{${type}_descr}${name} serve in the Italian forces with the equipment and battlefield role appropriate to this period.`);
 text=text.replace(new RegExp(`^\\{${type}_descr_short\\}`,'m'),`{${type}_descr_short}`);
}
fs.writeFileSync(p,Buffer.concat([Buffer.from([255,254]),Buffer.from(text,'utf16le')]));
console.log('Italian militia display names corrected.');
