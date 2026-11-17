"""TED API v3 Abrufer für die SIGMA-Markterkundung. Speichert Rohdaten und normalisierte JSONL."""
import json, sys, time, datetime as dt, pathlib, urllib.request

API = "https://api.ted.europa.eu/v3/notices/search"
NUTS = ["DEE", "DE3", "DE4", "DED", "DEG", "DE9", "DE8", "DE6", "DEF", "DE5", "DE7"]
CPV = ["39154000", "39154100", "39150000", "39151000", "39151100", "39151200", "39141000", "39141300",
       "39221000", "39221100", "39221110", "39314000", "39711130", "39711100", "42513000", "42513200",
       "45421153", "45421150", "45421000", "39100000", "79933000", "79930000", "39312000", "39312100", "39312200"]
FT = ["Ladenbau", "Ladeneinrichtung", "Bedientheke", "Ausgabetheke", "Thekenanlage", "Theke", "Cafeteria",
      "Mensa", "Speisenausgabe", "Ausgabeanlage", "Backshop", "Kühltheke", "Free-Flow", "Shopeinrichtung",
      "Kiosk", "Verkaufstheke", "Kassenzone", "Dorfladen", "Markthalle", "Museumsshop"]
FIELDS = ["publication-number", "notice-title", "buyer-name", "buyer-city", "place-of-performance",
          "classification-cpv", "publication-date", "deadline-receipt-tender-date-lot", "notice-type",
          "procedure-type", "estimated-value-lot", "total-value", "description-lot", "winner-name",
          "title-lot", "contract-duration-period-lot"]

def post(body, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(API, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception as e:
            print("retry", i, e, file=sys.stderr); time.sleep(2 ** i * 2)
    raise RuntimeError("TED nicht erreichbar")

def harvest(query, maxn=8000):
    out, token = [], None
    while True:
        body = {"query": query, "fields": FIELDS, "limit": 250, "paginationMode": "ITERATION"}
        if token: body["iterationNextToken"] = token
        d = post(body); out += d.get("notices", [])
        token = d.get("iterationNextToken")
        if not token or not d.get("notices") or len(out) >= maxn: return out, d.get("totalNoticeCount")
        time.sleep(1.1)

def de(v):
    if isinstance(v, dict):
        x = v.get("deu") or v.get("mul") or v.get("eng") or next(iter(v.values()), None)
        return x if not isinstance(x, list) else "; ".join(dict.fromkeys(x))
    if isinstance(v, list): return "; ".join(dict.fromkeys(map(str, v)))
    return v

def norm(n):
    pn = n["publication-number"]
    return {"pubnr": pn, "url": f"https://ted.europa.eu/de/notice/-/detail/{pn}",
            "titel": de(n.get("notice-title")), "lose": de(n.get("title-lot")), "auftraggeber": de(n.get("buyer-name")),
            "ort": de(n.get("buyer-city")), "nuts": de(n.get("place-of-performance")), "cpv": de(n.get("classification-cpv")),
            "veroeffentlicht": (n.get("publication-date") or "")[:10], "frist": de(n.get("deadline-receipt-tender-date-lot")),
            "typ": n.get("notice-type"), "verfahren": de(n.get("procedure-type")),
            "wert_geschaetzt": de(n.get("estimated-value-lot")), "wert_gesamt": n.get("total-value"),
            "gewinner": de(n.get("winner-name")), "laufzeit": de(n.get("contract-duration-period-lot")),
            "beschreibung": (de(n.get("description-lot")) or "")[:1500]}

if __name__ == "__main__":
    outdir = pathlib.Path(sys.argv[1]); outdir.mkdir(parents=True, exist_ok=True)
    since_open, since_award = sys.argv[2], sys.argv[3]       # JJJJMMTT
    geo = f"place-of-performance IN ({' '.join(NUTS)})"
    match = f"(classification-cpv IN ({' '.join(CPV)}) OR FT~({' OR '.join(chr(34)+t+chr(34) for t in FT)}))"
    jobs = {"offen_90t": f"{match} AND {geo} AND publication-date>={since_open}",
            "zuschlaege_5j": f"{match} AND {geo} AND publication-date>={since_award} AND notice-type IN (can-standard can-social can-modif can-desg can-tran)"}
    ts = dt.datetime.now().strftime("%Y%m%dT%H%M")
    for name, q in jobs.items():
        notices, total = harvest(q)
        (outdir / f"{ts}_{name}_raw.json").write_text(json.dumps({"query": q, "total": total, "notices": notices}, ensure_ascii=False))
        with open(outdir / f"{name}.jsonl", "w") as f:
            for n in notices: f.write(json.dumps(norm(n), ensure_ascii=False) + "\n")
        print(name, "total", total, "geholt", len(notices))
