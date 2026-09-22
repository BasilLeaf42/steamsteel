from pathlib import Path
import shutil

R=Path(__file__).resolve().parents[1]; D=R/'data'; T=D/'text/export_units.txt'
raw=T.read_bytes(); enc='utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8'
text=raw.decode(enc)
names={
'qing_green_banner_spears':('Green Banner Spearmen','Militia spearmen'),
'qing_green_banner_gunmen':('Green Banner Gunmen','Militia matchlock infantry'),
'qing_green_banner_archers':('Green Banner Archers','Militia archers'),
'qing_green_banner_regulars':('Green Banner Regulars','Militia infantry, Pattern 1853 Enfield rifle-musket'),
'qing_new_army':('New Army Infantry','Regular infantry, Hanyang 88 magazine rifle'),
'qing_green_banner_late':('Green Banner Infantry','Militia infantry, Mauser Model 1871 rifle'),
'qing_xiang_huai_early':('Xiang/Huai Infantry','Regular infantry, Pattern 1853 Enfield rifle-musket'),
'qing_xiang_huai_mid':('Xiang/Huai Infantry','Regular infantry, Dreyse M1868 needle rifle'),
'qing_beiyang_infantry':('Beiyang Infantry','Regular infantry, Hanyang 88 magazine rifle'),
'qing_baqi_gunmen':('Baqi Gunmen','Jingal skirmishers'),
'qing_green_banner_horse':('Green Banner Horse Squadron','Militia lancers'),
'qing_eight_banner_cavalry':('Eight Banner Cavalry','Banner horse archers'),
'qing_village_braves':('Village Braves','Militia infantry with hand weapons'),
}
add=[]
for k,(n,s) in names.items():
 if '{'+k+'}' not in text:
  add += [f'{{{k}}}{n}',f'{{{k}_descr}}{n}.',f'{{{k}_descr_short}}{s}','']
if add: text=text.rstrip()+"\r\n"+"\r\n".join(add)+"\r\n"
T.write_bytes(text.encode(enc))
cards=D/'ui/units/byzantium'
aliases={'qing_green_banner_late':'qing_inf','qing_xiang_huai_mid':'qing_gunners','qing_green_banner_horse':'oirat_cav','qing_village_braves':'qing_swords'}
for new,old in aliases.items():
 src=cards/f'#{old}.tga'; dst=cards/f'#{new}.tga'
 if src.exists(): shutil.copy2(src,dst)
 else: raise FileNotFoundError(src)
print('Finished Qing localization and card aliases.')
