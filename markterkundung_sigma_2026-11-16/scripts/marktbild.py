"""Modul E: öffentliches Beschaffungsvolumen in Ziel-CPV aus oeffentlichevergabe.de-Aggregaten (12/2023–11/2026) + TED (5 J.)."""
import json, glob, collections
agg = collections.defaultdict(lambda: {"n": 0, "wert": 0.0}); tage = 0; alle = 0; reg = 0
for f in glob.glob("raw/A/oeffentlichevergabe/*_agg.json"):
    d = json.load(open(f)); tage += 1; alle += d["alle"]; reg += d["region"]
    jahr = d["tag"][:4]
    for k, v in d["agg"].items():
        land, cpv, typ = k.split("|")
        for key in (f"{jahr}|{land}|{cpv}|{typ}", f"ALLE|{land}|ALLE|{typ}", f"{jahr}|ALLE|ALLE|{typ}"):
            agg[key]["n"] += v["n"]; agg[key]["wert"] += v["wert"]
ted = [json.loads(l) for l in open("raw/A/ted/zuschlaege_5j.jsonl")]
ted_jahr = collections.defaultdict(lambda: {"n": 0, "wert": 0.0})
ZIEL = ("39154", "39150", "39151", "39141", "39221", "39314", "39312", "39711", "42513", "45421153", "45421151", "79933", "79930")
for t in ted:
    if not any(c.startswith(ZIEL) for c in (t["cpv"] or "").split("; ")): continue
    j = t["veroeffentlicht"][:4]; ted_jahr[j]["n"] += 1; ted_jahr[j]["wert"] += float(t["wert_gesamt"] or 0)
out = {"ov_tage": tage, "ov_bekanntmachungen_gesamt": alle, "ov_bekanntmachungen_region": reg, "ov_agg": agg, "ted_zuschlaege_jahr": ted_jahr}
json.dump(out, open("work/marktbild_volumen.json", "w"), ensure_ascii=False, indent=1, default=float)
NAMES = {"DEE": "ST", "DE3": "BE", "DE4": "BB", "DED": "SN", "DEG": "TH", "DE9": "NI", "DE8": "MV", "DE6": "HH", "DEF": "SH", "DE5": "HB", "DE7": "HE"}
print("Tage:", tage, "Bekanntmachungen:", alle, "Region:", reg)
for l in NAMES:
    a = agg.get(f"ALLE|{l}|ALLE|award", {"n": 0, "wert": 0}); t = agg.get(f"ALLE|{l}|ALLE|tender", {"n": 0, "wert": 0})
    print(NAMES[l], "Zuschläge", a["n"], round(a["wert"] / 1e6, 1), "Mio € | Ausschreibungen", t["n"], round(t["wert"] / 1e6, 1), "Mio € (gesch. Wert, oft leer)")
for j in sorted(ted_jahr): print("TED", j, ted_jahr[j]["n"], round(ted_jahr[j]["wert"] / 1e6, 1), "Mio €")
