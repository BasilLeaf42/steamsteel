import json, hashlib, html, shutil
from pathlib import Path
from collections import Counter
from PIL import Image, ImageOps, ImageDraw, ImageFont
from research import BASE, clean

# Editorial offsets within the excess dimension: 0 = top/left, 1 = bottom/right.
# Each choice is subject-specific, then inspected in the rendered review sheets.
CHOICES = {
1:(.83,'Keep railway labourers, wheelbarrows and track; remove excess sky.'),
2:(.65,'Keep waterfront buildings, trading vessels and foreground boats.'),
3:(.62,'Retain ship, iceberg and ice; reduce empty upper sky.'),
4:(.10,'Focus on the two fighting warships and smoke; foreground spectator boat is outside this detail.'),
5:(.78,'Keep the complete firing line and nearest fallen figures.'),
6:(.91,'Focus on the royal family group; crop the high ceiling.'),
7:(.43,'Keep riders, horse heads and smoke signal together.'),
8:(.74,'Prioritize gun teams, riders and carriage wheels.'),
9:(.88,'Keep the execution line and gun wheels; remove empty sky.'),
10:(.76,'Keep anchorage, ships and water; reduce sky.'),
11:(.77,'Keep the woodland skirmishers; crop upper tree canopy.'),
12:(.76,'Keep barricade defenders and raised tricolour; reduce upper facade.'),
13:(.46,'Keep Westminster tower, moon and riverside promenade.'),
14:(.39,'Keep seated group, faces and bullet-casting work.'),
15:(.78,'Retain the riders and horses across the prairie.'),
16:(.30,'Keep deck passengers and their interactions; trim overhead rigging.'),
17:(.05,'Emphasize balloon, dirigible and aeroplane against the skyline.'),
18:(.65,'Keep cafe patrons, faces and tables; reduce upper lighting and lower floor.'),
20:(.65,'Keep burning ships, reflections and horizon.'),
21:(.78,'Retain defenders and firing position; reduce upper wall.'),
22:(.45,'Keep fleeing family and horse silhouette together.'),
23:(.00,'Balance dream figures at left with reclining man at right.'),
24:(.36,'Keep faces, umbrellas and receding Paris street.'),
25:(.62,'Focus on workers and glowing rolling-mill operation.'),
26:(.65,'Keep the royal barge, riverside steps and gathering.'),
27:(.85,'Focus on mourners and coffins in the square.'),
28:(.69,'Keep mounted hunter and buffalo; reduce distant sky.'),
29:(.66,'Keep camel riders and caravan line without cutting heads.'),
30:(.63,'Focus on the moving patrol and its street setting.'),
31:(.63,'Retain temple entrance, prayer flags and foreground worshipper.'),
32:(.89,'Focus on the assembly and imperial dais; reduce ceiling.'),
33:(.79,'Keep wedding participants and courtyard gathering.'),
34:(.08,'Retain chimneys, industry and rail infrastructure.'),
35:(.45,'Keep full procession and wheat-field setting.'),
36:(.78,'Focus on locomotives, platforms and steam.'),
37:(.78,'Retain public gathering and gateway entrance.'),
38:(.73,'Keep locomotive, rail line and foreground snow.'),
39:(.89,'Keep defenders, field guns and railway foreground; reduce sky.'),
40:(.65,'Horizontal crop favors rolling machinery and workers at right.'),
41:(.64,'Keep Napoleon, escort, horses and carriage.'),
42:(.76,'Keep exhibition visitors and the lower picture display.'),
43:(.69,'Retain travellers and mounts along the caravan.'),
44:(.43,'Keep all three faces, chessboard and hands.'),
45:(.85,'Keep official assembly and lower waterfront facade.'),
46:(.00,'Keep mountain pinnacles and the passage between cliffs.'),
47:(.45,'Emphasize the monumental arch, tiled facade and minarets.'),
48:(.79,'Keep patrol, horses and roadside encounter; reduce sky.'),
49:(.75,'Keep Seoul rooftops, city and mountain backdrop.'),
50:(.76,'Keep diplomats, imperial hosts and audience.'),
51:(.20,'Focus on printer, type case and press mechanism.'),
52:(.72,'Keep defenders, rifles and firing window.'),
53:(.75,'Focus on miners and their work beside the stream.'),
54:(.78,'Keep street vendors, diners and mosque entrance.'),
55:(.82,'Keep exhausted soldiers and stacked rifles in the snow.'),
56:(.82,'Keep troops, horses and public square; reduce sky.'),
57:(.68,'Keep arrested man, guards and witnesses.'),
58:(.55,'Keep officer, horse and infantry line.'),
59:(.12,'Keep barricade fighters, raised flag and street action.'),
60:(.61,'Balance sunset skyline with harbour shipping.'),
61:(.59,'Focus on the coronation dais and surrounding dignitaries.'),
62:(.72,'Keep expedition party, boats and riverbank farewell.')}

