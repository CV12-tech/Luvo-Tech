"""Erzeugt eine weiterleitungsfähige HTML-Fassung aller Ergebnisse (für den PDF-Druck mit Chromium)."""
import json, re, html, sys
import markdown
from openpyxl import load_workbook
OUT = sys.argv[1]
wb = load_workbook("markterkundung_sigma.xlsx")
P = json.load(open("01_firmenprofil.json"))
md = lambda t: markdown.markdown(t, extensions=["tables"])
def esc(v):
    if v is None: return ""
    s = str(v)
    if s.startswith("http"):
        u = s.split("; ")[0]; dom = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        return f'<a href="{html.escape(u)}">{html.escape(dom)}</a>'
    return html.escape(s)
def fmt(v):
    if hasattr(v, "strftime"): return v.strftime("%d.%m.%Y")
    return v
def table(sheet, cols, filt=None, limit=None, sort=None):
    ws = wb[sheet]; hdr = [c.value for c in ws[1]]; idx = [hdr.index(c) for c in cols]
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True)]
    if filt: rows = [r for r in rows if filt(dict(zip(hdr, r)))]
    if sort: rows.sort(key=lambda r: sort(dict(zip(hdr, r))))
    if limit: rows = rows[:limit]
    h = "<table><thead><tr>" + "".join(f"<th>{html.escape(c)}</th>" for c in cols) + "</tr></thead><tbody>"
    for r in rows:
        h += "<tr>" + "".join(f"<td>{esc(fmt(r[i]))}</td>" for i in idx) + "</tr>"
    return h + f"</tbody></table><p class='n'>{len(rows)} Einträge</p>"
