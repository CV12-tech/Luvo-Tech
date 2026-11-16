#!/usr/bin/env python3
"""make_pdf.py – erzeugt markterkundung_wolkenhof.html (+ PDF via render_pdf.js) aus Bericht, Profil und JSONL-Daten."""
import html
import json
from pathlib import Path

import markdown

BASE = Path(__file__).resolve().parent


def jl(name):
    p = BASE / name
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def s(v):
    if v is None:
        return ""
    if isinstance(v, list):
        return "; ".join(s(x) for x in v)
    if isinstance(v, dict):
        return "; ".join(f"{k}: {s(x)}" for k, x in v.items())
    return str(v)


def esc(v, maxlen=None):
    t = s(v)
    if maxlen and len(t) > maxlen:
        t = t[: maxlen - 1] + "…"
    return html.escape(t)


def link(urls):
    u = [x for x in (urls if isinstance(urls, list) else [urls]) if x and str(x).startswith("http")]
    if not u:
        return ""
    short = u[0].split("//", 1)[-1].split("/", 1)[0]
    return f'<a href="{html.escape(u[0])}">{html.escape(short)}</a>' + (f" (+{len(u)-1})" if len(u) > 1 else "")


NOWRAP = {"Klasse", "ID", "Frist", "Status", "CPV", "Jahr"}


