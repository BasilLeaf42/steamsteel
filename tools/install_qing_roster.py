from pathlib import Path
import re, shutil

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
SOE=ROOT.parent/'soe'/'data'; EDU=DATA/'tow_steamsteel/export_descr_unit.txt'

def blocks(text): return re.split(r'(?=^type\s+)',text,flags=re.M)
def typ(b):
 m=re.match(r'type\s+(.+?)\s*$',b,re.M); return m.group(1).strip() if m else None
def setline(b,key,val):
 p=rf'^{re.escape(key)}\s+.*$'
 return re.sub(p,f'{key:<17}{val}',b,count=1,flags=re.M) if re.search(p,b,re.M) else b
def eras(b,vals):
 b=re.sub(r'^era [012]\s+.*\n?','',b,flags=re.M)
 own=re.search(r'^ownership.*$',b,re.M)
 ins=''.join(f'era {e}            byzantium\n' for e in vals)
 return b[:own.end()]+'\n'+ins.rstrip()+b[own.end():]
def own(b): return setline(b,'ownership','byzantium, slave')
def rename_block(b,new_type,key,label,soldier,era):
 b=setline(b,'type',new_type); b=setline(b,'dictionary',f'{key} ; {label}'); b=setline(b,'soldier',soldier)
 return eras(own(b),era)

text=EDU.read_text(encoding='utf-8').replace('\r\n','\n'); bs=blocks(text); by={typ(b):b for b in bs if typ(b)}
spec={
'qing_pike':('qing_green_banner_spears','qing_green_banner_spears','Green Banner Spearmen','lvying_spear, 80, 0, 1.2',[0]),
'qing_vets':('qing_green_banner_gunmen','qing_green_banner_gunmen','Green Banner Gunmen (Matchlock)','janissary_musketeers, 40, 0, 1',[0]),
'qing_archers':('qing_green_banner_archers','qing_green_banner_archers','Green Banner Archers','lvying_archer, 80, 0, 1.2',[0]),
'qing_inf_upg':('qing_green_banner_regulars','qing_green_banner_regulars','Green Banner Regulars (Minié Rifle-Musket)','yongying_gunners, 40, 0, 1.2',[1]),
'qing_inf':('qing_new_army','qing_new_army','New Army Infantry (Hanyang 88)','baqilianjun, 40, 0, 1.2',[2]),
'qing_gunners':('qing_xiang_huai_mid','qing_xiang_huai_mid','Xiang/Huai Infantry (Dreyse M1868)','qing_gunners, 40, 0, 1',[1]),
'qing_ww1_inf':('qing_baqi_gunmen','qing_baqi_gunmen','Baqi Gunmen (Jingal)','huaijunnavy, 30, 0, 1.2',[0,1,2]),
'qing_swords':('qing_village_braves','qing_village_braves','Village Braves','qing_swords, 80, 0, 1',[0,1,2]),
'oirat_cav':('qing_green_banner_horse','qing_green_banner_horse','Green Banner Horse Squadron','oirat_cav, 24, 0, 1',[0,1,2]),
}
out=[]; done=set()
for b in bs:
 t=typ(b)
 if t in spec:
  out.append(rename_block(b,*spec[t])); done.add(t)
 elif t in {'Qing Tiger Warriors','mongol_bows','mongols_archer','mongol_inf','qing_carbs'}:
  out.append(eras(setline(b,'ownership','slave'),[]))
 else: out.append(b)
