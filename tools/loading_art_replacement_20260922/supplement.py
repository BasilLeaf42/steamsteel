import json,time
from research import BASE,api,search

direct={
106:'File:The Family of Queen Victoria (Tuxen).jpg',
111:'File:Rothermel Battle of Gettysburg.jpg',
117:'File:Henri Rousseau - Vue de pont de Sèvres.jpg',
151:'File:Charles Frederick Ulrich - The Village Printing Shop, Haarlem, Holland (1884).jpg',
}
missing=[(n,t) for n,t in direct.items() if not (BASE/'search'/f'{n:02}.json').exists()]
if missing:
    result=api(dict(action='query',titles='|'.join(t for n,t in missing),redirects=1,prop='imageinfo',iiprop='url|size|extmetadata',iiurlwidth=1200))
    pages=list(result['query']['pages'].values())
    for n,t in missing:
        matches=[p for p in pages if p['title']==t and 'missing' not in p]
        (BASE/'search'/f'{n:02}.json').write_text(json.dumps(dict(query=t,pages=matches),indent=2),encoding='utf-8')
    time.sleep(3)

queries={102:'Wirgman oil',112:'Meissonier barricade',114:'Gérôme café',129:'Guillaumet caravan',130:'Gérôme Bashi',132:'Ekman diet 1863',133:'Delacroix Jewish wedding',136:'Monet gare Saint Lazare',137:'Vereshchagin triumph',141:'Camphausen Sedan',145:'Hubert Vos Chinese',146:'Vereshchagin mountain',149:'Hubert Vos Seoul',150:'Gérôme Siam',159:'Vernet barricade',131:'Vereshchagin Buddhist',148:'Brandt patrol',153:'Nahl miners',155:'Jovanović resting',156:'Repin council',158:'Thompson Roll Call'}
for item in queries.items():search(item)
print('Supplement complete')
