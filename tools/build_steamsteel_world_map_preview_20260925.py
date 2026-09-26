from PIL import Image
from pathlib import Path
import base64, io, json, re

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(r'C:\Users\kwoks\.codex\visualizations\2026\09\12\01a09417-2b02-79c1-ac26-19f8f616b95f\steamsteel-world-map.html')
REGIONS = ROOT / 'data/world/maps/map_steamsteel/descr_regions.txt'
MAP = ROOT / 'data/world/maps/map_steamsteel/map_regions.tga'
LOC = ROOT / 'data/text/text_steamsteel/imperial_campaign_regions_and_settlement_names.txt'
STRAT = ROOT / 'data/world/maps/campaign/camp_steamsteel/descr_strat.txt'

loc_text = LOC.read_bytes()[2:].decode('utf-16le')
loc = {}
for line in loc_text.splitlines():
    m = re.match(r'^\{([^}]+)\}\s*(.*)$', line)
    if m: loc[m.group(1)] = m.group(2).strip()

lines = REGIONS.read_text(encoding='utf-8').splitlines()
regions = []
for i, line in enumerate(lines):
    if re.match(r'^[A-Za-z0-9_]+_Province\s*$', line):
        regions.append({'key': line.strip(), 'settlementKey': lines[i+1].strip(),
                        'creator': lines[i+2].strip(),
                        'rgb': tuple(map(int, lines[i+4].strip().split())),
                        'tags': [x.strip() for x in lines[i+5].split(',') if x.strip()]})

# Starting ownership is defined in descr_strat, not by the faction-creator field above.
strat = STRAT.read_text(encoding='utf-8').splitlines()
owner_by_region = {}
faction = ''
in_settlement = False
pending = False
depth = 0
current_region = None
for line in strat:
    m = re.match(r'^faction\s+([^,\s]+)', line)
    if m and not in_settlement: faction = m.group(1)
    if not in_settlement and line.strip() == 'settlement':
        pending = True; current_region = None; continue
    if pending and line.strip() == '{':
        pending = False; in_settlement = True; depth = 1; continue
    if in_settlement:
        depth += line.count('{') - line.count('}')
        m = re.match(r'^\s*region\s+(\S+)', line)
        if m: current_region = m.group(1)
        if depth == 0:
            if current_region: owner_by_region[current_region] = faction
            in_settlement = False

macro_rules = [
 ('North America', {'usa','csa','canada','mexico','amerindian','cuba'}),
 ('South America', {'s_america','argentina','brazil','peru','uruguay','paraguay'}),
 ('Europe', {'europe','uk','france','prussia','spain','netherlands','denmark','sweden','norway','italy','austria','hungary','greece','russia'}),
 ('North Africa & Middle East', {'north_africa','middle_east','arab','ottoman','morocco','muscat','egypt'}),
 ('Sub-Saharan Africa', {'sub_sahara','south_africa','zululand'}),
 ('South & Central Asia', {'india','persia','afghanistan','steppe','kokand','siberia','tibet'}),
 ('East Asia', {'china','japan','manchuria','mongolia'}),
 ('Southeast Asia & Oceania', {'east_indies','indochina','siam','anzac'}),
]
tag_groups = {
 'Broad geographic': ['europe','s_america','middle_east','north_africa','sub_sahara','steppe','east_indies','indochina','arab','amerindian','anzac'],
 'National recruitment': ['usa','csa','canada','mexico','cuba','argentina','brazil','peru','uruguay','paraguay','uk','scotland','france','prussia','spain','netherlands','denmark','sweden','norway','italy','austria','hungary','greece','russia','ottoman','morocco','muscat','egypt','ethiopia','south_africa','zululand','india','persia','afghanistan','kokand','siam','china','japan','korea'],
 'Regional and auxiliary': ['albania','armenia','bavaria','bulgaria','georgia','hanover','siberia','tibet','mongolia','manchuria'],
 'Non-recruitment': ['fish'],
}
palette = {
 'North America':(92,132,168),'South America':(91,151,117),'Europe':(144,122,173),
 'North Africa & Middle East':(190,146,85),'Sub-Saharan Africa':(139,111,78),
 'South & Central Asia':(170,112,111),'East Asia':(191,105,126),
 'Southeast Asia & Oceania':(78,151,151),'Other':(130,134,139)
}
def macro(tags):
    s=set(tags)
    for name, rule in macro_rules:
        if s & rule: return name
    return 'Other'

src = Image.open(MAP).convert('RGB')
pix = src.load(); w,h=src.size
rgb_to_region = {r['rgb']:r for r in regions}
display = Image.new('RGB', src.size, (52,91,122)); dp=display.load()
for y in range(h):
    for x in range(w):
        c=pix[x,y]; r=rgb_to_region.get(c)
        if r: dp[x,y]=palette[macro(r['tags'])]
        elif c==(0,0,0): dp[x,y]=(234,218,160)
        elif c==(255,255,255): dp[x,y]=(210,232,240)
        else: dp[x,y]=(52,91,122)
# Thin region boundaries from changes in the authoritative colour map.
for y in range(1,h-1):
    for x in range(1,w-1):
        c=pix[x,y]
        if c in rgb_to_region and any(pix[nx,ny] in rgb_to_region and pix[nx,ny]!=c for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1))):
            dp[x,y]=(39,45,52)

