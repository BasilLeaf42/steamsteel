from pathlib import Path

root = Path(__file__).resolve().parents[1]
for relative in (
    "data/descr_rebel_factions.txt",
    "data/world/maps/campaign/camp_steamsteel/descr_strat.txt",
    "data/world/maps/campaign/imperial_campaign/descr_strat.txt",
):
    path = root / relative
    text = path.read_text(encoding="utf-8", errors="strict")
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8"))
