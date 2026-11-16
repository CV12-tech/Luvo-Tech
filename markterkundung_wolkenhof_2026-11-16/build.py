#!/usr/bin/env python3
"""build.py – normalisiert raw/*.jsonl, bewertet (Phase 4) und erzeugt 03a/03b/03c + Excel."""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

BASE = Path(__file__).resolve().parent
TODAY = dt.date(2026, 11, 16)
PROFILE = json.loads((BASE / "01_firmenprofil.json").read_text(encoding="utf-8"))
PROFILE_CPV = {c["code"] for c in PROFILE["cpv_codes"]}

KERN = ["uelzen", "lüneburg", "lueneburg", "celle", "gifhorn", "heidekreis", "soltau", "walsrode", "fallingbostel",
        "munster", "lüchow", "luechow", "dannenberg", "wendland", "harburg", "winsen", "buchholz", "seevetal", "tostedt",
        "bardowick", "bad bevensen", "ebstorf", "suderburg", "wittingen", "rosengarten", "bispingen", "schneverdingen",
        "hermannsburg", "bergen", "adendorf", "reppenstedt", "dahlenburg", "bleckede", "amelinghausen", "scharnebeck",
        "rosche", "bienenbüttel", "hankensbüttel", "meinersen", "sassenburg", "neu wulmstorf", "hollenstedt", "jesteburg",
        "salzhausen", "stelle", "hanstedt", "de93", "de917"]
ERW = ["hamburg", "hannover", "braunschweig", "wolfsburg", "salzwedel", "stendal", "altmark", "schwerin", "ludwigslust",
       "parchim", "wismar", "nordwestmecklenburg", "bremen", "peine", "wolfenbüttel", "helmstedt", "geesthacht",
       "lauenburg", "stade", "garbsen", "langenhagen", "de60", "de92", "de91", "dee0", "de80", "de50"]
NEG = [k.lower() for k in PROFILE["negativ_keywords"]]


def read_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def s(v) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return "; ".join(s(x) for x in v)
    if isinstance(v, dict):
        return "; ".join(f"{k}: {s(x)}" for k, x in v.items())
    return str(v)


def as_list(v) -> list:
    if v in (None, ""):
        return []
    return v if isinstance(v, list) else [v]


def parse_date(v) -> dt.date | None:
    m = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", s(v))
    if m:
        try:
            return dt.date(int(m[3]), int(m[2]), int(m[1]))
        except ValueError:
            return None
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s(v))
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    return None


def region(text: str) -> str:
    t = text.lower()
    if any(k in t for k in KERN):
        return "kern"
    if any(k in t for k in ERW):
        return "erweitert"
    return "sonstige"


def parse_eur(v) -> float | None:
    t = s(v).lower().replace("€", "").replace("eur", "")
    m = re.search(r"(\d[\d\.\s]*(?:,\d+)?)\s*(mio|millionen|t|tsd|k)?", t)
    if not m:
        return None
    num = m[1].replace(" ", "").replace(".", "").replace(",", ".")
    try:
        val = float(num)
    except ValueError:
        return None
    unit = m[2] or ""
    if unit.startswith("mio") or unit.startswith("million"):
        val *= 1e6
    elif unit in ("t", "tsd", "k"):
        val *= 1e3
    return val


def quarter(d: dt.date | None) -> str:
    return f"Q{(d.month - 1) // 3 + 1}/{d.year}" if d else ""


def workdays_until(d: dt.date) -> int:
    n, cur = 0, TODAY
    while cur < d:
        cur += dt.timedelta(days=1)
        if cur.weekday() < 5:
            n += 1
    return n


