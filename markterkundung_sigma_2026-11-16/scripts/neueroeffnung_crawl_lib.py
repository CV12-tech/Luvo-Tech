"""Crawler neueroeffnung.info (öffentliche Einträge, 1 req/s, robots.txt beachtet)."""
import sys, re, json, time, pathlib, urllib.request, datetime as dt
from bs4 import BeautifulSoup
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from plz import land, stufe, vorfilter
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) markterkundung-research"}
def get(u):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r: return r.read()
        except Exception as e:
            if "404" in str(e): return b""
            time.sleep(3 * (i + 1))
    return b""
ENTRY = re.compile(r"^https://www\.neueroeffnung\.info/(?!branche/|stadt/|unternehmen/|entries/|karte|profile|token)[a-z0-9-]+/[a-z0-9_-]+$")
def listing(cat, maxpage):
    urls = []
    for p in range(1, maxpage + 1):
        h = get(f"https://www.neueroeffnung.info/branche/{cat}?page={p}"); time.sleep(1.0)
        s = BeautifulSoup(h, "html.parser"); new = [a["href"] for a in s.find_all("a", href=True) if ENTRY.match(a["href"])]
        if not new: break
        urls += new
    return list(dict.fromkeys(urls))
def parse(u, h, cat):
    s = BeautifulSoup(h, "html.parser"); t = s.get_text("\n"); t1 = re.sub(r"[ \t]+", " ", t)
    title = (s.title.string if s.title else "").split("|")[0].strip()
    m = re.search(r"Eröffnung:\s*\n?\s*(\d{2}\.\d{2}\.\d{4}|[^\n]{3,40})", t1)
    adr = re.search(r"([A-ZÄÖÜa-zäöüß.\- ]+\s?\d+[a-zA-Z]?(?:-\d+)?),?\s*(\d{5})\s+([^\n]+)", t1)
    plz = adr.group(2) if adr else None
    i = t1.find(title.replace("[NEU] ", "")[:20], t1.find("Kontaktdaten")) if title else -1
    body = t1[t1.find("Kontaktdaten"):][:2500] if "Kontaktdaten" in t1 else t1[:2500]
    tl = title.lower()
    typ = "Umbau" if "im umbau" in tl else ("Wiedereröffnung" if "wiedereröffnet" in tl else ("Schließung" if "schließt" in tl else ("Gerücht" if "gerücht" in tl or cat == "geruechte" else "Neueröffnung")))
    return {"url": u, "kategorie": cat, "titel": title, "typ": typ, "eroeffnung": m.group(1).strip() if m else None,
            "adresse": (adr.group(1).strip() + ", " + plz + " " + adr.group(3).strip()) if adr else None, "plz": plz,
            "land": land(plz) if vorfilter(plz) else None, "stufe": stufe(land(plz), plz) if vorfilter(plz) else None, "text": re.sub(r"\s+", " ", body)[:3000],
            "abgerufen": dt.datetime.now().isoformat(timespec="seconds")}
