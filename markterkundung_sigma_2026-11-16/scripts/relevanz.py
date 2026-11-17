"""Relevanzfilter für Ausschreibungen (Leistungs-Fit SIGMA). Gibt fit 0–30 und Begründung zurück."""
import re
STRONG = [r"ladenbau", r"ladeneinrichtung", r"ladenausbau", r"bedienthek", r"frischethek", r"kühlthek", r"thekenanlage",
          r"ausgabethek", r"ausgabeanlage", r"speisenausgabe", r"essensausgabe", r"free[- ]?flow", r"backshop", r"verkaufsthek",
          r"shop[- ]?einrichtung", r"museumsshop", r"cafeteria", r"kassenzone", r"dorfladen", r"markthalle", r"\bthek(e|en)\b",
          r"kioskeinrichtung", r"buffet(anlage)?", r"salatbar", r"tresen", r"bistro", r"mensa-?(ausstattung|einrichtung|möbel|küche|ausgabe)", r"betriebsrestaurant", r"kälteanlagen gastro"]
MEDIUM = [r"mensa", r"einbaumöbel", r"möblierung", r"innenausbau", r"innenausstattung", r"küchenausstattung", r"großküche", r"gastronomie",
          r"kantine", r"betriebsrestaurant", r"speiseraum", r"speisesaal", r"kühlmöbel", r"kühlzelle", r"verkaufsraum", r"kiosk",
          r"cafébereich", r"\bcafe\b|\bcafé\b", r"ausstellungsmöbel", r"tischlerarbeiten", r"küche"]
NEG = [r"speiseversorgung", r"mittagsversorgung", r"verpflegungsleistung", r"essensversorgung", r"schulverpflegung", r"catering",
       r"belieferung mit (mittag)?essen", r"reinigung", r"wachschutz", r"rohbau", r"fenster", r"türen\b|\btüren", r"fassade",
       r"schulmöbel", r"labormöbel", r"büromöbel", r"dach", r"tiefbau", r"estrich", r"bodenbelag", r"trockenbau", r"brandschutz",
       r"wartung", r"elektro", r"heizung", r"sanitär", r"aufzug", r"gerüst", r"maler", r"fliesen", r"metallbau", r"stahlbau"]
def score(r):
    t = " ".join(str(r.get(k) or "") for k in ("titel", "lose", "beschreibung")).lower()
    tl = " ".join(str(r.get(k) or "") for k in ("titel", "lose")).lower()
    s = [p for p in STRONG if re.search(p, t)]; m = [p for p in MEDIUM if re.search(p, t)]
    n = [p for p in NEG if re.search(p, tl)]
    fit = min(30, 12 * len(s) + 4 * len(m)) - 8 * len(n)
    if re.search(r"konzession|bewirtschaftung|betreiber|pächter|verpachtung|betreuungsleistung", tl): fit = min(fit, 4)
    if re.search(r"lüftung|elektro|elt-|gebäudeautomation|starkstrom|schwachstrom|putz|wdvs|zimmerer|schlosser|leitungsbau|maurer|planungsleistung|tga|akustik|trennwand|trennvorhang|parking|medien- und bühnen", tl) and not re.search(r"ladenbau|thek|tresen|ausgabe|möbl|einbaumöbel|küche", tl): fit = min(fit, 4)
    if re.search(r"(mensa|cafeteria|speise|betriebsrestaurant|kantine|bistro|kiosk).{0,80}(möbl|küche|ausstattung|einrichtung|tischler|ausgabe)|(möbl|küche|ausstattung|einrichtung|tischler|ausgabe).{0,80}(mensa|cafeteria|speise|betriebsrestaurant|kantine|bistro|kiosk)", tl): fit = max(fit, 24)
    if re.search(r"ingenieurleistung|objektplanung|tragwerksplanung|architektenleistung", tl): fit = min(fit, 8)
    if re.search(r"(speise|mittags|schul)versorgung|verpflegung|catering", tl) and not re.search(r"thek|ausgabe|einrichtung|ausstattung", tl): fit = 0
    return max(0, fit), s, m, n
