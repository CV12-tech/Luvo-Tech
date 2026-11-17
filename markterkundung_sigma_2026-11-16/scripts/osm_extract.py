"""Extrahiert Lebensmittel-Shops aus einem OSM-PBF (Nodes+Ways, ohne Geometrie) und ordnet sie über addr:postcode den 11 Ländern zu."""
import sys, json, pathlib, osmium
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from plz import land, stufe
SHOPS = {"bakery", "butcher", "supermarket", "convenience", "deli", "greengrocer", "organic", "farm", "seafood", "cheese", "pastry", "health_food", "beverages", "wine", "kiosk"}
pbf, out = sys.argv[1], sys.argv[2]; n = 0; kept = 0
with open(out, "w") as f:
    for o in osmium.FileProcessor(pbf).with_filter(osmium.filter.KeyFilter("shop")):
        if o.is_relation(): continue
        t = o.tags; sh = t.get("shop")
        if sh not in SHOPS: continue
        n += 1; plz = t.get("addr:postcode"); l = land(plz) if plz else None
        if not l: continue
        loc = None
        if o.is_node() and o.location.valid(): loc = [round(o.location.lat, 5), round(o.location.lon, 5)]
        rec = {"osm": f"{'n' if o.is_node() else 'w'}{o.id}", "shop": sh, "name": t.get("name"), "brand": t.get("brand"), "operator": t.get("operator"),
               "plz": plz, "ort": t.get("addr:city"), "strasse": (t.get("addr:street") or "") + " " + (t.get("addr:housenumber") or ""), "land": l,
               "stufe": stufe(l, plz), "web": t.get("website") or t.get("contact:website"), "loc": loc}
        f.write(json.dumps(rec, ensure_ascii=False) + "\n"); kept += 1
print("shops", n, "region", kept)