# ---------- Bewertung Ausschreibungen ----------
def score_tender(t: dict) -> tuple[int, str, list[str], dict]:
    felder = [f for f in re.split(r"[+,/; ]+", s(t.get("geschaeftsfeld")).lower()) if f]
    text = " ".join(s(t.get(k)) for k in ("titel", "kurzbeschreibung", "eignungskriterien", "zuschlagskriterien", "los_info")).lower()
    ko = []
    parts = {}
    neg_hit = any(n in text for n in NEG)
    parts["fit"] = 0 if neg_hit else (30 if felder else 12)
    reg = region(" ".join(s(t.get(k)) for k in ("ort", "nuts", "auftraggeber")))
    if reg == "kern":
        parts["region"] = 15
    elif reg == "erweitert":
        parts["region"] = 9
    else:
        parts["region"] = 6 if "greencloud" in felder else 2
    elig = 16
    if re.search(r"iso\s*27001|bsi\s*c5|iso/iec\s*27001", text):
        elig = 4
        ko.append("ISO 27001/C5 gefordert")
    if re.search(r"mindestumsatz|jahresumsatz von mindestens", text):
        elig -= 4
        ko.append("Mindestumsatz prüfen")
    if re.search(r"präqualifi", text):
        elig -= 2
    if re.search(r"24/7|24x7|rund um die uhr", text):
        elig -= 3
    parts["eignung"] = max(elig, 0)
    val = parse_eur(t.get("geschaetzter_wert"))
    if val is None:
        parts["groesse"] = 6
    elif val < 10000:
        parts["groesse"] = 2
    elif val <= 750000:
        parts["groesse"] = 10
    elif val <= 2000000:
        parts["groesse"] = 6
    else:
        parts["groesse"] = 2
        ko.append("Volumen > 2 Mio. € → nur Los/BIEGE")
    nk = s(t.get("nachhaltigkeitskriterien")).strip()
    parts["nachhaltigkeit"] = 5 if nk and nk.lower() not in ("keine", "nein", "-", "unbekannt") else 0
    cpvs = {re.sub(r"\D", "", s(c))[:8] for c in as_list(t.get("cpv"))}
    if cpvs & PROFILE_CPV:
        parts["cpv"] = 5
    elif any(c[:3] in {p[:3] for p in PROFILE_CPV} for c in cpvs if c):
        parts["cpv"] = 3
    else:
        parts["cpv"] = 1 if cpvs else 2
    frist = parse_date(t.get("angebotsfrist"))
    if frist is None:
        parts["zeit"] = 4
    elif frist < TODAY:
        parts["zeit"] = 0
    else:
        wd = workdays_until(frist)
        parts["zeit"] = 10 if wd >= 10 else (5 if wd >= 5 else 2)
    zw = s(t.get("zugangsweg")).lower()
    parts["zugang"] = 5 if "frei" in zw else (1 if "pq" in zw or "präqual" in zw else 3)
    parts["bonus"] = 5 if len(set(felder)) > 1 else 0
    total = min(sum(parts.values()), 100)
    klasse = "A" if total >= 75 else ("B" if total >= 50 else "C")
    return total, klasse, ko, parts


# ---------- Bewertung Signale ----------
def score_signal(sg: dict) -> tuple[int, str]:
    felder = [f for f in re.split(r"[+,/; ]+", s(sg.get("geschaeftsfeld")).lower()) if f]
    p = 30 if felder else 12
    vg = s(sg.get("vertrauensgrad")).lower()
    p += 20 if vg == "hoch" else (13 if vg == "mittel" else 6)
    m = re.search(r"Q([1-4])\s*/\s*(\d{4})", s(sg.get("erwarteter_zeitpunkt")))
    if m:
        qd = dt.date(int(m[2]), (int(m[1]) - 1) * 3 + 2, 15)
        months = (qd.year - TODAY.year) * 12 + qd.month - TODAY.month
        p += 20 if months <= 6 else (13 if months <= 12 else 6)
    else:
        p += 8
    txt = (s(sg.get("geschaetztes_volumen")) + " " + s(sg.get("beschreibung")) + " " + s(sg.get("abgeleiteter_bedarf"))).lower()
    p += 15 if re.search(r"rahmenvertrag|mehrjährig|mio|neubau|fusion", txt) else (10 if s(sg.get("geschaetztes_volumen")) else 6)
    reg = region(s(sg.get("ort")) + " " + s(sg.get("organisation")))
    p += 15 if reg == "kern" else (9 if reg == "erweitert" else 4)
    p = min(p, 100)
    return p, ("A" if p >= 75 else "B" if p >= 50 else "C")


def norm_key(name: str) -> str:
    n = s(name).lower()
    n = re.sub(r"\b(gmbh|ag|eg|e\.v\.|ev|kg|co|mbh|ggmbh|gemeinnützige|und|&)\b", " ", n)
    return re.sub(r"[^a-zäöüß0-9]+", "", n)


