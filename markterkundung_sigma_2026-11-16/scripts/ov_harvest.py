"""oeffentlichevergabe.de (Datenservice öffentlicher Einkauf) – Tagesexporte OCDS.
Speichert je Tag: relevante Kandidaten (JSONL) + Volumen-Aggregate für Ziel-CPV (JSON). Zips werden gelöscht."""
import json, sys, io, time, zipfile, datetime as dt, pathlib, urllib.request, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from relevanz import score
NUTS = ("DEE", "DE3", "DE4", "DED", "DEG", "DE9", "DE8", "DE6", "DEF", "DE5", "DE7")
CPV_ZIEL = ("39154", "39150", "39151", "39141", "39221", "39314", "39312", "39711", "42513", "45421153", "45421151", "79933", "79930")
UA = {"User-Agent": "markterkundung-scout/1.0 (research; contact via repo owner)"}

def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r: return r.read()
        except Exception as e:
            if "404" in str(e): return None
            time.sleep(2 ** i * 2)
    return None

def compact(r):
    t = r.get("tender", {}); b = r.get("buyer", {}); items = t.get("items", [])
    cpv = list(dict.fromkeys([i.get("classification", {}).get("id") for i in items if i.get("classification")] +
                             [a.get("id") for i in items for a in i.get("additionalClassifications", []) if a.get("scheme") == "CPV"]))
    regs = list(dict.fromkeys([b.get("address", {}).get("region")] + [i.get("deliveryAddress", {}).get("region") for i in items]))
    regs = [x for x in regs if x]
    orte = list(dict.fromkeys([i.get("deliveryAddress", {}).get("locality") for i in items if i.get("deliveryAddress", {}).get("locality")]))
    lots = t.get("lots", [])
    aw = [{"lieferant": "; ".join(s.get("name", "") for s in a.get("suppliers", [])) or a.get("title"),
           "lieferant_ort": "; ".join(s.get("address", {}).get("locality", "") for s in a.get("suppliers", [])),
           "wert": (a.get("value") or {}).get("amount"), "datum": (a.get("date") or "")[:10], "los": a.get("relatedLots")} for a in r.get("awards", [])]
    return {"id": r.get("id"), "ocid": r.get("ocid"), "tag": r.get("tag"), "datum": (r.get("date") or "")[:10],
            "url": f"https://oeffentlichevergabe.de/ui/de/search/details?noticeId={r.get('id')}",
            "api_eforms": f"https://oeffentlichevergabe.de/api/notices/{r.get('id')}?format=eforms",
            "auftraggeber": b.get("name"), "auftraggeber_ort": b.get("address", {}).get("locality"), "nuts": regs, "ausfuehrungsort": orte,
            "titel": t.get("title"), "beschreibung": (t.get("description") or "")[:1500],
            "lose": " | ".join(f"{l.get('title')}" for l in lots)[:1500],
            "los_details": [{"id": l.get("id"), "titel": l.get("title"), "wert": (l.get("value") or {}).get("amount"),
                             "start": (l.get("contractPeriod") or {}).get("startDate"), "ende": (l.get("contractPeriod") or {}).get("endDate")} for l in lots][:20],
            "cpv": cpv, "wert": (t.get("value") or {}).get("amount"), "verfahren": t.get("procurementMethodDetails"),
            "kategorie": t.get("mainProcurementCategory"), "unterlagen": list(dict.fromkeys(d.get("url") for d in t.get("documents", []) if d.get("url")))[:3],
            "zuschlaege": aw}

def run(start, end, outdir):
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    d = start
    while d <= end:
        day = d.isoformat(); tgt = outdir / f"{day}.jsonl"
        if not tgt.exists():
            raw = get(f"https://oeffentlichevergabe.de/api/notice-exports?pubDay={day}&format=ocds.zip")
            agg = collections.defaultdict(lambda: {"n": 0, "wert": 0.0}); n_all = n_reg = 0; cand = []
            if raw:
                with zipfile.ZipFile(io.BytesIO(raw)) as z:
                    for name in z.namelist():
                        try: rel = json.loads(z.read(name))["releases"][0]
                        except Exception: continue
                        n_all += 1; c = compact(rel)
                        land = next((x[:3] for x in c["nuts"] if x.startswith(NUTS)), None)
                        if not land: continue
                        n_reg += 1
                        ziel = [x for x in c["cpv"] if x and x.startswith(CPV_ZIEL)]
                        if ziel:
                            k = f"{land}|{ziel[0][:5]}|{'award' if 'award' in (c['tag'] or []) else 'tender'}"
                            agg[k]["n"] += 1
                            aw = sum((a["wert"] or 0) for a in c["zuschlaege"]); agg[k]["wert"] += aw or (c["wert"] or 0)
                        fit, s, m, neg = score(c)
                        if fit >= 12 or ziel:
                            c["fit"] = fit; c["treffer"] = s + m; c["land"] = land; cand.append(c)
            with open(tgt, "w") as f:
                for c in cand: f.write(json.dumps(c, ensure_ascii=False) + "\n")
            (outdir / f"{day}_agg.json").write_text(json.dumps({"tag": day, "alle": n_all, "region": n_reg, "agg": agg}, ensure_ascii=False))
            print(day, n_all, n_reg, len(cand), flush=True); time.sleep(1.0)
        d += dt.timedelta(days=1)

if __name__ == "__main__":
    run(dt.date.fromisoformat(sys.argv[1]), dt.date.fromisoformat(sys.argv[2]), sys.argv[3])
