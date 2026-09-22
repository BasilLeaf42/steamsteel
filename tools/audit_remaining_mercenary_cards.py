from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
AUDIT = json.loads((ROOT / "tools/remaining_mercenary_audit.json").read_text(encoding="utf-8"))
types = [row["type"] for row in AUDIT["units"] if row["category"] != "ship"]
folders = [ROOT / "data/ui/units/mercs", ROOT / "data/ui/units/slave"]
canonical = (184, 173, 143)
results = []

for unit_type in types:
    copies = [folder / f"#{unit_type}.tga" for folder in folders]
    row = {"type": unit_type, "copies": [], "identical": False}
    payloads = []
    for card in copies:
        if not card.exists():
            row["copies"].append({"path": str(card.relative_to(ROOT)), "missing": True})
            continue
        payloads.append(card.read_bytes())
        with Image.open(card) as source:
            rgba = source.convert("RGBA")
            corners = [rgba.getpixel(point)[:3] for point in ((0, 0), (47, 0), (0, 63), (47, 63))]
            row["copies"].append({
                "path": str(card.relative_to(ROOT)),
                "size": list(source.size),
                "mode": source.mode,
                "canonical_corners": all(pixel == canonical for pixel in corners),
            })
    row["identical"] = len(payloads) == 2 and payloads[0] == payloads[1]
    results.append(row)

cols = 8
cell_w, cell_h = 150, 96
rows = (len(types) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (38, 35, 30))
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default()
for index, unit_type in enumerate(types):
    x = (index % cols) * cell_w
    y = (index // cols) * cell_h
    card = folders[0] / f"#{unit_type}.tga"
    if card.exists():
        with Image.open(card) as source:
            sheet.paste(source.convert("RGB"), (x + 4, y + 4))
    label = unit_type.replace("merc_", "")
    while len(label) > 21:
        draw.text((x + 56, y + 5), label[:21], fill="white", font=font)
        label = label[21:]
        y += 11
    draw.text((x + 56, y + 5), label, fill="white", font=font)

(ROOT / "tools/remaining_mercenary_card_audit.json").write_text(
    json.dumps(results, indent=2) + "\n", encoding="utf-8"
)
sheet.save(ROOT / "tools/remaining_mercenary_cards_contact_sheet.png")
