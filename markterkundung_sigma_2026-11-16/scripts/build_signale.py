"""Baut 03b_signale.jsonl aus manuellen Signalen (work/signale_manuell_*.json) und neueroeffnung.info-Einträgen; bewertet nach Phase 4."""
import json, re, glob, sys, pathlib, datetime as dt
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from score import score_signal, HEUTE
MON = {"januar": 1, "februar": 2, "märz": 3, "april": 4, "mai": 5, "juni": 6, "juli": 7, "august": 8, "september": 9, "oktober": 10, "november": 11, "dezember": 12}
def termin_datum(t):
    """Schätzt ein Datum aus Freitext-Terminen (geschätzt = Quartals-/Halbjahresmitte)."""
    if not t: return None
    t = t.lower()
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", t)
    if m: return dt.date(int(m[3]), int(m[2]), int(m[1]))
    m = re.search(r"(\d)\.\s*quartal\s*(\d{4})", t) or re.search(r"q(\d)\s*/?\s*(\d{4})", t)
    if m: return dt.date(int(m[2]), int(m[1]) * 3 - 1, 15)
    m = re.search(r"(\d)\.\s*halbjahr\s*(\d{4})", t) or re.search(r"h(\d)\s*/?\s*(\d{4})", t)
    if m: return dt.date(int(m[2]), 4 if m[1] == "1" else 10, 1)
    for k, v in MON.items():
        m = re.search(k + r"\s*(\d{4})", t)
        if m: return dt.date(int(m[1]), v, 15)
    m = re.search(r"ostern\s*(\d{4})", t)
    if m: return dt.date(int(m[1]), 4, 1)
    m = re.search(r"(ende|spätsommer|herbst)\s*(\d{4})", t)
    if m: return dt.date(int(m[2]), 11 if m[1] == "ende" else 9, 1)
    m = re.search(r"(\d{4})", t)
    if m: return dt.date(int(m[1]), 7, 1)
    return None
ZENTRAL = re.compile(r"\b(lidl|aldi|netto|penny|norma|kaufland|globus|marktkauf|famila)\b", re.I)
LEH = re.compile(r"\b(edeka|rewe|nah ?& ?gut|e[- ]?center|konsum|bio|denn|alnatura|tegut|tante enso|nahkauf|cap|markant|hit|mein markt|dorfladen|hofladen)\b", re.I)
HAND = re.compile(r"bäck|baeck|back|konditor|fleisch|metzger|wurst|feinkost", re.I)
def zeitnaehe(d):
    if not d: return 6
    m = (d - HEUTE).days / 30.4
    if m < 0: return 2
    if m < 3: return 8
    if m <= 12: return 15
    if m <= 18: return 10
    return 5
def phase_aus_termin(d, typ):
    if typ == "Gerücht": return "Gerücht"
    if not d: return "Planung"
    m = (d - HEUTE).days / 30.4
    return "Eröffnung" if m < 2 else ("Bau" if m < 8 else ("Genehmigung" if m < 14 else "Planung"))
out = []; n = 0
for f in sorted(glob.glob("work/signale_manuell_*.json")):
    for s in json.load(open(f)):
        n += 1; s["id"] = f"C-M{n:03d}"; s["quelle"] = "Recherche (Presse/PM/Register)"
        d = termin_datum(s.get("termin")); s["termin_geschaetzt"] = d.isoformat() if d else None
        seg = s.get("segment") or 0
        segfit = 25 if seg in (1, 2, 4, 5) else (15 if seg in (3, 6) else (10 if seg in (7, 8) else 5))
        if ZENTRAL.search(s["organisation"]) and not LEH.search(s["organisation"]): segfit = 8
        if "Programm" in s["signal_typ"] or "Förderung (Frist)" in s["signal_typ"]: segfit = 25
        st = {"ST": 1, "BE": 1, "BB": 1, "SN": 2, "TH": 2, "NI": 2}.get((s.get("land") or "")[:2], 3)
        s["stufe"] = st
        vol = 15 if re.search(r"neubau|markthalle|programm", s["signal_typ"] + s["beschreibung"], re.I) else 10
        beleg = {"hoch": 15, "mittel": 11, "niedrig": 6}.get(s.get("vertrauensgrad"), 8)
        zug = {1: 10, 2: 7, 3: 4}[st] - (4 if segfit == 8 else 0)
        frische = bool(re.search(r"theke|frische|backshop|fleisch|bäck|o\+g|markthalle", s["beschreibung"], re.I))
        p, k = score_signal({"segment_fit": segfit, "projektphase": s.get("projektphase"), "beleg": beleg, "zeitnaehe": zeitnaehe(d), "monate_bis": ((d - HEUTE).days / 30.4) if d else None,
                             "volumen": vol, "zugang": zug, "bestandskunde": s.get("bestandskunde"), "frische": frische})
        if s.get("ko") or s["signal_typ"].startswith("Insolvenz (Wettbewerber)") or s["signal_typ"].startswith("Ansiedlung (entfallen)"):
            k = "Kontext"; p = None
        s.update({"score": p, "klasse": k}); out.append(s)