bericht = open("markterkundung_bericht.md").read().split("\n", 1)[1]
plan = open("02a_umsetzungs_stufenplan.md").read().split("\n", 1)[1]
qual = open("04_qualitaet.md").read().split("## Reproduktion")[0].split("\n", 1)[1]
st = P["stammdaten"]
profil = f"""
<table class="kv"><tbody>
<tr><td>Firma</td><td>{st['firma']}, {st['adresse']}</td></tr>
<tr><td>Register</td><td>{st['register']} · Gesellschaftsvertrag {st['gesellschaftsvertrag']} · Eintragung {st['eintragung']} · Stammkapital 25.000 €</td></tr>
<tr><td>Geschäftsführung</td><td>Marcus Strube (Gründer, laut Impressum)</td></tr>
<tr><td>Unternehmensgegenstand</td><td>{st['unternehmensgegenstand']}</td></tr>
<tr><td>Schwesterfirma</td><td>{st['schwesterfirma']}</td></tr>
<tr><td>Größe</td><td>{st['mitarbeiter']}</td></tr>
<tr><td>Kurzbeschreibung</td><td>{P['kurzbeschreibung']}</td></tr>
<tr><td>Wertversprechen</td><td>{P['wertversprechen']}</td></tr>
<tr><td>Realistische Auftragsgröße</td><td>{P['realistische_auftragsgroesse']}</td></tr>
<tr><td>Belegte Referenzprojekte</td><td>{'; '.join(r['projekt'] for r in P['referenzprojekte_belegt'])}</td></tr>
<tr><td>Fertigungspartner</td><td>O.H.M. Objekteinrichtungen in Holz und Metall GmbH, Kirchlengern (SIGMA ist Handelsvertretung)</td></tr>
</tbody></table>
<h3>Korrekturen gegenüber dem Vorab-Profil</h3><ul>{''.join(f'<li>{html.escape(c)}</li>' for c in P['korrekturen_gegenueber_vorabprofil'])}</ul>
<h3>Offene Punkte</h3><ul>{''.join(f'<li>{html.escape(c)}</li>' for c in P['offene_punkte'])}<li>Referenz „Lüning“: Lüning Ladenbau GmbH (Langenberg) ist Mitglied im Ladenbauverband – möglicherweise Partner statt Bäckerei.</li></ul>
"""
CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
@page wide { size: A4 landscape; margin: 14mm 12mm 16mm 12mm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 9.6pt; color: #1b1f24; line-height: 1.42; }
h1 { font-size: 22pt; color: #1F3864; margin: 0 0 4mm; }
h2 { font-size: 14pt; color: #1F3864; border-bottom: 2px solid #1F3864; padding-bottom: 1mm; margin-top: 7mm; break-after: avoid; }
h3 { font-size: 11pt; color: #2E5597; margin-top: 5mm; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 3mm; font-size: 8.2pt; }
th { background: #1F3864; color: #fff; text-align: left; padding: 1.4mm 1.6mm; vertical-align: top; }
td { border-bottom: 0.4pt solid #c9d1dc; padding: 1.2mm 1.6mm; vertical-align: top; }
tr { break-inside: avoid; }
thead { display: table-header-group; }
tr:nth-child(even) td { background: #f4f6fa; }
.wide { page: wide; } .wide table { font-size: 7.2pt; }
.break { break-before: page; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; }
.cover .sub { font-size: 13pt; color: #2E5597; } .cover .meta { margin-top: 12mm; font-size: 10pt; color: #555; }
.box { background: #eef2f8; border-left: 4px solid #1F3864; padding: 3mm 4mm; margin: 4mm 0; }
.kv td:first-child { width: 42mm; font-weight: bold; color: #1F3864; }
.n { font-size: 7.5pt; color: #777; margin-top: -1mm; }
a { color: #0563C1; text-decoration: none; }
blockquote { border-left: 3px solid #9fb3d6; margin: 3mm 0; padding: 1mm 4mm; color: #444; background: #f7f9fc; }
code { font-size: 8pt; }
"""
toc = ["1 Bericht (Executive Summary, Top-10, Pipeline, Bestandskunden, Zielkunden, Wettbewerb, Segmente, F-Gase & Förderung, Profillücken, Partner)",
       "2 Umsetzungs- und Stufenplan Nord- und Mitteldeutschland", "3 Geprüftes Firmenprofil",
       "Anhang A1 Top-Chancen mit nächster Aktion", "Anhang A2 Projekt-Pipeline (Stufe 1–2, Klassen A/B)", "Anhang A3 Projekt-Pipeline Stufe 3 (Klasse A)",
       "Anhang A4 Öffentliche Ausschreibungen", "Anhang A5 Private Kanäle", "Anhang A6 Bestandskunden-Potenzial", "Anhang A7 Zielkunden (Top 100)",
       "Anhang A8 Wettbewerber", "Anhang A9 Partner", "Anhang A10 Wiederausschreibungen", "Anhang A11 Marktbild", "Anhang A12 Methodik und Qualität"]
H = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Markterkundung SIGMA Ladenbau</title><style>{CSS}</style></head><body>
<div class="cover"><h1>Markterkundung<br>SIGMA Ladenbau und Projekt GmbH</h1>
<div class="sub">Öffentliche und private Ausschreibungen · Projekt- und Bedarfssignale · Zielkunden · Wettbewerb · Marktbild</div>
<div class="meta">Suchraum: Nord- und Mitteldeutschland in drei Stufen (Kern: Sachsen-Anhalt, Berlin, Brandenburg)<br>Stand: 17.11.2026</div>
<div class="box" style="margin-top:14mm"><b>Inhalt</b><br>{'<br>'.join(toc)}</div>
<p style="font-size:8pt;color:#666;margin-top:8mm">Belegte Fakten sind mit einer Quelle verlinkt; Ableitungen und Schätzungen sind gekennzeichnet. Personen sind nur in ihrer beruflichen Rolle genannt, sofern öffentlich (Impressum, Pressemitteilung, Register).
Datengrundlage u. a.: TED API, oeffentlichevergabe.de, neueroeffnung.info, OpenStreetMap (© OSM-Mitwirkende, ODbL), Presse- und Unternehmensquellen.</p></div>
<div class="break"></div><h2>1 Bericht</h2>{md(bericht)}
<div class="break"></div><h2>2 Umsetzungs- und Stufenplan</h2>{md(plan)}
<div class="break"></div><h2>3 Geprüftes Firmenprofil</h2>{profil}
<div class="wide"><div class="break"></div>
<h2>Anhang A1 – Top-Chancen mit nächster Aktion</h2>{table('Top-Chancen', ['Art','Score','Klasse','Segment','Stufe','Organisation/Auftraggeber','Typ/Titel','Ort','Termin','Angebotsfrist','Nächste Aktion','Beleg'])}
<div class="break"></div><h2>Anhang A2 – Projekt-Pipeline Stufe 1–2 (Klassen A und B), nach Quartal</h2>
{table('Projekt-Pipeline', ['Quartal','Score','Klasse','Segment','Stufe','Objekt/Organisation','Signaltyp','Projektphase','Termin (Quelle)','Adresse Objekt','Volumen (geschätzt)','Beleg'], filt=lambda r: r['Klasse'] in ('A','B') and r['Stufe'] in (1,2))}
<div class="break"></div><h2>Anhang A3 – Projekt-Pipeline Stufe 3 (nur Klasse A, gemäß Stufenplan)</h2>
{table('Projekt-Pipeline', ['Quartal','Score','Segment','Land','Objekt/Organisation','Signaltyp','Projektphase','Termin (Quelle)','Adresse Objekt','Beleg'], filt=lambda r: r['Klasse']=='A' and r['Stufe']==3)}
<div class="break"></div><h2>Anhang A4 – Öffentliche Ausschreibungen (letzte 90 Tage und offene Fristen)</h2>
{table('Öffentlich', ['Score','Klasse','K.-o.','Segment','Stufe','Auftraggeber','Titel','Ort','Verfahren','Angebotsfrist','Werktage bis Frist','Unterlagen','Bekanntmachung'])}
<h2>Anhang A5 – Private Kanäle und Projektanfragen</h2>{table('Privat', ['Segment','Stufe','Titel','Organisation','Art','Zugang','Status','Klasse','Link'])}
<div class="break"></div><h2>Anhang A6 – Bestandskunden-Potenzial</h2>{table('Bestandskunden-Potenzial', ['Segment','Kunde/Gruppe','Filialen (gesamt)','davon Stufe 1','Standorte','Signale/Anlässe','Nächste Aktion','Beleg'])}
<div class="break"></div><h2>Anhang A7 – Zielkunden (Top 100 nach Score)</h2>
{table('Zielkunden', ['Score','Klasse','Segment','Organisation','Filialen (OSM, Untergrenze)','davon Stufe 1','Top-Standorte','Umbaubedarf (geschätzt)','Einkaufsweg','Entscheiderrolle','Bestandskunde'], limit=100)}
<p class="n">Vollständige Liste (480 Zielkunden) in der Excel-Datei „markterkundung_sigma.xlsx“.</p>
<div class="break"></div><h2>Anhang A8 – Wettbewerber</h2>{table('Wettbewerber', ['Segment','Wettbewerber','Typ','Positionierung/Notiz','Beleg'])}
<h2>Anhang A9 – Partner</h2>{table('Partner', ['Segment','Partner','Rolle','Notiz','Beleg'])}
<div class="break"></div><h2>Anhang A10 – Vergangene Zuschläge und Prognose Wiederausschreibung</h2>
{table('Wiederausschreibungen', ['Segment','Auftraggeber','Titel','Ort','Zuschlag veröffentlicht','Gewinner','Wert (€)','Prognose Wiederausschreibung','Bekanntmachung'])}
<div class="break"></div><h2>Anhang A11 – Marktbild</h2>{table('Marktbild', ['Bereich','Kennzahl','Wert','Anmerkung','Quelle','Link'])}
</div>
<div class="break"></div><h2>Anhang A12 – Methodik und Qualität</h2>{md(qual)}
</body></html>"""
H = H.replace("Ulrike Hoge-Peters", "die Insolvenzverwalterin")
open(OUT, "w").write(H); print("html ok", len(H))
