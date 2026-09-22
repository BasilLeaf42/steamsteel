const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'..');
const eduPaths=['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt'].map(p=>path.join(root,p));
function read(file){const b=fs.readFileSync(file);return {text:(b[0]===255&&b[1]===254?b.toString('utf16le'):b.toString('utf8')).replace(/^\uFEFF/,''),utf16:b[0]===255&&b[1]===254};}
function write(file,s,text){const b=Buffer.from(text,s.utf16?'utf16le':'utf8');fs.writeFileSync(file,s.utf16?Buffer.concat([Buffer.from([255,254]),b]):b);}
const states=eduPaths.map(read);if(states[0].text!==states[1].text)throw Error('EDU mirrors differ before global land pass');
const changes={fireDelay:0,cost:0,terrain:0,strength:0,formation:0,attributes:0,ballistics:0,cursor:0};
let blocks=states[0].text.split(/(?=^type\s+)/m).map(block=>{
 if(!/^type\s+/m.test(block))return block;const type=(block.match(/^type\s+(.+)$/m)||[])[1]?.trim(),cat=(block.match(/^category\s+(\S+)/m)||[])[1];if(cat==='ship'||cat==='siege')return block;
 block=block.replace(/^stat_fire_delay\s+[^\r\n]+/m,m=>{if(/\s0\s*$/.test(m))return m;changes.fireDelay++;return 'stat_fire_delay  0'});
 if(type!=='camel_wagon')block=block.replace(/^stat_ground\s+[^\r\n]+/m,m=>{if(/\s0, 0, 0, 0\s*$/.test(m))return m;changes.terrain++;return 'stat_ground      0, 0, 0, 0'});
 block=block.replace(/^stat_cost\s+([^\r\n]+)/m,(m,row)=>{const x=row.split(',').map(v=>v.trim());if(x.length<8)return m;const total=Number(x[1]);if(!Number.isFinite(total))return m;const third=Math.round(total/3);const next=[x[0],x[1],String(third),'100','100',x[5],x[6],String(third)];if(next.join(', ')===x.join(', '))return m;changes.cost++;return 'stat_cost        '+next.join(', ')});
 const forced={fra_chasseurs_early:30,fra_chasseurs_mid:30,fra_chasseurs_high:30,fra_chass:30,merc_zulu_rifles:30,otto_cav:24,afghan_gen:24,'Qing Tiger Warriors':80,it_royals_mongols:80,it_royals:80,it_royals_hungary:80};
 if(forced[type])block=block.replace(/^soldier\s+([^,]+),\s*\d+/m,(m,s)=>{const old=Number((m.match(/,\s*(\d+)/)||[])[1]);if(old===forced[type])return m;changes.strength++;return `soldier          ${s.trim()}, ${forced[type]}`});
 const count=Number((block.match(/^soldier\s+[^,]+,\s*(\d+)/m)||[])[1]),pri=(block.match(/^stat_pri\s+([^\r\n]+)/m)||[])[1]||'',firearm=/(?:arquebus|harquebus|musket|rifle|wall_gun|long_gun).*_bullet/.test(pri);
 if(cat==='infantry'&&firearm&&count===30)block=block.replace(/^formation\s+[^\r\n]+/m,m=>{const want='formation        1.4, 1.8, 2.8, 3.6, 3, square';if(m===want)return m;changes.formation++;return want});
 if(cat==='infantry'&&firearm&&count!==30&&count>4)block=block.replace(/^formation\s+[^\r\n]+/m,m=>{let body='1.2, 1.2, 1.2, 1.2, 3, square';if(/magazine_rifle_bullet/.test(pri))body='1.2, 1.4, 2.4, 2.8, 3, square';else if(/(?:^|[^a-z])rifle_bullet/.test(pri))body='1.2, 1.2, 2.0, 2.4, 3, square';const want='formation        '+body;if(m.trimEnd()===want)return m;changes.formation++;return want});
 if(cat==='cavalry'&&count>4&&!/^(?:boer_wagon|camel_wagon|indian_ele|siam_ele_gunner|Elephant Artillery)$/.test(type))block=block.replace(/^formation\s+[^\r\n]+/m,m=>{const want='formation        2, 2, 4, 4, 3, square';if(m===want)return m;changes.formation++;return want});
 block=block.replace(/^attributes\s+([^\r\n]+)/m,(m,row)=>{const keepWithdraw=['spa_caz_early','spa_caz_mid','spa_caz_high','cuban_inf_high'].includes(type);let a=row.split(',').map(x=>x.trim()).filter(Boolean).filter(x=>!['hide_improved_forest','hardy','very_hardy','affected_by_rain'].includes(x)&&(x!=='can_withdraw'||keepWithdraw));const eras=[...block.matchAll(/^era\s+([012])\b/gm)].map(x=>Number(x[1])),late=eras.length>0&&eras.every(x=>x===2),engineering=/(?:sapeur|sapper|pionier|engineer|ingenier|michanik|genio)/i.test(type+' '+(block.match(/^dictionary\s+.*$/m)||[''])[0]),carbine=cat==='cavalry'&&/_carbine_bullet/.test(pri),stakes=engineering||(late&&(cat==='infantry'||carbine));a=a.filter(x=>x!=='stakes');if(stakes)a.push('stakes');const next='attributes       '+a.join(', ');if(next===m)return m;changes.attributes++;return next});
 if(firearm&&!/(?:wall_gun|long_gun)_bullet/.test(pri))block=block.replace(/^stat_pri\s+([^\r\n]+)/m,(m,row)=>{const x=row.split(',').map(v=>v.trim());if(x.length<10)return m;const projectile=x[2],pistol=cat==='cavalry'&&Number(x[3])<=60,skirm=cat==='infantry'&&count===30;let range=200;if(/arquebus|harquebus/.test(projectile))range=160;else if(/rifled_musket/.test(projectile))range=220;else if(/magazine_rifle/.test(projectile))range=260;else if(/rifle/.test(projectile))range=240;if(skirm)range+=40;if(cat==='cavalry')range-=20;if(pistol)range=60;x[3]=String(range);x[9]=pistol?'musket_shot_set':/magazine_rifle/.test(projectile)?'smokeless_shot_set':'musket_shot_set';const next='stat_pri         '+x.join(', ');if(next===m)return m;changes.ballistics++;return next});
 if(['spa_caz_early','spa_caz_mid','spa_caz_high','cuban_inf_high'].includes(type))block=block.replace(/^attributes\s+([^\r\n]+)/m,(m,row)=>{let a=row.split(',').map(x=>x.trim()).filter(Boolean).filter(x=>x!=='cannot_skirmish');if(!a.includes('can_withdraw'))a.push('can_withdraw');return 'attributes       '+a.join(', ')});
 if(type==='camel_wagon')block=block.replace(/^stat_ground\s+[^\r\n]+/m,'stat_ground      1, 0, 0, 1');
 if(type==='zulu_elite')block=block.replace(/^formation\s+[^\r\n]+/m,'formation        1.2, 1.2, 2.4, 2.8, 2, square');
 return block;
});
const next=blocks.join('');for(let i=0;i<eduPaths.length;i++)write(eduPaths[i],states[i],next);

const cursorPath=path.join(root,'data/descr_cursor_actions.txt'),cs=read(cursorPath);let cursor=cs.text;
// The executable accepts the documented mixed-case `Na`; uppercase `NA` is parsed as an unknown action.
cursor=cursor.replace(/^(\s*\S+\s+)NA(?=\s|$)/gm,(m,p)=>{changes.cursor++;return p+'Na'});write(cursorPath,cs,cursor);
console.log(JSON.stringify(changes));
