from pathlib import Path
p=Path(__file__).with_name('preview_safe_remaining_mercenary_cards_20260922.py')
s=p.read_text(encoding='utf-8')
if 'dist(nxt,cur)<=10' not in s:raise SystemExit('threshold target missing')
p.write_text(s.replace('dist(nxt,cur)<=10','dist(nxt,cur)<=16'),encoding='utf-8')