def table(headers, rows, cls=""):
    h = "".join(f'<th class="{"nw" if x in NOWRAP else ""}">{html.escape(x)}</th>' for x in headers)
    b = "".join("<tr>" + "".join(f'<td class="{"nw" if headers[i] in NOWRAP else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def badge(k):
    return f'<span class="k k{k}">{k}</span>'


def md(path):
    txt = (BASE / path).read_text(encoding="utf-8")
    return markdown.markdown(txt, extensions=["tables", "sane_lists"])


T = jl("03a_ausschreibungen.jsonl")
S = jl("03b_signale.jsonl")
A = jl("03c_accounts.jsonl")
W = jl("raw/D/wettbewerber.jsonl")
P = jl("raw/D/partner.jsonl")
Z = jl("raw/A/zuschlaege.jsonl")
M = jl("raw/E/marktbild.jsonl")
PROF = json.loads((BASE / "01_firmenprofil.json").read_text(encoding="utf-8"))

sections = []

# Deckblatt
sections.append(f"""
<section class="cover">
  <div class="eyebrow">Markterkundung · Stand 16.11.2026</div>
  <h1>Wolkenhof GmbH<br><span>Uelzen</span></h1>
  <p class="lead">Öffentliche und private Ausschreibungen · Bedarfssignale · Zielkunden · Wettbewerb · Marktbild</p>
  <div class="kpis">
    <div><b>{len(T)}</b><span>Ausschreibungen</span></div>
    <div><b>{sum(t['frist_status']=='offen' for t in T)}</b><span>davon offen</span></div>
    <div><b>{len(S)}</b><span>Bedarfssignale</span></div>
    <div><b>{len(A)}</b><span>Zielkunden</span></div>
    <div><b>{len(W)}</b><span>Wettbewerber</span></div>
    <div><b>{len(M)}</b><span>Marktkennzahlen</span></div>
  </div>
  <p class="note">Datenbasis: ausschließlich Websuche (Suchtreffer). Fristen und Werte vor jedem Angebot in der Originalbekanntmachung prüfen.
  Legende: [F] belegter Fakt · [A] Ableitung · Klassen A ≥ 75, B 50–74, C &lt; 50.</p>
  <h3>Inhalt</h3>
  <ol class="toc">
    <li>Bericht (Executive Summary, Top-10, Pipeline, Zielkunden, Wettbewerb, Potenzial, Profillücken, Partner)</li>
    <li>Firmenprofil (geprüft)</li>
    <li>Anhang A – Ausschreibungen (öffentlich und privat)</li>
    <li>Anhang B – Bedarfssignale und Pipeline</li>
    <li>Anhang C – Wiederausschreibungen</li>
    <li>Anhang D – Zielkunden</li>
    <li>Anhang E – Wettbewerber und Partner</li>
    <li>Anhang F – Marktbild</li>
    <li>Qualitätsbericht und Methodik</li>
  </ol>
</section>""")

# 1 Bericht
rep = md("markterkundung_bericht.md")
rep = rep.split("<hr />", 1)[-1] if "<hr />" in rep else rep
sections.append(f'<section><div class="chapter">1 · Bericht</div>{rep}</section>')

# 2 Profil
st = PROF["stammdaten"]
rows = []
for k, v in st.items():
    if isinstance(v, dict):
        rows.append([esc(k.replace("_", " ")), esc(v.get("wert")), esc(v.get("status")), link(v.get("quelle") if isinstance(v.get("quelle"), list) else [v.get("quelle")])])
for x in st.get("standorte", []):
    rows.append(["Standort", esc(x["ort"]), esc(x["rolle"]), link(x["quelle"] if isinstance(x["quelle"], list) else [x["quelle"]])])
lei = "".join(f"<li><b>{html.escape(f)}:</b> {html.escape('; '.join(l))}</li>" for f, l in PROF["kernleistungen"].items())
usp = "".join(f"<li>{html.escape(u['usp'])} <i>({html.escape(u['status'])})</i></li>" for u in PROF["alleinstellungsmerkmale"])
icp = "".join(f"<li><b>{html.escape(f)}:</b> {html.escape(t)}</li>" for f, t in PROF["zielkunden_profil"].items())
gap = "".join(f"<li>{html.escape(x)}</li>" for x in PROF["eignung"]["nicht_gefunden"])
size = "".join(f"<li><b>{html.escape(f)}:</b> {html.escape(t)}</li>" for f, t in PROF["realistische_auftragsgroesse"].items())
cpv = table(["CPV", "Titel", "Feld", "Konfidenz"], [[c["code"], esc(c["titel"]), c["feld"], esc(c["konfidenz"])] for c in PROF["cpv_codes"]], "small")
sections.append(f"""<section><div class="chapter">2 · Firmenprofil (geprüft, Stand 16.11.2026)</div>
<h2>Kurzbeschreibung</h2><p>{html.escape(PROF['kurzbeschreibung'])}</p>
<p><b>Wertversprechen:</b> {html.escape(PROF['wertversprechen'])}</p>
<h2>Stammdaten</h2>{table(['Merkmal','Wert','Status','Quelle'], rows, 'small')}
<h2>Kernleistungen</h2><ul>{lei}</ul>
<h2>Alleinstellungsmerkmale</h2><ul>{usp}</ul>
<h2>Zielkundenprofil je Geschäftsfeld</h2><ul>{icp}</ul>
<h2>Realistische Auftragsgröße (geschätzt)</h2><ul>{size}</ul>
<h2>Eignungslücken (nicht belegt)</h2><ul>{gap}</ul>
<h2>CPV-Codes</h2><p class="muted">{html.escape(PROF['cpv_pruefhinweis'])}</p>{cpv}
</section>""")

# A Ausschreibungen
def trow(t):
    return [badge(t["klasse"]) + f" {t['score']}", esc(t["id"]), esc(s(t.get("geschaeftsfeld")).replace('+',' + ')), esc(t.get("titel"), 90),
            esc(t.get("auftraggeber"), 60), esc(t.get("ort"), 30), esc(t.get("angebotsfrist")), esc(t["frist_status"]),
            esc(t.get("ko_kriterien")), esc(t.get("naechste_aktion"), 220), link(t.get("url"))]
TH = ["Klasse", "ID", "Feld", "Titel", "Auftraggeber", "Ort", "Frist", "Status", "K.-o.", "Nächste Aktion", "Quelle"]
pub = [t for t in T if t.get("modul") == "A"]
prv = [t for t in T if t.get("modul") == "B"]
sections.append(f"""<section class="land"><div class="chapter">Anhang A · Ausschreibungen</div>
<h2>Öffentlich ({len(pub)})</h2>{table(TH, [trow(t) for t in pub], 'small')}
<h2>Privat / Projektbörsen ({len(prv)})</h2>{table(TH, [trow(t) for t in prv], 'small')}
</section>""")

# B Signale
qs = sorted(S, key=lambda x: (s(x.get("erwarteter_zeitpunkt"))[3:7] + s(x.get("erwarteter_zeitpunkt"))[:2] if s(x.get("erwarteter_zeitpunkt")).startswith("Q") else "9999", -x["score"]))
sections.append(f"""<section class="land"><div class="chapter">Anhang B · Bedarfssignale und Pipeline ({len(S)})</div>
{table(['Klasse','ID','Zeitpunkt','Feld','Typ','Organisation','Beschreibung','Abgeleiteter Bedarf / Aktion','Vertrauen','Beleg'],
 [[badge(x['klasse'])+f" {x['score']}", esc(x['id']), esc(x.get('erwarteter_zeitpunkt'),30), esc(s(x.get('geschaeftsfeld')).replace('+',' + ')), esc(x.get('signal_typ'),30),
   esc(x.get('organisation'),55), esc(x.get('beschreibung'),220), esc(x.get('naechste_aktion') or x.get('abgeleiteter_bedarf'),200),
   esc(x.get('vertrauensgrad'),25), link(x.get('beleg_url'))] for x in qs], 'small')}
</section>""")

# C Wiederausschreibungen
sections.append(f"""<section class="land"><div class="chapter">Anhang C · Vergangene Zuschläge und erwartete Wiederausschreibungen ({len(Z)})</div>
{table(['Auftraggeber','Leistung','Feld','Gewinner','Wert','Zuschlag','Laufzeit','Erwartete Wiederausschreibung (geschätzt)','Quelle'],
 [[esc(z.get('auftraggeber'),50), esc(z.get('leistung'),120), esc(z.get('geschaeftsfeld')), esc(z.get('gewinner'),40), esc(z.get('wert'),40),
   esc(z.get('zuschlag_datum'),60), esc(z.get('laufzeit'),50), esc(z.get('erwartete_wiederausschreibung'),200), link(z.get('url'))] for z in Z], 'small')}
</section>""")

# D Zielkunden
acc = sorted(A, key=lambda a: -a["score"])
sections.append(f"""<section class="land"><div class="chapter">Anhang D · Zielkunden ({len(A)}, nach Score)</div>
{table(['Klasse','Organisation','Segment','Felder','Größe','Standort','Einkaufsweg','Signale / Ansatz','Beleg'],
 [[badge(a['klasse'])+f" {a['score']}", esc(a.get('organisation'),60), esc(a.get('segment'),25), esc(' + '.join(a.get('geschaeftsfeld_fit') or [])),
   esc(a.get('groesse'),40), esc(a.get('standort'),35), esc(a.get('einkaufsweg'),45), esc(a.get('signale'),180), link(a.get('beleg_url'))] for a in acc], 'small')}
</section>""")

# E Wettbewerb & Partner
sections.append(f"""<section class="land"><div class="chapter">Anhang E · Wettbewerber ({len(W)}) und Partner ({len(P)})</div>
<h2>Wettbewerber</h2>
{table(['Name','Ort','Feld','Leistungsbreite','Größe','Positionierung','Beleg'],
 [[esc(c.get('name'),50), esc(c.get('ort'),35), esc(c.get('geschaeftsfeld'),30), esc(c.get('leistungsbreite'),160), esc(c.get('groesse'),40),
   esc(c.get('positionierung'),160), link(c.get('beleg_url'))] for c in W], 'small')}
<h2>Partner für Bietergemeinschaften</h2>
{table(['Name','Ort','Kompetenz','Nutzen für Wolkenhof','Beleg'],
 [[esc(p.get('name'),50), esc(p.get('ort'),30), esc(p.get('kompetenz'),120), esc(p.get('nutzen_fuer_wolkenhof'),200), link(p.get('beleg_url'))] for p in P], 'small')}
</section>""")

# F Marktbild
mk = (BASE / "raw/E/marktbild.md")
mtxt = markdown.markdown(mk.read_text(encoding="utf-8"), extensions=["tables"]) if mk.exists() else ""
sections.append(f"""<section><div class="chapter">Anhang F · Marktbild</div>{mtxt}</section>""")
sections.append(f"""<section class="land"><h2>Marktkennzahlen ({len(M)})</h2>
{table(['ID','Thema','Feld','Kennzahl','Wert','Einheit','Jahr','Bedeutung (Ableitung)','Quelle'],
 [[esc(m.get('id')), esc(m.get('thema'),40), esc(m.get('geschaeftsfeld')), esc(m.get('kennzahl'),110), esc(m.get('wert'),40), esc(m.get('einheit'),20),
   esc(m.get('jahr')), esc(m.get('bedeutung_fuer_wolkenhof'),160), link(m.get('url'))] for m in M], 'small')}
</section>""")

# Qualität + Methodik
q = md("04_qualitaet.md")
tools = md("00_tools.md")
plan = md("02_quellenplan.md")
ba = (BASE / "raw/C/bedarfsausloeser_status.md")
batxt = markdown.markdown(ba.read_text(encoding="utf-8"), extensions=["tables"]) if ba.exists() else ""
sections.append(f'<section><div class="chapter">Qualitätsbericht</div>{q}</section>')
sections.append(f'<section><div class="chapter">Methodik · Status der Bedarfsauslöser</div>{batxt}</section>')
sections.append(f'<section><div class="chapter">Methodik · Werkzeuge</div>{tools}</section>')
sections.append(f'<section class="land"><div class="chapter">Methodik · Quellenplan</div>{plan}</section>')

CSS = """
@page { size: A4; margin: 16mm 14mm 16mm 14mm; }
@page land { size: A4 landscape; margin: 12mm 10mm 14mm 10mm; }
:root { --ink:#1b2a30; --muted:#5b6b72; --accent:#1F4E5A; --green:#2e7d5b; --line:#d5dde0; --bg:#f3f6f7; }
* { box-sizing: border-box; }
body { font-family: "Inter","Segoe UI","Helvetica Neue",Arial,sans-serif; color: var(--ink); font-size: 9.6pt; line-height: 1.42; margin:0; background:#fff; }
section { page-break-after: always; }
section:last-child { page-break-after: auto; }
section.land { page: land; }
.chapter { font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; color: var(--green); font-weight: 700; border-bottom: 2px solid var(--accent); padding-bottom: 4px; margin-bottom: 10px; }
h1 { font-size: 34pt; line-height: 1.05; color: var(--accent); margin: 8px 0 10px; }
h1 span { color: var(--green); font-weight: 400; }
h2 { font-size: 13pt; color: var(--accent); margin: 16px 0 6px; page-break-after: avoid; }
h3 { font-size: 11pt; color: var(--accent); margin: 12px 0 4px; page-break-after: avoid; }
p, li { orphans: 3; widows: 3; }
a { color: #0b5cad; text-decoration: none; }
table { width: 100%; border-collapse: collapse; margin: 6px 0 12px; font-size: 8.4pt; }
table.small { font-size: 7.2pt; }
th { background: var(--accent); color: #fff; text-align: left; padding: 4px 5px; font-weight: 600; vertical-align: bottom; }
td { padding: 3.5px 5px; border-bottom: 1px solid var(--line); vertical-align: top; overflow-wrap: anywhere; }
tr:nth-child(even) td { background: var(--bg); }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
.k { display:inline-block; min-width: 15px; text-align:center; border-radius: 3px; color:#fff; font-weight:700; padding: 0 3px; }
.kA { background:#2e7d5b; } .kB { background:#c98a12; } .kC { background:#8a969b; }
.cover { padding-top: 40mm; }
.eyebrow { color: var(--green); font-weight: 700; letter-spacing: .1em; text-transform: uppercase; font-size: 9pt; }
.lead { font-size: 13pt; color: var(--muted); max-width: 150mm; }
.kpis { display:grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 18px 0; max-width: 160mm; }
.kpis div { background: var(--bg); border-left: 4px solid var(--accent); padding: 8px 10px; }
.kpis b { display:block; font-size: 20pt; color: var(--accent); }
.kpis span { color: var(--muted); font-size: 8.5pt; }
.note { font-size: 8.5pt; color: var(--muted); max-width: 160mm; border-top: 1px solid var(--line); padding-top: 8px; }
.toc li { margin: 2px 0; }
td.nw, th.nw { white-space: nowrap; overflow-wrap: normal; }
.muted { color: var(--muted); font-size: 8pt; }
code { font-size: 8pt; background: var(--bg); padding: 0 3px; }
"""

doc = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Markterkundung Wolkenhof GmbH</title><style>{CSS}</style></head>
<body>{''.join(sections)}</body></html>"""
(BASE / "markterkundung_wolkenhof.html").write_text(doc, encoding="utf-8")
print("html ok")
