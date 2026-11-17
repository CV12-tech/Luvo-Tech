"""Erzeugt markterkundung_sigma.xlsx (12 Tabs) aus den normalisierten Dateien."""
import json, re, glob, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter
HEUTE = dt.date(2026, 11, 17)
A = [json.loads(l) for l in open("03a_ausschreibungen.jsonl")]
S = [json.loads(l) for l in open("03b_signale.jsonl")]
C = [json.loads(l) for l in open("03c_accounts.jsonl")]
P = json.load(open("01_firmenprofil.json")); PRIV = json.load(open("work/privat.json"))
AKT = json.load(open("work/aktionen.json")); V = json.load(open("work/marktbild_volumen.json"))
SEGN = {0: "Wettbewerb/Partner", 1: "1 Kaufleute EDEKA/REWE", 2: "2 Bäckerei/Fleischerei", 3: "3 SB-Warenhaus", 4: "4 Nahversorger/Dorfladen", 5: "5 Bio", 6: "6 Gastro/Kantine", 7: "7 Projektentwickler", 8: "8 Tankstelle/Sonder", 9: "öffentlich sonstige"}
def seg(x): return SEGN.get(x, str(x)) if isinstance(x, int) else (x or "")
def d_de(s):
    if not s: return ""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})(.*)", str(s))
    return f"{m[3]}.{m[2]}.{m[1]}{m[4]}" if m else str(s)
def quartal(s):
    if not s: return "offen"
    y, mth = int(s[:4]), int(s[5:7]); return f"{y}-Q{(mth - 1) // 3 + 1}"
def aktion(name, typ=""):
    for k, v in AKT.items():
        if name.startswith(k[:30]) or k.startswith(name[:30]): return v
    if "Insolvenz" in typ: return "Inhaber/Sachwalter ansprechen; Nachnutzer der Standorte beobachten"
    if "Kaufmann" in typ: return "Neuen Kaufmann nach Übergabe ansprechen, Modernisierungsfahrplan anbieten"
    if typ in ("Neueröffnung", "Neubau"): return "Betreiber/Kaufmann ermitteln (Expansion der Regionalgesellschaft), Ausstattung anbieten"
    if typ in ("Wiedereröffnung", "Umbau"): return "Betreiber kontaktieren; Folgeumbau/Nachrüstung anbieten"
    if typ == "Gerücht": return "Beobachten (Ratsinfo/Presse)"
    return "Beobachten"
