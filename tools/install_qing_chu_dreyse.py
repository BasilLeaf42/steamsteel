from pathlib import Path
import re,shutil
R=Path(__file__).resolve().parents[1]; D=R/'data'; M=D/'unit_models/battle_models.modeldb'
src=Path(r'C:\Users\kwoks\AppData\Local\Temp\qing_chu_dreyse\built\qing_chu_dreyse_lod0.mesh')
out=D/'unit_models/_Units/Xiang/qing_chu_dreyse_lod0.mesh'; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,out)
text=M.read_text(encoding='utf-8').replace('\r\n','\n'); name='qing_chu_dreyse'
if not re.search(rf'(?m)^{len(name)} {name}\s*$',text):
 lines=[f'{len(name)} {name}','1 1',f'{len("unit_models/_Units/Xiang/qing_chu_dreyse_lod0.mesh")} unit_models/_Units/Xiang/qing_chu_dreyse_lod0.mesh 20000','2']
 for fac in ('byzantium','slave'):
  lines += [f'{len(fac)} {fac}','50 unit_models/_Units/Xiang/textures/chu_yong.texture','52 unit_models/_Units/Xiang/textures/chu_yong_n.texture','45 unit_sprites/aztecs_Aztec_Warriors_sprite.spr']
 lines += ['2']
 for fac in ('byzantium','slave'):
  lines += [f'{len(fac)} {fac}','57 unit_models/_Units/attachments/textures/chin_head.texture','58 unit_models/_Units/attachments/textures/blank_norm.texture 0']
 lines += ['1','4 None','14 MTW2_Musket_SS 0','1','19 MTW2_Musket_Primary','0','16 -0.090000004 0 0 -0.34999999 0.80000001 0.60000002']
 first,rest=text.split('\n',1); m=re.match(r'^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0\s*)$',first); assert m
 first=m.group(1)+str(int(m.group(2))+1)+m.group(3); text=first+'\n'+rest.rstrip()+'\n'+'\n'.join(lines)+'\n'
M.write_text(text.replace('\n','\r\n'),encoding='utf-8',newline='')
for p in [D/'tow_steamsteel/export_descr_unit.txt',D/'export_descr_unit.txt']:
 t=p.read_text(encoding='utf-8').replace('\r\n','\n'); parts=re.split(r'(?=^type\s+)',t,flags=re.M)
 for i,b in enumerate(parts):
  if re.match(r'^type\s+qing_xiang_huai_mid\s*$',b,re.M):
   b=re.sub(r'^soldier\s+.*$', 'soldier          qing_chu_dreyse, 40, 0, 1',b,flags=re.M)
   b=re.sub(r'^attributes\s+.*$','attributes       free_upkeep_unit, sea_faring, hide_forest, gunmen, start_not_skirmishing, cannot_skirmish',b,flags=re.M)
   b=re.sub(r'^formation\s+.*$','formation        1.2, 1.2, 2.0, 2.4, 3, square',b,flags=re.M)
   parts[i]=b
 p.write_text(''.join(parts).replace('\n','\r\n'),encoding='utf-8',newline='')
print('Installed dedicated Chu-uniform Dreyse infantry mesh and mapping.')
