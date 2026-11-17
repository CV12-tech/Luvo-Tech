"""PLZ → Bundesland/Landkreis über OpenPLZ API (openplzapi.org), mit Datei-Cache; Stufe gemäß 02a."""
import json, time, pathlib, urllib.request
CACHE = pathlib.Path(__file__).resolve().parent.parent / "raw" / "_plz_cache.json"
_c = json.loads(CACHE.read_text()) if CACHE.exists() else {}
_FULL = pathlib.Path(__file__).resolve().parent.parent / "raw" / "_plz_land_full.json"
_full = json.loads(_FULL.read_text()) if _FULL.exists() else {}
_KZ = {"ST": "Sachsen-Anhalt", "BE": "Berlin", "BB": "Brandenburg", "SN": "Sachsen", "TH": "Thüringen", "NI": "Niedersachsen", "MV": "Mecklenburg-Vorpommern", "HH": "Hamburg", "SH": "Schleswig-Holstein", "HB": "Bremen", "HE": "Hessen"}
KUERZEL = {"Sachsen-Anhalt": "ST", "Berlin": "BE", "Brandenburg": "BB", "Sachsen": "SN", "Thüringen": "TH", "Niedersachsen": "NI",
           "Mecklenburg-Vorpommern": "MV", "Hamburg": "HH", "Schleswig-Holstein": "SH", "Bremen": "HB", "Hessen": "HE"}
STUFE = {"ST": 1, "BE": 1, "BB": 1, "SN": 2, "TH": 2, "NI": 2, "MV": 3, "HH": 3, "SH": 3, "HB": 3, "HE": 3}
NI_OST_KREISE = ("Region Hannover", "Braunschweig", "Wolfsburg", "Salzgitter", "Gifhorn", "Helmstedt", "Peine", "Wolfenbüttel", "Goslar",
                 "Hildesheim", "Celle", "Uelzen", "Lüchow-Dannenberg", "Göttingen", "Northeim", "Holzminden", "Schaumburg", "Hameln-Pyrmont", "Nienburg")
def vorfilter(plz):  # grober Ausschluss von NRW/Süd
    return bool(plz) and len(plz) == 5 and plz[0] in "01236789" and not plz.startswith(("32", "33", "40", "41", "42", "44", "45", "46", "47", "48", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "66", "67", "68", "69", "7", "8", "90", "91", "92", "93", "94", "95", "96", "97"))
def lookup(plz):
    if not plz or len(plz) != 5: return None
    if plz in _full: v = _full[plz]; return {"land": _KZ[v["land"]], "kreis": v["kreis"] or "", "orte": v["orte"]}
    if _full: return None   # Volltabelle vorhanden: PLZ liegt außerhalb der 11 Länder
    if plz not in _c:
        try:
            with urllib.request.urlopen(f"https://openplzapi.org/de/Localities?postalCode={plz}", timeout=20) as r: d = json.load(r)
            _c[plz] = {"land": d[0]["federalState"]["name"], "kreis": d[0]["district"]["name"], "orte": [x["name"] for x in d]} if d else None
        except Exception:
            return None
        CACHE.write_text(json.dumps(_c, ensure_ascii=False)); time.sleep(0.3)
    return _c[plz]
def land(plz):
    x = lookup(plz); return KUERZEL.get(x["land"]) if x else None
def stufe(l, plz=None):
    s = STUFE.get(l)
    if l == "NI":
        x = lookup(plz); return 2 if x and any(k in x["kreis"] for k in NI_OST_KREISE) else 3
    return s
