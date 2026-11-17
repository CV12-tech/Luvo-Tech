"""Leitet Account-Kandidaten (Filialnetze, Kaufleute) aus OSM-Shopdaten ab."""
import sys, json, re, collections
rows = [json.loads(l) for l in open(sys.argv[1])]
ZENTRAL = re.compile(r"^(lidl|aldi|netto|penny|norma|kaufland|globus|real|edeka center$|rewe city$|nahkauf$|spar|diska|np|marktkauf|famila|combi|tegut|denns?|alnatura|rossmann|dm|budni|mix markt|bio company|basic|kaiser'?s|jet|aral|shell|esso|total|star|agip|hem|bft|orlen|avia|westfalen)\b", re.I)
SEG = {"bakery": 2, "pastry": 2, "butcher": 2, "supermarket": 1, "convenience": 8, "deli": 2, "greengrocer": 4, "organic": 5, "health_food": 5,
       "farm": 8, "seafood": 2, "cheese": 2, "beverages": 8, "wine": 8, "kiosk": 8}
def key(r):
    b = (r.get("brand") or "").strip(); n = (r.get("name") or "").strip()
    if r["shop"] in ("supermarket", "convenience") and n:
        m = re.match(r"^(EDEKA|E[- ]?Center|REWE|nah ?& ?gut|NP|Konsum|CAP|Markant|Combi|Nahkauf|Ihr Kaufmann)\b[\s\-–]*(.*)$", n, re.I)
        if m:
            fmt = m.group(1).upper().replace(" ", ""); rest = re.sub(r"\b(Markt|Center|Frischemarkt|Supermarkt|e\.?K\.?|GmbH|OHG|KG)\b", "", m.group(2), flags=re.I).strip(" -–")
            if fmt in ("KONSUM", "CAP", "MARKANT", "COMBI", "NP"): return fmt, fmt
            return (f"{fmt} {rest}".strip() if rest else fmt), fmt
    if b: return b, b
    if not n: return None, None
    n2 = re.sub(r"\b(Filiale|Backshop|Verkaufsstelle|Bäckerei-?Café|GmbH|& ?Co\.? ?KG|KG|e\.K\.|im \w+.*|am \w+.*|in \w+.*)\b", "", n, flags=re.I).strip(" -–,")
    return n2[:60] or n, None
acc = collections.defaultdict(lambda: {"filialen": 0, "laender": collections.Counter(), "orte": collections.Counter(), "shops": collections.Counter(), "web": set(), "stufen": collections.Counter(), "osm": []})
for r in rows:
    k, fmt = key(r)
    if not k: continue
    a = acc[k]; a["filialen"] += 1; a["laender"][r["land"]] += 1; a["orte"][r.get("ort") or r["plz"]] += 1; a["shops"][r["shop"]] += 1
    a["stufen"][r["stufe"]] += 1; a["fmt"] = fmt
    if r.get("web"): a["web"].add(r["web"])
    if len(a["osm"]) < 5: a["osm"].append(r["osm"])
out = []
for k, a in acc.items():
    shop = a["shops"].most_common(1)[0][0]; seg = SEG.get(shop, 8)
    if a.get("fmt") in ("EDEKA", "E-CENTER", "ECENTER", "REWE", "NAH&GUT", "NAHKAUF", "IHRKAUFMANN", "KONSUM", "CAP", "MARKANT"): seg = 4 if a["fmt"] in ("NAH&GUT", "CAP", "KONSUM", "MARKANT") else 1
    zentral = bool(ZENTRAL.match(k)) and not re.match(r"^(EDEKA|REWE|NAH)\s+\S", k, re.I)
    out.append({"organisation": k, "segment": seg, "shop_typ": shop, "filialen_osm": a["filialen"], "laender": dict(a["laender"]), "stufen": {str(s): c for s, c in a["stufen"].items()},
                "top_orte": [o for o, _ in a["orte"].most_common(6)], "website": sorted(a["web"])[:2], "zentral_gesteuert": zentral,
                "beleg_osm": [f"https://www.openstreetmap.org/{'node' if x[0]=='n' else 'way'}/{x[1:]}" for x in a["osm"]]})
out.sort(key=lambda x: -x["filialen_osm"])
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False)
print(len(out))
