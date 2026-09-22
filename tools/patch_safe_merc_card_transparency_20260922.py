from pathlib import Path
p=Path(__file__).with_name('preview_safe_remaining_mercenary_cards_20260922.py')
s=p.read_text(encoding='utf-8')
old=" bins=Counter(tuple(c//10 for c in px[:3]) for px in samples if px[3]>=32)\n key=bins.most_common(1)[0][0]; chosen=[px for px in samples if tuple(c//10 for c in px[:3])==key]"
new=" bins=Counter(tuple(c//10 for c in px[:3]) for px in samples if px[3]>=32)\n if not bins:return CANON\n key=bins.most_common(1)[0][0]; chosen=[px for px in samples if tuple(c//10 for c in px[:3])==key]"
if old not in s:raise SystemExit('patch target missing')
p.write_text(s.replace(old,new),encoding='utf-8')