assert done==set(spec)
base=by['qing_inf_upg']
extras=[
 rename_block(base,'qing_xiang_huai_early','qing_xiang_huai_early','Xiang/Huai Infantry (Pattern 1853 Enfield)','yongying_gunners, 40, 0, 1.2',[0]),
 rename_block(by['qing_inf'],'qing_green_banner_late','qing_green_banner_late','Green Banner Infantry (Mauser Model 1871)','baqilianjun, 40, 0, 1.2',[2]),
 rename_block(by['qing_inf'],'qing_beiyang_infantry','qing_beiyang_infantry','Beiyang Infantry (Hanyang 88)','huaijunnavy, 40, 0, 1.2',[2]),
 rename_block(by['oirat_royal'],'qing_eight_banner_cavalry','qing_eight_banner_cavalry','Eight Banner Cavalry','MongolbaqiArchers, 24, 0, 1',[0,1,2]),
]
insert='\n'.join(extras)+'\n'
joined=''.join(out); marker=';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n;################ Empire of Japan'
joined=joined.replace(marker,insert+'\n'+marker)
# Apply D-tier morale and post-rule -100 cost to the national roster.
names={v[0] for v in spec.values()}|{'qing_xiang_huai_early','qing_green_banner_late','qing_beiyang_infantry','qing_eight_banner_cavalry'}
regular={'qing_xiang_huai_early','qing_xiang_huai_mid','qing_beiyang_infantry','qing_new_army'}
parts=blocks(joined)
for i,b in enumerate(parts):
 t=typ(b)
 if t not in names: continue
 morale=4 if t in regular else 2
 b=re.sub(r'^stat_mental\s+\d+,\s*\w+,\s*\w+',f'stat_mental      {morale}, normal, trained' if t in regular else f'stat_mental      {morale}, low, trained',b,flags=re.M)
 m=re.search(r'^stat_cost\s+(.+)$',b,re.M)
 if m:
  a=[int(x.strip()) for x in m.group(1).split(',')]; a[1]=max(0,a[1]-100); a[5]=max(0,a[5]-100); a[2]=a[1]//3; a[7]=a[5]//3; a[3]=a[4]=100
  b=b[:m.start()]+f"stat_cost        {', '.join(map(str,a))}"+b[m.end():]
 parts[i]=b
joined=''.join(parts).replace('\n','\r\n')
EDU.write_text(joined,encoding='utf-8',newline=''); (DATA/'export_descr_unit.txt').write_text(joined,encoding='utf-8',newline='')

# Merge exact SOE donor model records and their loose assets.
src=(SOE/'unit_models/battle_models.modeldb').read_text(encoding='utf-8').replace('\r\n','\n'); dst=(DATA/'unit_models/battle_models.modeldb').read_text(encoding='utf-8').replace('\r\n','\n')
donors=['lvying_spear','lvying_archer','janissary_musketeers','yongying_gunners','huaijunnavy','baqilianjun','MongolbaqiArchers']
def entry(s,n):
 m=re.search(rf'(?m)^{len(n)} {re.escape(n)}\s*$',s); assert m,n
 e=re.search(r'(?m)^16 -0\.090000004 0 0 -0\.34999999 0\.80000001 0\.60000002\s*$',s[m.start():]); assert e,n
 return s[m.start():m.start()+e.end()].rstrip()+'\n'
add=[]
for n in donors:
 if not re.search(rf'(?m)^{len(n)} {re.escape(n)}\s*$',dst): add.append(entry(src,n))
if add:
 first,rest=dst.split('\n',1); mm=re.match(r'^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0\s*)$',first); assert mm
 first=mm.group(1)+str(int(mm.group(2))+len(add))+mm.group(3); dst=first+'\n'+rest.rstrip()+'\n'+''.join(add)
(DATA/'unit_models/battle_models.modeldb').write_text(dst.replace('\n','\r\n'),encoding='utf-8',newline='')
for d in ['Huai','huai','baqi','Xiang','xiang','lvying','mongols']:
 s=SOE/'unit_models/_Units'/d
 if s.exists(): shutil.copytree(s,DATA/'unit_models/_Units'/d,dirs_exist_ok=True)
for d in ['AttachmentSets']:
 s=SOE/'unit_models'/d
 if s.exists(): shutil.copytree(s,DATA/'unit_models'/d,dirs_exist_ok=True)
if (SOE/'unit_sprites').exists(): shutil.copytree(SOE/'unit_sprites',DATA/'unit_sprites',dirs_exist_ok=True)

# Install preserved SOE tactical donors under each new internal name.
cards=DATA/'ui/units/byzantium'; cards.mkdir(parents=True,exist_ok=True)
sources={'qing_green_banner_spears':'lvying_spear','qing_green_banner_gunmen':'Janissary_Musketeers','qing_green_banner_archers':'lvying_archer','qing_green_banner_regulars':'yongying_gunners','qing_new_army':'baqilianjun','qing_baqi_gunmen':'huaijunnavy','qing_xiang_huai_early':'yongying_gunners','qing_beiyang_infantry':'huaijunnavy','qing_eight_banner_cavalry':'MongolbaqiArchers'}
for n,s in sources.items():
 choices=list((SOE/'ui/units').glob(f'*/#{s}.tga')); assert choices,s; shutil.copy2(choices[0],cards/f'#{n}.tga')
print('Installed Qing roster, SOE donors, mirrored EDU, and tactical donor cards.')
