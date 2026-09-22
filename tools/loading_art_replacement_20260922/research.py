import urllib.request, urllib.parse, json, time, re, html
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE=Path(__file__).resolve().parent
UA='SteamSteelHistoricalArt/1.0 (public-domain painting research; Wikimedia Commons metadata)'

def api(params):
    url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(format='json',**params))
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=45) as r:
                result=json.load(r)
            if 'error' in result: raise RuntimeError(result['error'])
            return result
        except Exception:
            if attempt==5: raise
            time.sleep(15+attempt*12)

def clean(s):
    return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s))).strip()

def search(item):
    n,q=item; dest=BASE/'search'/f'{n:02}.json';dest.parent.mkdir(exist_ok=True)
    if dest.exists(): return
    r=api(dict(action='query',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=5,prop='imageinfo',iiprop='url|size|extmetadata',iiurlwidth=1200))
    pages=sorted(r.get('query',{}).get('pages',{}).values(),key=lambda x:x.get('index',0))
    dest.write_text(json.dumps(dict(query=q,pages=pages),indent=2),encoding='utf-8')
    print('Searched',n,flush=True)
    time.sleep(3)

QUERIES={
1:'Savitsky Repair railway',2:'China harbour oil painting 1850',3:'William Bradford Arctic painting',4:'Manet Kearsarge Alabama',
5:'Vereshchagin surprise attack',6:'Tuxen Victoria jubilee painting',7:'Remington smoke signal painting',8:'Detaille artillery oil',
9:'Vereshchagin suppression Indian revolt',10:'Whampoa anchorage oil painting',11:'Thulstrup Gettysburg painting',12:'Steffeck barricade 1848',
13:'Grimshaw Westminster',14:'Gerome coffee house Cairo',15:'Catlin Comanche feats horsemanship',16:'Tissot last evening',
17:'Jules Garnier balloon painting',18:'John Frederick Lewis coffee bearer',19:'Vereshchagin Plevna before attack',20:'Aivazovsky Sinop 1853',
21:'Vereshchagin fortress wall',22:'Eastman Johnson ride liberty',23:'Lecomte Nouy opium dream',24:'Gustave Caillebotte Paris Street Rainy Day',
25:'Adolph Menzel iron rolling mill',26:'Edwin Lord Weeks Benares',27:'Adolph Menzel March fallen',28:'Albert Bierstadt last buffalo',
29:'Gustave Guillaumet caravan',30:'Vereshchagin doors Tamerlane',31:'Edwin Lord Weeks temple India',32:'Akseli Gallen Kallela Paris boulevard',
33:'George Catlin dance painting',34:'Constantin Meunier black country',35:'Jules Breton blessing wheat',36:'Terence Cuneo armoured train',
37:'Vereshchagin triumphal',38:'Claude Monet train snow Argenteuil',39:'Detaille Le Reve',40:'William Bell Scott Iron Coal',
41:'Velazquez surrender Breda',42:'Edouard Dantan coin salon 1880',43:'Eugene Fromentin caravan',44:'Jean Leon Gerome chess players',
45:'Albert Edelfelt Pasteur',46:'Vereshchagin mountain pass',47:'Vereshchagin Samarkand',48:'Jozef Brandt cavalry patrol',
49:'Takahashi Yuichi street painting',50:'Jean Joseph Benjamin Constant last rebels',51:'John White Alexander printing',52:'Alphonse Neuville last cartridges',
53:'Albert Bierstadt gold mining',54:'John Frederick Lewis Cairo',55:'Vasily Polenov Montenegrin',56:'Ilya Repin ceremonial meeting state council',
57:'Ilya Repin arrest propagandist',58:'Jean Baptiste Edouard Detaille parade',59:'Ernest Meissonier barricade',60:'Thomas Daniell Canton',
61:'Laurits Tuxen coronation Nicholas',62:'Almeida Junior caipira picando fumo'
}

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=1) as pool:
        list(pool.map(search,QUERIES.items()))
    lines=[]
    for n,q in QUERIES.items():
        r=json.loads((BASE/'search'/f'{n:02}.json').read_text(encoding='utf-8'));lines.append(f'\nSLOT {n}: {q}')
        for i,p in enumerate(r['pages']):
            ii=p.get('imageinfo',[{}])[0];m=ii.get('extmetadata',{})
            fields=' | '.join(clean(m.get(k,{}).get('value',''))[:110] for k in ['Artist','DateTimeOriginal','LicenseShortName'])
            lines.append(f"{i}: {p['title']} | {ii.get('width')}x{ii.get('height')} | {fields}")
    (BASE/'search_summary.txt').write_text('\n'.join(lines),encoding='utf-8')
    print('Completed',len(QUERIES),'searches')