manual_keys = {(re.sub(r"\W", "", (s.get("ort") or "").lower())[:8], (LEH.search(s["organisation"]) or ZENTRAL.search(s["organisation"]) or HAND.search(s["organisation"]) or [""])[0].lower()) for s in out}
for l in open("raw/C/neueroeffnung_info/_entries.jsonl"):
    r = json.loads(l)
    if not r.get("land") or r["kategorie"] in ("shops",) or r["typ"] == "Schließung": continue
    t = r["titel"].replace("[NEU] ", "")
    if not (LEH.search(t) or ZENTRAL.search(t) or HAND.search(t) or re.search(r"café|cafe|markt", t, re.I)): continue
    d = termin_datum(r.get("eroeffnung"))
    if d and d < HEUTE - dt.timedelta(days=365): continue
    ort = t.split(" in ")[-1] if " in " in t else ""
    brand = (LEH.search(t) or ZENTRAL.search(t) or HAND.search(t) or [""])[0].lower()
    if (re.sub(r"\W", "", ort.lower())[:8], brand) in manual_keys: continue
    zentral = bool(ZENTRAL.search(t)) and not LEH.search(t)
    seg = 2 if HAND.search(t) else (1 if (LEH.search(t) or zentral) else 6)
    unbenannt = bool(re.match(r"^(bäckerei|supermarkt|gastronomie|café|cafe|fleischerei|metzgerei|lebensmittelmarkt|markt)\b", t, re.I))
    segfit = 8 if zentral else (18 if unbenannt else (25 if seg in (1, 2) else 15))
    typ = r["typ"]; phase = phase_aus_termin(d, typ)
    vol = 12 if (seg == 1 and typ == "Neueröffnung") else (9 if typ in ("Wiedereröffnung", "Umbau") else 6)
    if zentral: vol = 4
    zug = {1: 10, 2: 7, 3: 4}.get(r["stufe"], 2) - (4 if zentral else 0)
    beleg = (12 if (r.get("adresse") and r.get("eroeffnung")) else 9) - (4 if typ == "Gerücht" else 0)
    p, k = score_signal({"segment_fit": segfit, "projektphase": phase, "beleg": beleg, "zeitnaehe": zeitnaehe(d), "monate_bis": ((d - HEUTE).days / 30.4) if d else None, "volumen": vol, "zugang": max(0, zug),
                         "bestandskunde": False, "frische": seg == 2})
    n += 1
    out.append({"id": f"C-N{n:04d}", "signal_typ": typ, "segment": seg, "organisation": t, "betreiber": "zentral (Filialist)" if zentral else None,
                "ort": ort, "land": r["land"], "stufe": r["stufe"], "adresse_objekt": r.get("adresse"), "datum": r.get("abgerufen", "")[:10],
                "beschreibung": r["text"][:700], "projektphase": phase, "termin": r.get("eroeffnung"), "termin_geschaetzt": d.isoformat() if d else None,
                "verkaufsflaeche": None, "geschaetztes_volumen": None, "beleg_url": [r["url"]], "vertrauensgrad": "mittel (Aggregator)",
                "quelle": "neueroeffnung.info", "score": p, "klasse": k})
out.sort(key=lambda s: -(s["score"] or 0))
with open("03b_signale.jsonl", "w") as f:
    for s in out: f.write(json.dumps(s, ensure_ascii=False, default=str) + "\n")
import collections
print(len(out), collections.Counter(s["klasse"] for s in out), collections.Counter(s["stufe"] for s in out))
for s in out[:40]: print(s["score"], s["klasse"], s["stufe"], s["termin"], "|", s["organisation"][:70])