NEW = {
12:('The Barricade at Porte St Denis, Paris 1848','Nicolas Edward Gabé','1849','Urban revolution','A Paris barricade replaces the previous tall aftermath scene.'),
18:('A Parisian Cafe','Ilya Repin','1875','Coffeehouse social life','A Paris cafe replaces the tall coffee bearer; the cafe theme remains, with a different country.'),
39:('The Defense of Champigny','Édouard Detaille','1879','European military life','French troops defending Champigny replace the bivouac dream scene.'),
40:("Sheet-Rolling Workshop at the Abainville Forges",'Ignace-François Bonhommé','1838','Industrial machinery','A panoramic French rolling workshop replaces Iron and Coal.'),
44:('The Chess Players','Thomas Eakins','1876','Seated social exchange','An American chess gathering replaces the tall draughts scene in Egypt; the people and location differ.'),
46:('A Mountain Pass','Franz Roubaud','Undated; before 1928','Travel through a mountain pass','A Caucasus mountain landscape replaces the tall mounted-traveller scene. The source does not establish a more precise painting date.'),
55:('Night Bivouac of the Grande Armée','Vasily Vereshchagin','1896–1897','Military rest and hardship','A period oil depicting Napoleon’s retreat in 1812 replaces the tall wounded Montenegrin scene; this is an earlier historical subject.'),
62:('Study for Departure of the Monção','Almeida Júnior','1897','Brazilian expedition','A river expedition and farewell replace woodland hunters; this period painting depicts an earlier Brazilian expedition.')}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    old=json.loads((BASE/'revision1/source_register.json').read_text(encoding='utf-8'))
    meta=json.loads((BASE/'selected_metadata.json').read_text(encoding='utf-8'))
    result=[]
    for r0,row in zip(old,meta):
        r=dict(r0);n=r['slot'];path=BASE/'staged'/r['staged_file']
        if n==19:
            shutil.copy2(BASE/'archive'/(r['original_runtime_sha256']+'.tga'),path)
            r.update(title='Plevna surrender — preserved original',artist='Original installed artwork',date='Unverified',
                     theme='Surrender at Plevna',approximation='Original screen restored byte-for-byte at the user’s explicit request.',
                     medium='Preserved original; attribution and rights not reassessed',medium_verified=False,
                     licence='Preserved original — rights unverified',source_url='',source_revision_url='',medium_evidence=None,
                     retained_original=True,crop_box=None,crop_reason='Original framing retained exactly.',fitted_box=[0,0,1024,490],
                     formatting='Unmodified original 1024×768 TGA.',source_sha256=r['original_runtime_sha256'])
            for key in ['commons_file','source_revision','download_url','licence_url','rights_basis','credit','original_artist_metadata']:
                r.pop(key,None)
            canvas=Image.open(path).convert('RGBA')
        else:
            if n in NEW:
                r.update(dict(zip(['title','artist','date','theme','approximation'],NEW[n])))
                p=row['page'];ii=p['imageinfo'][0];m=ii['extmetadata']
                ev=json.loads((BASE/'evidence'/f"{p['pageid']}.json").read_text(encoding='utf-8'))
                wt=ev['revisions'][0]['slots']['main']['*']
                evidence_url=ii['descriptionurl'];basis='Oil medium explicitly stated in archived Commons description.'
                if n==12:
                    wd=json.loads((BASE/'evidence/Q119074285.json').read_text())
                    assert any(x['mainsnak'].get('datavalue',{}).get('value',{}).get('id')=='Q296955' for x in wd['entities']['Q119074285']['claims']['P186'])
                    evidence_url='https://www.wikidata.org/wiki/Q119074285';basis='P186 material claim: oil paint; entity response archived.'
                else: assert any(s in wt.lower() for s in ['oil','huile sur toile']),n
                side=json.loads((BASE/'sources'/f'{n:02}.download.json').read_text())
                r.update(commons_file=p['title'],source_url=ii['descriptionurl'],source_revision=ev['revisions'][0]['revid'],
                         source_revision_url='https://commons.wikimedia.org/w/index.php?oldid='+str(ev['revisions'][0]['revid']),
                         download_url=side['url'],source_sha256=side['sha256'],licence=clean(m['LicenseShortName']['value']),
                         licence_url=m.get('LicenseUrl',{}).get('value','https://creativecommons.org/publicdomain/mark/1.0/'),
                         rights_basis=clean(m.get('UsageTerms',{}).get('value','')),credit=clean(m.get('Credit',{}).get('value','')),
                         original_artist_metadata=clean(m.get('Artist',{}).get('value','')),medium_evidence=dict(url=evidence_url,basis=basis))
            side=json.loads((BASE/'sources'/f'{n:02}.download.json').read_text())
            assert side['title']==row['page']['title']
            r.update(source_sha256=side['sha256'],download_url=side['url'])
            src=BASE/'sources'/f'{n:02}.image';assert sha(src)==r['source_sha256']
            art=ImageOps.exif_transpose(Image.open(src)).convert('RGB');w,h=art.size
            r['source_pixel_size']=[w,h]
            base=[0,0,w,h]
            if n==45:base=[round(w*116/1280),round(h*119/954),round(w*1157/1280),round(h*832/954)]
            if n==39:base=[round(w*.008),round(h*.014),round(w*.994),round(h*.987)]
            if n==22:base=[round(w*.012),round(h*.01),round(w*.995),round(h*.99)]
            a,b,c,d=base;cw,ch=c-a,d-b;offset,reason=CHOICES[n]
            if cw/ch>1024/490:
                nw=round(ch*1024/490);a+=round((cw-nw)*offset);c=a+nw
            else:
                nh=round(cw*490/1024);b+=round((ch-nh)*offset);d=b+nh
            crop=[a,b,c,d]
            canvas=Image.open(BASE/'archive'/(r['original_runtime_sha256']+'.tga')).convert('RGBA')
            canvas.paste(art.crop(crop).resize((1024,490),Image.Resampling.LANCZOS),(0,0))
            canvas.save(path,compression='tga_rle',orientation=-1)
            r.update(crop_box=crop,crop_reason=reason,editorial_offset=offset,
                     formatting='Subject-specific crop filling the original 1024×490 artwork panel; no added borders or margins. Lower 278 rows preserved.',
                     fitted_box=[0,0,1024,490],final_visual_review='pending')
        r['staged_sha256']=sha(path)
        with Image.open(BASE/'archive'/(r['original_runtime_sha256']+'.tga')) as before:
            assert canvas.crop((0,490,1024,768)).tobytes()==before.convert('RGBA').crop((0,490,1024,768)).tobytes()
        canvas.convert('RGB').save(BASE/'previews'/f'{n:02}.jpg',quality=95)
        canvas.crop((0,0,1024,490)).convert('RGB').save(BASE/'previews'/f'{n:02}_art.jpg',quality=95)
        result.append(r)
    (BASE/'source_register.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for start in range(0,62,8):
        sheet=Image.new('RGB',(1040,1120),'#20242a');d=ImageDraw.Draw(sheet)
        for j,r in enumerate(result[start:start+8]):
            im=Image.open(BASE/'previews'/f"{r['slot']:02}_art.jpg");im.thumbnail((512,245));x=j%2*520;y=j//2*280
            sheet.paste(im,(x,y+28));d.text((x+5,y+5),f"{r['slot']:02} · {r['artist']}",font=font,fill='white')
        sheet.save(BASE/f'wide_review_{start//8+1:02}.jpg',quality=95)
    credits=['# Loading-screen artwork credits','61 sourced oil paintings plus the original Plevna surrender screen retained at the user’s request. Individual crops fill the original 1024×490 artwork panel. The lower loading-text area is unchanged.','Source rights: '+str(dict(Counter(r['licence'] for r in result)))+'.']
    for r in result:
        credits.extend([f"## Screen {r['slot']}: {r['title']}",f"{r['artist']}, {r['date']}. {r['medium']}.",r['approximation'],r['crop_reason']])
        if r.get('source_url'):
            credits.extend([f"Source: [{r['commons_file']}]({r['source_revision_url']}). Rights: [{r['licence']}]({r['licence_url']}).",f"Medium evidence: [{r['medium_evidence']['basis']}]({r['medium_evidence']['url']})."])
    (BASE/'ARTWORK_CREDITS.md').write_text('\n\n'.join(credits),encoding='utf-8')
    findings=json.loads((BASE.parent/'loading_art_audit_20260922/findings.json').read_text(encoding='utf-8'))
    page=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Loading artwork — individually composed wide crops</title><style>body{background:#171c1e;color:#eee8dc;font:17px/1.5 system-ui;max-width:1160px;margin:30px auto;padding:20px}a{color:#b8d8eb}article{padding:20px;background:#242b2e;margin:22px 0}img{width:100%}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}input{padding:12px;width:65%}small{color:#b5b5ac}</style><h1>Loading-screen artwork</h1><p>61 oil paintings with individually chosen wide crops, plus the preserved original Plevna surrender screen. All fill the original 1024 × 490 artwork panel; the 1024 × 768 game texture retains its dark text area below.</p><p id="status">Crop review in progress.</p><p><a href="ARTWORK_CREDITS.md">Sources and credits</a> · <a href="source_register.json">Crop decisions and verification</a></p><input placeholder="Find a screen, artist or theme" oninput="document.querySelectorAll(\'article\').forEach(e=>e.hidden=!e.textContent.toLowerCase().includes(this.value.toLowerCase()))">']
    for r in result:
        n=r['slot'];key=findings[n-1]['id']
        page.append(f'<article><h2>{n:02} · {html.escape(r["title"])}</h2><p>{html.escape(r["artist"])} · {html.escape(r["date"])}</p><div class="pair"><div><small>Original screen</small><img loading="lazy" src="../loading_art_audit_20260922/{key}_art.png"></div><div><small>Current crop — click for full texture</small><a href="previews/{n:02}.jpg"><img loading="lazy" src="previews/{n:02}_art.jpg"></a></div></div><p>{html.escape(r["crop_reason"])}</p><p>{html.escape(r["approximation"])}</p>')
        if r.get('source_url'):page.append(f'<a href="{html.escape(r["source_url"])}">Full painting and rights record</a>')
        page.append('</article>')
    (BASE/'gallery.html').write_text(''.join(page)+'</html>',encoding='utf-8')
    print('Built 61 wide crops and restored Plevna. Eight review sheets ready.')
if __name__=='__main__':run()