def png_uri(im):
    b=io.BytesIO(); im.save(b,'PNG',optimize=True)
    return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()

data=[]
for r in regions:
    data.append({'rgb':','.join(map(str,r['rgb'])),'region':loc.get(r['key'],r['key']),
                 'settlement':loc.get(r['settlementKey'],r['settlementKey']),
                 'owner':owner_by_region.get(r['key'],'unknown'),'tags':r['tags'],'macro':macro(r['tags'])})

fragment=f'''<div id="ss-world-map">
<h2>Steam &amp; Steel campaign world</h2>
<div class="viz-controls"><label class="form-label">Tag group<select class="form-select" id="ss-tag-group"></select></label><label class="form-label">Specific tag<select class="form-select" id="ss-tag"><option value="">All tags in group</option></select></label></div>
<div class="ss-map-wrap"><canvas id="ss-map" role="img" aria-label="Interactive reconstruction of the Steam and Steel campaign regions"></canvas></div>
<div class="card ss-detail" id="ss-detail" aria-live="polite"><strong>Move over or select a region</strong><span class="text-muted">The map follows the exact region boundaries and tags loaded by Steam &amp; Steel.</span></div>
<div class="ss-legend">{''.join(f'<span><i style="background:rgb{palette[n]}"></i>{n}</span>' for n,_ in macro_rules)}<span><i style="background:rgb{palette['Other']}"></i>Other / untagged</span></div>
<script>
(()=>{{const root=document.getElementById('ss-world-map'),canvas=root.querySelector('#ss-map'),detail=root.querySelector('#ss-detail');
const display=new Image(),ids=new Image(),regions={json.dumps({r['rgb']:r for r in data},ensure_ascii=False)};
const groups={json.dumps(tag_groups,ensure_ascii=False)},groupSel=root.querySelector('#ss-tag-group'),tagSel=root.querySelector('#ss-tag');
display.src={json.dumps(png_uri(display))};ids.src={json.dumps(png_uri(src))};let idCanvas=document.createElement('canvas'),idctx=idCanvas.getContext('2d',{{willReadFrequently:true}}),ctx=canvas.getContext('2d'),idPixels=null,ready=false;
for(const name of Object.keys(groups))groupSel.add(new Option(name,name));
function populateTags(){{tagSel.length=0;tagSel.add(new Option('All tags in group',''));for(const tag of groups[groupSel.value])tagSel.add(new Option(tag,tag));draw();}}
function draw(){{if(!ready)return;const width=Math.max(320,root.clientWidth),height=Math.round(width*{h}/{w});canvas.width=width;canvas.height=height;ctx.imageSmoothingEnabled=false;ctx.drawImage(display,0,0,width,height);const selected=tagSel.value;if(selected){{const image=ctx.getImageData(0,0,width,height),d=image.data;for(let y=0;y<height;y++)for(let x=0;x<width;x++){{const sx=Math.min({w-1},Math.floor(x/width*{w})),sy=Math.min({h-1},Math.floor(y/height*{h})),si=(sy*{w}+sx)*4,r=regions[`${{idPixels[si]}},${{idPixels[si+1]}},${{idPixels[si+2]}}`];if(r&&!r.tags.includes(selected)){{const i=(y*width+x)*4;d[i]=82;d[i+1]=84;d[i+2]=87;}}}}ctx.putImageData(image,0,0);}}}}
Promise.all([new Promise(r=>display.onload=r),new Promise(r=>ids.onload=r)]).then(()=>{{idCanvas.width={w};idCanvas.height={h};idctx.drawImage(ids,0,0);idPixels=idctx.getImageData(0,0,{w},{h}).data;ready=true;populateTags();}});new ResizeObserver(draw).observe(root);groupSel.addEventListener('change',populateTags);tagSel.addEventListener('change',draw);
function pick(e){{const b=canvas.getBoundingClientRect(),x=Math.max(0,Math.min({w-1},Math.floor((e.clientX-b.left)/b.width*{w}))),y=Math.max(0,Math.min({h-1},Math.floor((e.clientY-b.top)/b.height*{h}))),p=idctx.getImageData(x,y,1,1).data,r=regions[`${{p[0]}},${{p[1]}},${{p[2]}}`];if(!r)return;detail.innerHTML=`<strong>${{r.region}} — ${{r.settlement}}</strong><span>${{r.tags.join(', ')||'no geographic tag'}} · starting owner: ${{r.owner}} · ${{r.macro}}</span>`;}}
canvas.addEventListener('pointermove',pick);canvas.addEventListener('click',pick);
}})();
</script>
<style>
#ss-world-map{{display:grid;gap:12px;color:var(--foreground)}}#ss-world-map h2{{margin:0}}.ss-map-wrap{{width:100%;overflow:hidden}}#ss-map{{display:block;width:100%;height:auto;image-rendering:pixelated}}.ss-detail{{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center}}.ss-detail strong{{font-weight:500}}.ss-legend{{display:flex;flex-wrap:wrap;gap:8px 14px;color:var(--muted-foreground);font-size:12px}}.ss-legend span{{display:inline-flex;align-items:center;gap:6px}}.ss-legend i{{display:inline-block;width:12px;height:12px}}
</style></div>'''
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(fragment,encoding='utf-8');print(OUT);print('bytes',OUT.stat().st_size)