wb = Workbook(); wb.remove(wb.active)
HFILL = PatternFill("solid", fgColor="1F3864"); RED = PatternFill("solid", fgColor="F8CBAD")
def sheet(name, cols, rows, widths=None, link_cols=(), frist_col=None):
    ws = wb.create_sheet(name); ws.append(cols)
    for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows: ws.append([("; ".join(map(str, v)) if isinstance(v, (list, tuple)) else (json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else v)) for v in r])
    for ci in link_cols:
        for row in ws.iter_rows(min_row=2, min_col=ci, max_col=ci):
            c = row[0]; v = str(c.value or "")
            if v.startswith("http"): c.hyperlink = v.split("; ")[0]; c.font = Font(color="0563C1", underline="single")
    for i, w in enumerate(widths or [], 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
    if frist_col and ws.max_row > 1:
        L = get_column_letter(frist_col); rng = f"{L}2:{L}{ws.max_row}"
        ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND(ISNUMBER({L}2),{L}2-TODAY()<7)'], fill=RED))
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    return ws
def as_date(s):
    try: return dt.date.fromisoformat(str(s)[:10])
    except Exception: return None
# 1 Top-Chancen
top = []
for s in S:
    if s["klasse"] == "A" and (s["stufe"] in (1, 2) or s["score"] >= 85):
        top.append(("Signal", s["score"], s["klasse"], seg(s["segment"]), s["stufe"], s["organisation"], s["signal_typ"], s.get("ort"), s.get("termin"), None, aktion(s["organisation"], s["signal_typ"]), s["beleg_url"][0]))
for a in A:
    if not a["ko"] and a["klasse"] in ("A", "B") and a["score"] >= 63:
        top.append(("Ausschreibung", a["score"], a["klasse"], seg(a["segment"]), a["stufe"], a["auftraggeber"], (a["titel"] or "")[:120], a["ort"], None, as_date(a["angebotsfrist"]), (aktion(a["auftraggeber"] or "") if aktion(a["auftraggeber"] or "") != "Beobachten" else "Unterlagen über die Vergabeplattform laden (kostenlose Registrierung), Leistungsverzeichnis und Eignung prüfen, Go/No-Go bis 5 Werktage vor Frist; ggf. mit Partner (Großküchen-Fachhandel/Tischlerei)"), a["url"][0]))
for c in C:
    if c.get("klasse") == "A":
        top.append(("Account", c["score"], "A", seg(c["segment"]), None, c["organisation"], c["typ"], "; ".join((c.get("standorte") or [])[:3]), None, None, aktion(c["organisation"]), (c.get("beleg_url") or [""])[0] if c.get("beleg_url") else c.get("website")))
top.sort(key=lambda r: -(r[1] or 0))
ws = sheet("Top-Chancen", ["Art", "Score", "Klasse", "Segment", "Stufe", "Organisation/Auftraggeber", "Typ/Titel", "Ort", "Termin", "Angebotsfrist", "Nächste Aktion", "Beleg"], top,
           [13, 7, 7, 22, 6, 40, 40, 22, 16, 12, 70, 45], link_cols=(12,), frist_col=10)
for row in ws.iter_rows(min_row=2, min_col=10, max_col=10):
    row[0].number_format = "DD.MM.YYYY"
# 2 Projekt-Pipeline
pip = [(quartal(s.get("termin_geschaetzt")), s["id"], s["score"], s["klasse"], seg(s["segment"]), s["stufe"], s.get("land"), s["organisation"], s["signal_typ"], s["projektphase"], s.get("termin"),
        s.get("termin_geschaetzt") and d_de(s["termin_geschaetzt"]) + " (geschätzt)", s.get("adresse_objekt"), s.get("verkaufsflaeche"), s.get("geschaetztes_volumen"), (s.get("beschreibung") or "")[:400],
        s.get("quelle"), s.get("vertrauensgrad"), s["beleg_url"][0]) for s in S if s["klasse"] != "Kontext"]
pip.sort(key=lambda r: (r[0], -(r[2] or 0)))
sheet("Projekt-Pipeline", ["Quartal", "ID", "Score", "Klasse", "Segment", "Stufe", "Land", "Objekt/Organisation", "Signaltyp", "Projektphase", "Termin (Quelle)", "Termin (geschätzt)", "Adresse Objekt",
      "VK m²", "Volumen (geschätzt)", "Beschreibung", "Quelle", "Vertrauen", "Beleg"], pip, [10, 9, 6, 6, 20, 6, 6, 40, 16, 12, 16, 16, 30, 7, 22, 60, 18, 12, 45], link_cols=(19,))
# 3 Öffentlich
pub = [(a["id"], a["score"], a["klasse"], "; ".join(a["ko"]), seg(a["segment"]), a["stufe"], a["auftraggeber"], a["titel"], a["ort"], a["nuts"], a["cpv"], a["verfahrensart"], a["geschaetzter_wert"],
        d_de(a["veroeffentlicht_am"]), as_date(a["angebotsfrist"]), a["werktage_bis_frist"], a["zugangsweg"], a["unterlagen_url"], (a["kurzbeschreibung"] or "")[:400], a["url"][0]) for a in A]
ws = sheet("Öffentlich", ["ID", "Score", "Klasse", "K.-o.", "Segment", "Stufe", "Auftraggeber", "Titel", "Ort", "NUTS", "CPV", "Verfahren", "Wert (€)", "Veröffentlicht", "Angebotsfrist", "Werktage bis Frist",
           "Zugang", "Unterlagen", "Kurzbeschreibung", "Bekanntmachung"], pub, [14, 6, 6, 22, 18, 6, 32, 45, 18, 8, 18, 14, 10, 12, 12, 8, 25, 40, 60, 45], link_cols=(18, 20), frist_col=15)
for row in ws.iter_rows(min_row=2, min_col=15, max_col=15): row[0].number_format = "DD.MM.YYYY"
# 4 Privat
sheet("Privat", ["Segment", "Stufe", "Titel", "Organisation", "Art", "Zugang", "Status", "Score", "Klasse", "Link"],
      [(seg(p["segment"]), p["stufe"], p["titel"], p["organisation"], p["art"], p["zugang"], p["status"], p["score"], p["klasse"], p["url"]) for p in PRIV], [18, 6, 55, 30, 20, 40, 30, 7, 7, 50], link_cols=(10,))
# 5 Zielkunden
zk = [c for c in C if c["typ"].startswith("Zielkunde")]
sheet("Zielkunden", ["Score", "Klasse", "Segment", "Organisation", "Typ", "Filialen (OSM, Untergrenze)", "davon Stufe 1", "Länder", "Top-Standorte", "Umbaubedarf (geschätzt)", "Einkaufsweg", "Entscheiderrolle",
      "Bestandskunde", "Verknüpfte Signale", "Website", "Beleg"],
      [(c["score"], c["klasse"], seg(c["segment"]), c["organisation"], c["typ"], c.get("filialen_anzahl"), c.get("filialen_stufe1"), c.get("laender"), (c.get("standorte") or [])[:5], c.get("umbaubedarf_geschaetzt"),
        c.get("einkaufsweg"), c.get("entscheiderrolle"), "ja" if c.get("bestandskunde") else "", c["verknuepfte_signale_ids"], c.get("website"), (c.get("beleg_url") or [""])[0]) for c in zk],
      [6, 6, 20, 38, 14, 10, 8, 22, 35, 30, 28, 22, 8, 18, 30, 45], link_cols=(15, 16))
# 6 Bestandskunden-Potenzial
ref = ["Steinecke", "Halberstädter", "Ihr Landbäcker", "Altmärker", "Schäfer's", "EDEKA Minden", "BIO COMPANY", "Steinecke"]
bk = []
for c in C:
    if c.get("bestandskunde"):
        sig = [s for s in S if s["id"] in c["verknuepfte_signale_ids"]]
        bk.append((seg(c["segment"]), c["organisation"], c.get("filialen_anzahl") or c.get("filialen_hinweis"), c.get("filialen_stufe1"), (c.get("standorte") or [])[:6], "; ".join(s["organisation"] for s in sig)[:300], aktion(c["organisation"]), (c.get("beleg_url") or [""])[0]))
for s in S:
    if s.get("bestandskunde") and not any(s["organisation"][:15] in b[5] for b in bk):
        bk.append((seg(s["segment"]), s["organisation"], None, None, s.get("ort"), s["signal_typ"] + ": " + s["beschreibung"][:200], aktion(s["organisation"], s["signal_typ"]), s["beleg_url"][0]))
bk += [("1 Kaufleute EDEKA/REWE", "Referenzmärkte EDEKA MH (Wernigerode E-Center, Schatz Bad Lauchstädt, Stenschke Köthen [2 Standorte], Dorbritz Gardelegen, Hinze Naumburg)", 6, 6, "ST",
        "Bestandsmärkte – Nachrüstung (Kältetausch/BAFA bis 31.12.2026), Backshop-/Thekenmodernisierung; Kaufleute mit weiteren Standorten", "Kaufleute-Tour Q1/2027: Bestandsaufnahme Theken/Kühlmöbel, BAFA-Antrag vorbereiten", "https://www.sigma-ladenbau.de/projekte"),
       ("4 Nahversorger/Dorfladen", "nah&gut-Referenzen (Arendsee, Tangermünde, Zerbst) + weitere NAH&GUT-Kaufleute Börde (OSM: Homeyer, Achtenicht, Grave, Müller, Krzos)", 32, 20, "ST/BB",
        "NP-Umstellungswelle; Kaufleute mit 2+ Märkten", "Referenzbesuch anbieten; Rest-NP-Märkte in ST/BB über EDEKA MH identifizieren", "https://www.sigma-ladenbau.de/projekte")]
sheet("Bestandskunden-Potenzial", ["Segment", "Kunde/Gruppe", "Filialen (gesamt)", "davon Stufe 1", "Standorte", "Signale/Anlässe", "Nächste Aktion", "Beleg"], bk, [20, 45, 10, 8, 35, 70, 60, 45], link_cols=(8,))
# 7 Wettbewerber
sheet("Wettbewerber", ["Segment", "Wettbewerber", "Typ", "Positionierung/Notiz", "Website", "Beleg"],
      [(seg(c["segment"]), c["organisation"], c["typ"], c.get("notiz"), c.get("website"), (c.get("beleg_url") or [""])[0]) for c in C if c["typ"].startswith("Wettbewerber")] +
      [("öffentlich sonstige", g, "Zuschlagsempfänger TED (Mensa/Kantine/Einbau 2021–2026)", f"{n} relevante Zuschläge", "", "") for g, n in __import__("collections").Counter(
          x for r in json.load(open("raw/A/ted/zuschlaege_relevant.json")) for x in (r["gewinner"] or "").split("; ") if x).most_common(20)],
      [18, 45, 28, 70, 30, 45], link_cols=(5, 6))
# 8 Wiederausschreibungen
wa = []
for r in json.load(open("raw/A/ted/zuschlaege_relevant.json")):
    lz = r.get("laufzeit"); rahmen = bool(re.search(r"rahmen", (r["titel"] or "") + (r["beschreibung"] or ""), re.I))
    pub = r["veroeffentlicht"]; y = int(pub[:4])
    if rahmen and isinstance(lz, dict) and lz.get("unit") == "MONTH": prog = f"{d_de(pub)} + {lz['value']} Mon. → Neuausschreibung ca. {y + int(lz['value']) // 12} (geschätzt)"
    elif rahmen: prog = f"Rahmenvertrag – Neuausschreibung ca. {y + 4} (geschätzt, Standardlaufzeit 4 J.)"
    else: prog = f"Einmalbeschaffung – Ersatz/Modernisierung ca. {y + 12} (geschätzt, Nutzungsdauer 10–15 J.); Folgegeschäft Nachrüstung"
    wa.append(("6 Gastro/Kantine" if re.search(r"mensa|kantine|küche|speise", (r["titel"] or ""), re.I) else "öffentlich sonstige", r["auftraggeber"], r["titel"], r["ort"], d_de(pub), r["gewinner"], r["wert_gesamt"], lz, prog, r["url"]))
wa.sort(key=lambda x: x[8])
sheet("Wiederausschreibungen", ["Segment", "Auftraggeber", "Titel", "Ort", "Zuschlag veröffentlicht", "Gewinner", "Wert (€)", "Laufzeit", "Prognose Wiederausschreibung", "Bekanntmachung"], wa, [18, 32, 55, 16, 12, 35, 12, 15, 55, 45], link_cols=(10,))
# 9 Partner
partner = [(seg(c["segment"]), c["organisation"], c["typ"], c.get("notiz"), c.get("website"), (c.get("beleg_url") or [""])[0]) for c in C if c["typ"].startswith("Partner") or "Partner" in c["typ"]]
partner += [("6 Gastro/Kantine", "Großküchen-Fachhandel (Chefs Culinar Nord-Ost/Ost, Kunkel, KPC, Emmerich, Neltner)", "Partner öffentlicher Sektor (empfohlen)", "Bieten Mensa-/Kantinenküchen; SIGMA als Nachunternehmer für Ausgabe-/Thekenbereiche", "", ""),
            ("Wettbewerb/Partner", "Kältefachbetriebe in ST/BB (zu ermitteln)", "Partner Kälte (Lücke)", "Für BAFA-/F-Gas-Umbauten notwendig; keine belegten Partner gefunden", "", ""),
            ("Wettbewerb/Partner", "Ex-Mitarbeitende HANSE Ladenbau (Projektleitung/Montage Rostock, Berlin, Magdeburg)", "Personal/Projektleiter Nord", "Nur über Insolvenzverwaltung bzw. öffentliche Stellenanzeigen ansprechen (DSGVO)", "", "https://insolvenz-radar.de/firmeninsolvenz/hrb+5836/kavelstorf/n1206/"),
            ("Wettbewerb/Partner", "Liebherr Kühlmöbel-Service (Aufbereitung gebrauchter Kühlmöbel)", "Partner Kühlmöbel/Kreislauf", "EHI: im Schnitt 50 % der Einrichtung wird nach Umbau weiterverwendet", "", "https://www.lzdirekt.de/stores/news/studie-ehi-ladenbau-2693")]
sheet("Partner", ["Segment", "Partner", "Rolle", "Notiz", "Website", "Beleg"], partner, [18, 50, 30, 70, 30, 45], link_cols=(5, 6))
# 10 Marktbild
ob = V["ov_bereinigt"]
mb = [("Markt", "Ladenbau-Investitionen Einzelhandel DE 2025", "7,02 Mrd €", "−23 % ggü. Studie 2023", "EHI Laden-Monitor 2026", "https://www.lzdirekt.de/stores/news/studie-ehi-ladenbau-2693"),
      ("Markt", "Investition je m² VK – neue LEH-Märkte bis 2.500 m²", "961 €/m²", "+13 % ggü. 2022", "EHI Laden-Monitor 2026", "https://retail-news.de/laden-monitor-2026-ehi/"),
      ("Markt", "Investition je m² VK – LEH-Märkte ab 2.500 m²", "711 €/m²", "+5 % in 3 Jahren", "EHI Laden-Monitor 2026", "https://retail-news.de/laden-monitor-2026-ehi/"),
      ("Markt", "Investitionsschwerpunkt LEH", "Kältetechnik (F-Gas-VO)", "50 % Weiterverwendung nach Umbau", "EHI", "https://rundschau.de/studie/fokus-auf-kaeltetechnik-praegt-investitionen/"),
      ("Handwerk", "Betriebe Bäckerhandwerk DE 2025", "8.659", "−2,8 % (Vorjahr 8.912; 2015: 12.155); 448 Neugründungen", "ZV Bäckerhandwerk", "https://www.baeckerhandwerk.de/zahlen-fakten"),
      ("Handwerk", "Betriebsstätten Fleischerhandwerk DE 2024", "15.809", "−2,9 %", "DFV Jahrbuch 2025", "https://www.fleischerhandwerk.de/fileadmin/fleischerhandwerk/03_Presse/DFV_Jahrbuch_2025.pdf"),
      ("Handwerk", "Fleischereien (Schwerpunkt Verkauf) Sachsen", "206", "−1/3 in 10 Jahren", "Sachsen Fernsehen 10/2026", "https://www.sachsen-fernsehen.de/amp/zahl-der-fleischereien-in-sachsen-sinkt-deutlich-2302755/"),
      ("Handwerk", "Bäckereibetriebe Sachsen-Anhalt", "≈ −1/3 in 10 Jahren", "", "Hans-Böckler-Stiftung/NGG (lt. Presse)", "https://www.berliner-zeitung.de/article/baeckermeister-aus-sachsen-anhalt-backt-mit-85-jahren-weiter-10524269"),
      ("Handwerk", "Bäckerei-Insolvenzen H1/2026 bundesweit", "63", "", "Creditreform (lt. Presse)", "https://ms-aktuell.de/welt/lebensmittel-insolvenzen-29-08-2026/"),
      ("Arbeitsmarkt", "Unbesetzte Stellen Fleischfachverkauf 2025", "≈ 4.600", "Höchstwert – Treiber Hybrid-/SB-Theken", "KOFA lt. Lebensmittel Praxis", "https://lebensmittelpraxis.de/handel-aktuell/48114-bedientheken-fachkraefteluecke-bei-fleischfachverkaeufern-am-groessten.html"),
      ("Regulierung", "BAFA Kälte-Klima-Richtlinie", "Antragsschluss 31.12.2026", "Umsetzung binnen 2 J.; kein vorzeitiger Maßnahmenbeginn", "BMUKN", "https://www.bundesumweltministerium.de/meldung/energieeffiziente-kaelte-und-klimaanlagen-werden-gefoerdert-bis-ende-2026"),
      ("Regulierung", "F-Gase-VO (EU) 2024/573", "Stufenweise Verbote 2025/2027/2030/2032", "Steckerfertige Geräte GWP≥150 ab 2025; Fristen je Anlagentyp in Anhang IV prüfen", "EUR-Lex / DUH", "https://eur-lex.europa.eu/eli/reg/2024/573/oj"),
      ("Struktur", "EDEKA Minden-Hannover", "ca. 1.500 Märkte, ca. 640 selbstständige Kaufleute", "Gebiet Ostfriesland–ST–BE–BB", "EDEKA MH", "https://verbund.edeka/minden-hannover/presse/"),
      ("Struktur", "NP-Umstellung EDEKA MH", "ca. 330 Märkte bis 2026", "2/3 nah&gut, 1/3 EDEKA", "Supermarkt Inside", "https://www.supermarkt-inside.de/edeka-macht-schluss-mit-np/"),
      ("Struktur", "tegut-Zerschlagung", "EDEKA 178+, REWE 44, Tante Enso 36 Märkte", "Kartellamt 06–11/2026", "Bundeskartellamt", "https://www.bundeskartellamt.de/SharedDocs/Meldung/DE/Pressemitteilungen/2026/11_12_2026_REWE_tegut.html"),
      ("Struktur", "Aichinger (Thekenhersteller) gehört zur EDEKA-Gruppe", "seit 2025", "Umsatz 2024 74,4 Mio €", "Fleisch&Co / Wikipedia", "https://fleischundco.at/info-politik/breaking-news-edeka-uebernimmt-ladenbau-spezialisten-aichinger"),
      ("Struktur", "Brandenburg: 24/7-Smart-Stores (Ladenöffnung)", "Gesetzesänderung geplant", "ST hat bereits Regeln", "Lebensmittel Praxis", "https://lebensmittelpraxis.de/handel-aktuell/46042-smart-stores-brandenburg-plant-rund-um-die-uhr-oeffnung-fuer-automatische-supermaerkte.html")]
osm = json.load(open("work/osm_laender.json")) if glob.glob("work/osm_laender.json") else {}
for l, v in osm.items(): mb.append(("Standorte (OSM, Untergrenze)", f"Lebensmittelgeschäfte {l}", f"Supermärkte {v['supermarket']} · Bäckereien {v['bakery']} · Fleischereien {v['butcher']}", "nur Objekte mit PLZ-Tag", "OpenStreetMap (ODbL)", "https://download.openstreetmap.fr/extracts/europe/germany-latest.osm.pbf"))
for l, v in ob.items(): mb.append(("Öffentliche Beschaffung (eigene Berechnung)", f"Zuschläge Ziel-CPV {l} 12/2023–11/2026", f"{v['zuschlaege']} Zuschläge; Summe (mit Wert, ≤5 Mio) {v['summe_mio']} Mio €", f"nur {v['mit_wert']} mit Wert; Median {v['median_teur']} T€; {v['ausreisser_gt5mio']} Ausreißer >5 Mio ausgeschlossen", "oeffentlichevergabe.de (OCDS)", "https://oeffentlichevergabe.de"))
for j, v in sorted(V["ov_bereinigt_jahr"].items()): mb.append(("Öffentliche Beschaffung (eigene Berechnung)", f"Zuschläge Ziel-CPV 11 Länder {j}", f"{v['n']} mit Wert · {round(v['wert'] / 1e6, 1)} Mio €", "bereinigt", "oeffentlichevergabe.de", "https://oeffentlichevergabe.de"))
for j, v in sorted(V["ted_zuschlaege_jahr"].items()): mb.append(("Öffentliche Beschaffung (eigene Berechnung)", f"TED-Zuschläge Ziel-CPV 11 Länder {j}", f"{v['n']} · {round(v['wert'] / 1e6, 1)} Mio € (unbereinigt)", "enthält Gesamtwerte von Bauaufträgen", "TED API v3", "https://api.ted.europa.eu"))
sheet("Marktbild", ["Bereich", "Kennzahl", "Wert", "Anmerkung", "Quelle", "Link"], mb, [26, 50, 45, 50, 28, 50], link_cols=(6,))
# 11 Quellen-Log
ql = []
for idx in glob.glob("raw/**/_index.tsv", recursive=True):
    for l in open(idx):
        ts, url, f = l.rstrip("\n").split("\t"); ql.append((idx.split("/")[1], idx.split("/")[2], ts, url, f"{idx.rsplit('/', 1)[0]}/{f}", "HTTP-Abruf"))
ql += [("A", "TED API v3", "16.11.2026", "https://api.ted.europa.eu/v3/notices/search", "raw/A/ted/", "offizielle API – 744 Bekanntmachungen (90 T), 5.835 Zuschläge (5 J.)"),
       ("A", "oeffentlichevergabe.de", "16.–17.11.2026", "https://oeffentlichevergabe.de/api/notice-exports", "raw/A/oeffentlichevergabe/", "offizielle API – 1.081 Tagesexporte, 876.421 Bekanntmachungen, davon 415.822 in Region"),
       ("C", "neueroeffnung.info", "16.11.2026", "https://www.neueroeffnung.info", "raw/C/neueroeffnung_info/_entries.jsonl", "öffentliche Detailseiten (robots.txt beachtet; Listen ab Seite 2 Premium – nicht genutzt)"),
       ("D", "OpenStreetMap", "16.11.2026", "https://download.openstreetmap.fr/extracts/europe/germany-latest.osm.pbf", "raw/D/osm/shops_nord_mitte.jsonl", "Datenexport; Overpass/Geofabrik aus Rechenzentrum nicht erreichbar"),
       ("D", "OpenPLZ API", "16.11.2026", "https://openplzapi.org", "raw/_plz_land_full.json", "PLZ→Land/Kreis"),
       ("alle", "WebSearch (Suchindex)", "16.11.2026", "", "raw/phase1/websearch/", "Belege aus Index-Auszügen; Primärquelle nicht immer abgerufen"),
       ("1", "sigma-ladenbau.de", "16.11.2026", "https://www.sigma-ladenbau.de", "", "BLOCKIERT: TLS-Reset durch Server – nur Suchindex-Auszüge")]
sheet("Quellen-Log", ["Modul", "Quelle", "Zeitstempel", "URL", "Rohdatei", "Zugriff/Bemerkung"], ql, [8, 22, 18, 70, 50, 60], link_cols=(4,))
# 12 Firmenprofil
fp = [("Stammdaten", k, v) for k, v in P["stammdaten"].items()]
for k in ("kurzbeschreibung", "wertversprechen", "realistische_auftragsgroesse", "freigabe"): fp.append(("Profil", k, P.get(k)))
fp += [("Alleinstellung", a["aussage"], a["status"]) for a in P["alleinstellungsmerkmale"]]
fp += [("Leistung", l, "") for l in P["kernleistungen"]] + [("Referenz", r["projekt"], seg(r["segment"])) for r in P["referenzprojekte_belegt"]]
fp += [("Korrektur", c, "") for c in P["korrekturen_gegenueber_vorabprofil"]] + [("Offener Punkt", o, "") for o in P["offene_punkte"]]
fp += [("Partner", p["name"], p["rolle"]) for p in P["partner_und_gewerke"]] + [("NUTS", k, v) for k, v in P["nuts_regionen"].items()]
fp += [("CPV", c["code"] + " " + c["bez"], c["konfidenz"]) for c in P["cpv_codes"]]
fp.append(("Offener Punkt", "Referenz 'Lüning': Lüning Ladenbau GmbH (Langenberg) ist dLv-Mitglied – evtl. Partner statt Bäckerei", "dLv-Mitgliederliste 2026"))
sheet("Firmenprofil", ["Bereich", "Merkmal", "Wert/Status"], [(a, b, c if not isinstance(c, (dict, list)) else json.dumps(c, ensure_ascii=False)) for a, b, c in fp], [18, 70, 70])
# Segment-Spalte in Tabs ohne Segment? alle haben Segment außer Quellen-Log/Firmenprofil (Meta)
wb.save("markterkundung_sigma.xlsx"); print("ok", [ws.title for ws in wb.worksheets], len(top))
