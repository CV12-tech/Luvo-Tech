"""Schneeball-Crawler über öffentliche Detailseiten von neueroeffnung.info (Umgebungslinks). 1 req/s, nur Zielregion wird expandiert."""
import sys, json, time, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from neueroeffnung_crawl_lib import get, parse, ENTRY
from bs4 import BeautifulSoup
OUT = pathlib.Path(sys.argv[1]); SEEN = OUT / "_entries.jsonl"; MAX = int(sys.argv[2]) if len(sys.argv) > 2 else 2500
recs = {json.loads(l)["url"]: json.loads(l) for l in open(SEEN)} if SEEN.exists() else {}
seeds = [l.strip() for l in open(OUT / "_seeds.txt") if l.strip()] if (OUT / "_seeds.txt").exists() else []
queue = list(dict.fromkeys(seeds + [u for u, r in recs.items() if r.get("land")])); expanded = set(); n = 0
RELEVANT = re.compile(r"edeka|rewe|netto|penny|lidl|aldi|kaufland|globus|famila|marktkauf|nah-?\s?&?\s?gut|nahgut|norma|combi|konsum|cap-|bio|denn|alnatura|tegut|tante|markt|bäck|baeck|back|konditor|fleisch|metzger|wurst|café|cafe|bistro|kantine|mensa|hofladen|feinkost|supermar|nahkauf|np-|wasgau|hit-|marktkauf|e-center|center", re.I)
CAT = {"supermaerkte": "supermaerkte", "baeckereien": "baeckereien", "gastronomie": "gastronomie", "shops": "shops", "geruechte": "geruechte"}
while queue and n < MAX:
    u = queue.pop(0)
    if u in expanded: continue
    expanded.add(u)
    h = get(u); time.sleep(1.0); n += 1
    if not h: continue
    s = BeautifulSoup(h, "html.parser")
    cat = next((c for c in CAT if f"/branche/{c}" in h.decode("utf-8", "ignore")[h.decode("utf-8","ignore").find("Kontaktdaten")-3000:h.decode("utf-8","ignore").find("Kontaktdaten")]), "unbekannt") if b"Kontaktdaten" in h else "unbekannt"
    if u not in recs:
        r = parse(u, h, cat); recs[u] = r
        with open(SEEN, "a") as f: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    r = recs[u]
    if r.get("land"):
        for a in s.find_all("a", href=True):
            v = a["href"]
            if ENTRY.match(v) and v not in expanded and v not in queue and RELEVANT.search(a.get_text(" ", strip=True) + " " + v): queue.append(v)
    if n % 50 == 0: print(n, len(recs), len(queue), flush=True)
print("fertig", n, len(recs))
