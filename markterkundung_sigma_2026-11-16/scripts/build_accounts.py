"""Baut 03c_accounts.jsonl aus manuellen Accounts (work/accounts_manuell.json) und OSM-Filialnetzen; verknüpft Signale; Score (D)."""
import json, re, collections
S = [json.loads(l) for l in open("03b_signale.jsonl")]
M = json.load(open("work/accounts_manuell.json"))
O = json.load(open("raw/D/osm/accounts_osm.json"))
GENERISCH = {"backshop", "backstube", "bäckerei", "bäcker", "schneider", "schnell", "harmonie", "müller", "schmidt", "meyer", "markt", "feinkost",
             "hofladen", "fleischerei", "metzgerei", "konditorei", "café", "cafe", "bistro", "kiosk", "edeka", "rewe", "netto", "penny", "aldi", "lidl"}
ZENTRAL_X = re.compile(r"^(tante enso|getränke|trinkgut|hol ab|fristo|edeka getränke|rewe getränke|backwerk|back-factory|ditsch|kamps|le crobag|wiener feinbäcker)", re.I)
def lnk(tokens):
    tokens = [t for t in tokens if t and t not in GENERISCH and len(t) >= 6]
    return [s["id"] for s in S if any(t in s["organisation"].lower() for t in tokens)][:15]
acc = []
for m in M:
    m["verknuepfte_signale_ids"] = lnk(m.get("match", [])); m["verknuepfte_treffer_ids"] = []; acc.append(m)
names = {a["organisation"].lower() for a in acc}
for o in O:
    s1 = o["stufen"].get("1", 0); tot = o["filialen_osm"]; name = o["organisation"]
    if o["zentral_gesteuert"] or ZENTRAL_X.match(name): continue
    if name.upper() in ("REWE", "EDEKA", "E-CENTER", "REWE CITY", "REWE TO GO", "NAH&GUT", "KONSUM", "CAP", "NP", "NAHKAUF", "EDEKA CENTER", "NAH & FRISCH", "NAH UND GUT"): continue
    if name.lower() in GENERISCH or len(name) < 4: continue
    if o["segment"] not in (1, 2, 4, 5): continue
    keep = (s1 >= 2) or (s1 >= 1 and o["segment"] in (1, 4) and re.match(r"^(EDEKA|E-?CENTER|REWE|NAH&GUT|nah)", name, re.I)) or (tot >= 10 and o["segment"] == 2)
    if not keep or any(name.lower()[:10] in n for n in names): continue
    tok = name.lower()
    acc.append({"organisation": name, "typ": "Zielkunde", "segment": o["segment"], "filialen_anzahl": tot, "filialen_stufe1": s1, "standorte": o["top_orte"],
                "website": (o["website"] or [None])[0], "laender": o["laender"], "letzter_umbau": None, "verknuepfte_treffer_ids": [],
                "verknuepfte_signale_ids": lnk([tok] if len(tok.split()) > 1 or len(tok) >= 8 else []),
                "einkaufsweg": "Kaufmann/Inhaber (selbst)" if o["segment"] in (1, 4) else "Inhaber/GF (selbst)",
                "entscheiderrolle": "Inhaber/Kaufmann" if o["segment"] in (1, 4) else "Inhaber/GF", "beleg_url": o["beleg_osm"],
                "quelle": "OpenStreetMap (© OSM-Mitwirkende, ODbL)", "shop_typ": o["shop_typ"]})
for a in acc:
    if a.get("filialen_anzahl") is None and a.get("match") and a["typ"].startswith("Zielkunde") and a["segment"] == 2:
        hits = [o for o in O if any(t == o["organisation"].lower() or o["organisation"].lower().startswith(t) for t in a["match"])]
        if hits:
            a["filialen_anzahl"] = sum(h["filialen_osm"] for h in hits); a["filialen_stufe1"] = sum(h["stufen"].get("1", 0) for h in hits)
            a["standorte"] = list(dict.fromkeys(sum((h["top_orte"] for h in hits), [])))[:6]; a["beleg_url"] = a.get("beleg_url", []) + hits[0]["beleg_osm"][:2]
            a["filialen_quelle"] = "OSM (Untergrenze)"
ICP = {1: 30, 2: 30, 4: 25, 5: 20, 6: 15, 7: 15, 8: 10}
for a in acc:
    if not a["typ"].startswith("Zielkunde"): a["score"] = None; a["klasse"] = None; continue
    f = a.get("filialen_anzahl") or 1
    fil = 5 if f < 2 else (10 if f < 5 else (15 if f < 10 else (20 if f < 30 else 25)))
    sig = min(30, 15 * len(a["verknuepfte_signale_ids"]))
    umb = 15 if re.search(r"insolv|eigenverw|übernahme|übernimmt|tegut|\bnp\b", json.dumps({k: a.get(k) for k in ("organisation", "notiz", "filialen_hinweis", "einkaufsweg")}, ensure_ascii=False).lower()) else 10
    s = ICP.get(a["segment"], 10) + fil + sig + umb + (10 if a.get("bestandskunde") else 0) + (5 if a.get("hanse_altkunde") else 0)
    if a.get("filialen_stufe1") == 0: s = round(s * 0.8)
    a["score"] = min(100, s); a["klasse"] = "A" if s >= 75 else ("B" if s >= 50 else "C")
    a["umbaubedarf_geschaetzt"] = "hoch (Herleitung: Insolvenz/Übernahme/Umflaggung)" if umb == 15 else "mittel (Herleitung: Modernisierungszyklus 7–12 J., kein Einzelbeleg)"
acc.sort(key=lambda a: -(a["score"] or 0))
with open("03c_accounts.jsonl", "w") as fo:
    for a in acc: fo.write(json.dumps(a, ensure_ascii=False) + "\n")
zk = [a for a in acc if a["typ"] == "Zielkunde"]
print(len(acc), collections.Counter(a["typ"] for a in acc), collections.Counter(a.get("klasse") for a in acc))
print("Zielkunden:", len(zk), collections.Counter(a["segment"] for a in zk), "Kernregion:", sum(1 for a in zk if (a.get("filialen_stufe1") or 0) > 0))
for a in acc[:35]: print(a["score"], a["klasse"], a["segment"], a.get("filialen_anzahl"), "|", a["organisation"][:55], "|", a["verknuepfte_signale_ids"][:3])
