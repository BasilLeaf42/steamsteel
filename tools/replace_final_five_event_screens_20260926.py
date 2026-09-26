from pathlib import Path
import json
import shutil
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "event_screen_replacement_20260926"
SOURCES = OUT / "sources"
BACKUP = OUT / "originals"
OUT.mkdir(parents=True, exist_ok=True)
SOURCES.mkdir(parents=True, exist_ok=True)

records = {
    "timurids_invasion_warn.tga": {
        "title": "File:Wassilij Wassiljewitsch Wereschtschagin 003.jpg",
        "label": "Irregular Cavalry",
        "artist": "Vasily Vereshchagin",
        "date": "1873",
        "license": "Public domain",
    },
    "football_banned.tga": {
        "title": "File:Thomas Hemy Sunderland v Aston Villa 1895 A Corner Kick.jpg",
        "label": "Sunderland v Aston Villa: A Corner Kick",
        "artist": "Thomas M. Hemy",
        "date": "1895",
        "license": "Public domain",
    },
    "gunpowder_discovered.tga": {
        "title": "File:Interior of a gunpowder manufactory, and the instruments use Wellcome V0023593EL.jpg",
        "label": "Interior of a Gunpowder Manufactory",
        "artist": "Bénard after Louis-Jacques Goussier",
        "date": "18th-century engraving retained as a technical subject",
        "license": "Public domain",
    },
    "grote_mandenke.tga": {
        "title": "File:Alfred Sisley, Flood at Port-Marly, 1872, NGA 66436.jpg",
        "label": "Flood at Port-Marly",
        "artist": "Alfred Sisley",
        "date": "1872",
        "license": "CC0 / public domain",
    },
    "world_is_round.tga": {
        "title": "File:1891 world map - Karte der Erde nach Mercator; Politische Übersicht und Darstellung des Weltverkehrs mit Angabe der Dampferlinien, der unterseeischen Kabel etc.djvu",
        "label": "World Traffic and Communications Map",
        "artist": "Oswald Meinke and Carl Friedrich Baur",
        "date": "1891",
        "license": "Public domain",
    },
}


def commons_image(title: str, destination: Path) -> str:
    query = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": "1800",
        "titles": title,
    })
    request = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + query,
        headers={"User-Agent": "SteamSteelArtworkAudit/1.0"},
    )
    with urllib.request.urlopen(request) as response:
        payload = json.load(response)
    page = next(iter(payload["query"]["pages"].values()))
    info = page["imageinfo"][0]
    url = info.get("thumburl", info["url"])
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "SteamSteelArtworkAudit/1.0"})) as response:
        destination.write_bytes(response.read())
    return url


def cover_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    ratio = max(width / image.width, height / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


source_register = []
for filename, metadata in records.items():
    source_path = SOURCES / (Path(filename).stem + ".img")
    source_url = commons_image(metadata["title"], source_path)
    metadata["source_page"] = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(metadata["title"].replace(" ", "_"), safe=":;(),'_-.")
    metadata["download_url"] = source_url

    with Image.open(source_path) as opened:
        artwork = opened.convert("RGB")
    artwork = cover_crop(artwork, 317, 118)
    artwork = ImageEnhance.Contrast(artwork).enhance(1.04)

    targets = sorted((ROOT / "data" / "ui").glob(f"*/eventpics/{filename}"))
    if not targets:
        raise FileNotFoundError(filename)
    for target in targets:
        relative = target.relative_to(ROOT)
        backup = BACKUP / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(target, backup)
        with Image.open(target) as opened:
            framed = opened.convert("RGBA")
        framed.paste(artwork.convert("RGBA"), (25, 15))
        framed.save(target, format="TGA")

    source_register.append({"event": filename, "targets": [str(p.relative_to(ROOT)) for p in targets], **metadata})

(OUT / "source_register.json").write_text(json.dumps(source_register, indent=2, ensure_ascii=False), encoding="utf-8")

preview = Image.new("RGB", (760, 540), "#28241f")
draw = ImageDraw.Draw(preview)
font = ImageFont.load_default()
draw.text((8, 8), "Installed final five event-screen replacements", fill="white", font=font)
for index, filename in enumerate(records):
    target = next((ROOT / "data" / "ui").glob(f"*/eventpics/{filename}"))
    with Image.open(target) as opened:
        image = opened.convert("RGBA")
        backdrop = Image.new("RGBA", image.size, "#28241f")
        backdrop.alpha_composite(image)
        thumb = backdrop.convert("RGB")
    x = 8 + (index % 2) * 375
    y = 30 + (index // 2) * 165
    preview.paste(thumb, (x, y + 18))
    draw.text((x, y), filename, fill="white", font=font)
preview.save(OUT / "installed_contact_sheet.png")
print(f"Installed {len(records)} sourced event-screen replacements; originals: {BACKUP}")