def main() -> None:
    raw = BASE / "raw"
    tenders = read_jsonl(raw / "A" / "treffer.jsonl") + read_jsonl(raw / "B" / "treffer.jsonl")
    # Deduplizierung: gleicher Titel+Auftraggeber
    seen, dedup = {}, []
    for t in tenders:
        k = norm_key(t.get("titel", ""))[:60] + "|" + norm_key(t.get("auftraggeber", ""))
        if k in seen:
            seen[k]["url"] = sorted(set(as_list(seen[k].get("url")) + as_list(t.get("url"))))
            continue
        seen[k] = t
        dedup.append(t)
    tenders = dedup
    for t in tenders:
        sc, kl, ko, parts = score_tender(t)
        t["score"], t["klasse"], t["ko_kriterien"], t["score_details"] = sc, kl, ko, parts
        fr = parse_date(t.get("angebotsfrist"))
        t["frist_status"] = "unbekannt" if fr is None else ("abgelaufen" if fr < TODAY else "offen")
        t["region"] = region(" ".join(s(t.get(k)) for k in ("ort", "nuts", "auftraggeber")))
    tenders.sort(key=lambda x: (x["frist_status"] != "offen", -x["score"]))

    signals = read_jsonl(raw / "C" / "signale.jsonl")
    for sg in signals:
        sg["score"], sg["klasse"] = score_signal(sg)
        sg["region"] = region(s(sg.get("ort")) + " " + s(sg.get("organisation")))
    signals.sort(key=lambda x: -x["score"])

    accounts = read_jsonl(raw / "D" / "accounts.jsonl")
    acc_by_key = {norm_key(a.get("organisation", "")): a for a in accounts}

    def link(org: str):
        k = norm_key(org)
        if not k:
            return None
        if k in acc_by_key:
            return acc_by_key[k]
        for ak, a in acc_by_key.items():
            if len(ak) > 5 and len(k) > 5 and (ak in k or k in ak):
                return a
        return None

    for t in tenders:
        a = link(t.get("auftraggeber", ""))
        if a is not None:
            a.setdefault("verknuepfte_treffer_ids", []).append(t["id"])
    for sg in signals:
        a = link(sg.get("organisation", ""))
        if a is not None:
            a.setdefault("verknuepfte_signale_ids", []).append(sg["id"])

    SEG_W = {"kanzlei": 14, "steuer": 14, "versicher": 13, "sparkasse": 13, "volksbank": 13, "bank": 12, "lebensmittel": 12,
             "bio": 12, "sozial": 13, "wohlfahrt": 13, "bildung": 10, "kommun": 9, "handwerk": 9, "bau": 9, "mittelstand": 11, "industrie": 10}
    for a in accounts:
        seg = s(a.get("segment")).lower()
        icp = max([w for k, w in SEG_W.items() if k in seg] or [8])
        fit = as_list(a.get("geschaeftsfeld_fit"))
        reg = region(s(a.get("standort")) + " " + s(a.get("organisation")))
        sc = icp + min(len(fit), 4) * 7 + (15 if reg == "kern" else 7 if reg == "erweitert" else 0)
        sc += 12 * len(a.get("verknuepfte_treffer_ids", [])) + 10 * len(a.get("verknuepfte_signale_ids", []))
        if s(a.get("signale")).strip():
            sc += 8
        if "bestandskunde" in (s(a.get("typ")) + s(a.get("segment")) + s(a.get("signale")) + s(a.get("bestandskunde"))).lower():
            sc += 6
        g = s(a.get("groesse")).lower()
        if re.search(r"\b(2\d|[3-9]\d|1\d\d|2[0-4]\d)\b", g) or any(x in g for x in ("mittel", "klein", "20–250", "50-249")):
            sc += 6
        a["score"] = min(sc, 100)
        a["klasse"] = "A" if a["score"] >= 75 else "B" if a["score"] >= 50 else "C"
        a["region"] = reg
    accounts.sort(key=lambda x: -x["score"])

    # 03a/b/c
    def dump(name, rows):
        with (BASE / name).open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    dump("03a_ausschreibungen.jsonl", tenders)
    dump("03b_signale.jsonl", signals)
    dump("03c_accounts.jsonl", accounts)

    competitors = read_jsonl(raw / "D" / "wettbewerber.jsonl")
    partners = read_jsonl(raw / "D" / "partner.jsonl")
    awards = read_jsonl(raw / "A" / "zuschlaege.jsonl")
    market = read_jsonl(raw / "E" / "marktbild.jsonl")
    build_xlsx(tenders, signals, accounts, competitors, partners, awards, market)
    stats = {"ausschreibungen": len(tenders), "offen": sum(t["frist_status"] == "offen" for t in tenders),
             "A_klasse_offen": sum(t["klasse"] == "A" and t["frist_status"] != "abgelaufen" for t in tenders),
             "signale": len(signals), "signale_A": sum(x["klasse"] == "A" for x in signals),
             "accounts": len(accounts), "accounts_A": sum(a["klasse"] == "A" for a in accounts),
             "wettbewerber": len(competitors), "partner": len(partners), "zuschlaege": len(awards), "markt": len(market)}
    (BASE / "build_stats.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False))


HDR_FILL = PatternFill("solid", fgColor="1F4E5A")
HDR_FONT = Font(color="FFFFFF", bold=True)
RED = PatternFill("solid", fgColor="F8CBAD")
GREEN = PatternFill("solid", fgColor="C6EFCE")


def add_sheet(wb, title, headers, rows, link_cols=(), date_cols=(), widths=None):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill, cell.font = HDR_FILL, HDR_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        vals = []
        for h, v in zip(headers, r):
            if h in date_cols:
                d = parse_date(v)
                vals.append(d if d else (s(v) or None))
            else:
                vals.append(s(v) if not isinstance(v, (int, float)) else v)
        ws.append(vals)
        ri = ws.max_row
        for h in link_cols:
            ci = headers.index(h) + 1
            cell = ws.cell(row=ri, column=ci)
            url = s(cell.value).split(";")[0].strip()
            if url.startswith("http"):
                cell.hyperlink = url
                cell.font = Font(color="0563C1", underline="single")
        for h in date_cols:
            ci = headers.index(h) + 1
            if isinstance(ws.cell(row=ri, column=ci).value, dt.date):
                ws.cell(row=ri, column=ci).number_format = "DD.MM.YYYY"
    for i, h in enumerate(headers, 1):
        w = (widths or {}).get(h, min(max(len(h) + 2, 12), 45))
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    if ws.max_row > 1:
        ws.auto_filter.ref = ws.dimensions
    for h in date_cols:
        if "frist" in h.lower():
            col = get_column_letter(headers.index(h) + 1)
            rng = f"{col}2:{col}{max(ws.max_row, 2)}"
            ws.conditional_formatting.add(rng, FormulaRule(
                formula=[f"AND(ISNUMBER({col}2),{col}2>=TODAY(),{col}2-TODAY()<7)"], fill=RED))
    return ws


def build_xlsx(tenders, signals, accounts, competitors, partners, awards, market):
    wb = Workbook()
    wb.remove(wb.active)
    T_H = ["Klasse", "Score", "ID", "Geschäftsfeld", "Titel", "Auftraggeber", "Ort", "Region", "Angebotsfrist", "Frist-Status",
           "Geschätzter Wert", "Verfahrensart", "Zugangsweg", "Eignung", "Zuschlagskriterien", "Nachhaltigkeitskriterien",
           "K.-o.-Hinweise", "Nächste Aktion", "Vertrauensgrad", "Quelle", "URL"]

    def trow(t):
        return [t["klasse"], t["score"], t.get("id"), t.get("geschaeftsfeld"), t.get("titel"), t.get("auftraggeber"),
                t.get("ort"), t.get("region"), t.get("angebotsfrist"), t["frist_status"], t.get("geschaetzter_wert"),
                t.get("verfahrensart"), t.get("zugangsweg"), t.get("eignungskriterien"), t.get("zuschlagskriterien"),
                t.get("nachhaltigkeitskriterien"), t.get("ko_kriterien"), t.get("naechste_aktion"),
                t.get("vertrauensgrad"), t.get("quelle"), as_list(t.get("url"))]
    W = {"Titel": 45, "Auftraggeber": 30, "URL": 40, "Eignung": 35, "Nächste Aktion": 40, "Beschreibung": 50}

    top_t = [t for t in tenders if t["frist_status"] != "abgelaufen" and t["klasse"] in ("A", "B")]
    top_s = [x for x in signals if x["klasse"] == "A"][:15]
    TOP_H = ["Typ", "Klasse", "Score", "ID", "Geschäftsfeld", "Titel / Signal", "Organisation", "Ort", "Frist / Zeitpunkt",
             "Nächste Aktion", "URL"]
    top_rows = [["Ausschreibung", t["klasse"], t["score"], t["id"], t.get("geschaeftsfeld"), t.get("titel"), t.get("auftraggeber"),
                 t.get("ort"), t.get("angebotsfrist"), t.get("naechste_aktion"), as_list(t.get("url"))] for t in top_t]
    top_rows += [["Signal", x["klasse"], x["score"], x["id"], x.get("geschaeftsfeld"), x.get("beschreibung"), x.get("organisation"),
                  x.get("ort"), x.get("erwarteter_zeitpunkt"), x.get("naechste_aktion") or x.get("abgeleiteter_bedarf"),
                  as_list(x.get("beleg_url"))] for x in top_s]
    add_sheet(wb, "Top-Chancen", TOP_H, top_rows, link_cols=["URL"], widths={"Titel / Signal": 55, "Nächste Aktion": 45, "URL": 40, "Organisation": 30})
    add_sheet(wb, "Öffentlich", T_H, [trow(t) for t in tenders if t.get("modul") == "A"], ["URL"], ["Angebotsfrist"], W)
    add_sheet(wb, "Privat", T_H, [trow(t) for t in tenders if t.get("modul") == "B"], ["URL"], ["Angebotsfrist"], W)
    S_H = ["Quartal", "Klasse", "Score", "ID", "Geschäftsfeld", "Signaltyp", "Organisation", "Ort", "Datum", "Beschreibung",
           "Abgeleiteter Bedarf", "Erwarteter Zeitpunkt", "Geschätztes Volumen", "Vertrauensgrad", "Beleg-URL"]
    sig_sorted = sorted(signals, key=lambda x: (s(x.get("erwarteter_zeitpunkt"))[-4:] + s(x.get("erwarteter_zeitpunkt"))[:2] or "9999", -x["score"]))
    add_sheet(wb, "Signale & Pipeline", S_H, [[x.get("erwarteter_zeitpunkt"), x["klasse"], x["score"], x.get("id"), x.get("geschaeftsfeld"),
              x.get("signal_typ"), x.get("organisation"), x.get("ort"), x.get("datum"), x.get("beschreibung"), x.get("abgeleiteter_bedarf"),
              x.get("erwarteter_zeitpunkt"), x.get("geschaetztes_volumen"), x.get("vertrauensgrad"), as_list(x.get("beleg_url"))]
              for x in sig_sorted], ["Beleg-URL"], ["Datum"], W)
    A_H = ["Segment", "Klasse", "Score", "Organisation", "Typ", "Geschäftsfeld", "Größe", "Standort", "Region", "Website",
           "Einkaufsweg", "Relevante Rollen", "Signale", "Verknüpfte Treffer", "Verknüpfte Signale", "Beleg-URL"]
    acc_sorted = sorted(accounts, key=lambda a: (s(a.get("segment")), -a["score"]))
    add_sheet(wb, "Zielkunden", A_H, [[a.get("segment"), a["klasse"], a["score"], a.get("organisation"), a.get("typ"),
              "+".join(as_list(a.get("geschaeftsfeld_fit"))), a.get("groesse"), a.get("standort"), a["region"], a.get("website"),
              a.get("einkaufsweg"), a.get("relevante_rollen"), a.get("signale"), a.get("verknuepfte_treffer_ids"),
              a.get("verknuepfte_signale_ids"), as_list(a.get("beleg_url"))] for a in acc_sorted], ["Website", "Beleg-URL"], [], W)
    C_H = ["Name", "Ort", "Geschäftsfeld", "Leistungsbreite", "Größe", "Referenzen / Zuschläge", "Positionierung", "Beleg-URL"]
    add_sheet(wb, "Wettbewerber", C_H, [[c.get("name"), c.get("ort"), c.get("geschaeftsfeld"), c.get("leistungsbreite"),
              c.get("groesse"), c.get("referenzen") or c.get("referenzen/zuschlaege") or c.get("zuschlaege"), c.get("positionierung"),
              as_list(c.get("beleg_url"))] for c in competitors], ["Beleg-URL"], [], {"Leistungsbreite": 45, "Positionierung": 40, "Beleg-URL": 40})
    R_H = ["Auftraggeber", "Leistung", "Geschäftsfeld", "Gewinner", "Wert", "Zuschlag", "Laufzeit", "Erwartete Wiederausschreibung", "URL"]
    add_sheet(wb, "Wiederausschreibungen", R_H, [[w.get("auftraggeber"), w.get("leistung"), w.get("geschaeftsfeld"), w.get("gewinner"),
              w.get("wert"), w.get("zuschlag_datum"), w.get("laufzeit"), w.get("erwartete_wiederausschreibung"), as_list(w.get("url"))]
              for w in awards], ["URL"], ["Zuschlag"], {"Leistung": 40, "Erwartete Wiederausschreibung": 40, "URL": 40})
    P_H = ["Name", "Ort", "Geschäftsfeld", "Kompetenz", "Nutzen für Wolkenhof", "Beleg-URL"]
    add_sheet(wb, "Partner", P_H, [[p.get("name"), p.get("ort"), p.get("geschaeftsfeld", ""), p.get("kompetenz"),
              p.get("nutzen_fuer_wolkenhof"), as_list(p.get("beleg_url"))] for p in partners], ["Beleg-URL"], [], {"Kompetenz": 40, "Nutzen für Wolkenhof": 45})
    M_H = ["ID", "Thema", "Geschäftsfeld", "Kennzahl", "Wert", "Einheit", "Jahr", "Region", "Quelle", "Bedeutung für Wolkenhof (Ableitung)", "URL"]
    add_sheet(wb, "Marktbild", M_H, [[m.get("id"), m.get("thema"), m.get("geschaeftsfeld"), m.get("kennzahl"), m.get("wert"),
              m.get("einheit"), m.get("jahr"), m.get("region"), m.get("quelle"), m.get("bedeutung_fuer_wolkenhof"), as_list(m.get("url"))]
              for m in market], ["URL"], [], {"Kennzahl": 40, "Bedeutung für Wolkenhof (Ableitung)": 50, "URL": 40})
    # Quellen-Log
    logs = []
    for t in tenders:
        for u in as_list(t.get("url")):
            logs.append([t.get("modul"), t.get("id"), t.get("quelle"), u, "Ausschreibung"])
    for x in signals:
        for u in as_list(x.get("beleg_url")):
            logs.append(["C", x.get("id"), x.get("signal_typ"), u, "Signal"])
    for a in accounts:
        for u in as_list(a.get("beleg_url")):
            logs.append(["D", a.get("organisation"), "Account", u, "Zielkunde"])
    for c in competitors:
        for u in as_list(c.get("beleg_url")):
            logs.append(["D", c.get("name"), "Wettbewerber", u, "Wettbewerber"])
    for m in market:
        for u in as_list(m.get("url")):
            logs.append(["E", m.get("id"), m.get("quelle"), u, "Marktbild"])
    for u in PROFILE["quellenbelege"]:
        logs.append(["Profil", "", "", u, "Firmenprofil"])
    add_sheet(wb, "Quellen-Log", ["Modul", "Bezug", "Quelle", "URL", "Art", "Geschäftsfeld"],
              [l + ["alle"] for l in logs], ["URL"], [], {"URL": 70, "Bezug": 30})
    # Firmenprofil
    fp = []
    for k, v in PROFILE["stammdaten"].items():
        if isinstance(v, dict):
            fp.append(["Stammdaten", k, s(v.get("wert")), s(v.get("status")), s(v.get("quelle"))])
        elif isinstance(v, list):
            for x in v:
                fp.append(["Standort", s(x.get("ort")), s(x.get("rolle")), "belegt", s(x.get("quelle"))])
    for f, lst in PROFILE["kernleistungen"].items():
        for x in lst:
            fp.append([f"Leistung", f, x, "belegt/Website", ""])
    for u in PROFILE["alleinstellungsmerkmale"]:
        fp.append(["USP", "alle", u["usp"], u["status"], u["quelle"]])
    for x in PROFILE["eignung"]["nicht_gefunden"]:
        fp.append(["Profillücke", "alle", x, "nicht belegt", ""])
    add_sheet(wb, "Firmenprofil", ["Bereich", "Geschäftsfeld / Schlüssel", "Wert", "Status", "Quelle"], fp, ["Quelle"], [],
              {"Wert": 70, "Quelle": 50, "Geschäftsfeld / Schlüssel": 25})
    wb.save(BASE / "markterkundung_wolkenhof.xlsx")


if __name__ == "__main__":
    main()
