# 02a – Umsetzungs- und Stufenplan: Erweiterung auf Nord- und Mitteldeutschland
Stand 16.11.2026 · Grundlage: freigegebenes Profil (01_firmenprofil.json)

## Ausgangslage (Fakten → Folgerung)
- SIGMA hat 3 öffentlich genannte Personen, keine eigene Fertigung und arbeitet als Handelsvertretung für O.H.M. (Kirchlengern). **Folgerung:** Die Reichweite wird durch Projektleitung und Montage begrenzt, nicht durch die Fertigung.
- Die belegten Referenzen liegen fast alle in Sachsen-Anhalt (Altmark, Harz, Saalekreis, Anhalt), dazu Mühlenbeck (BB).
- Hanse Ladenbau (Kavelstorf, MV) ist seit 31.07.2026 insolvent. Hanse hatte eine Niederlassung in Kiel und Außendienstbüros in Berlin, Dresden und Magdeburg. **Folgerung:** Im Norden und Osten fehlt Bestandskunden ein Lebensmittel-Ladenbauer. Das ist der stärkste Hebel für die Expansion, solange er zeitlich offen ist (geschätzt 6–12 Monate, bis Wettbewerber die Kunden übernommen haben).

## Drei Stufen

| Stufe | Länder / NUTS | Entfernung ab Möser (Straße, geschätzt) | Lieferweg | Region-Score (Phase 4) | Zeitraum |
|---|---|---|---|---|---|
| **1 – Kern** | ST (DEE0), BE (DE30), BB (DE40) | 0–200 km | SIGMA direkt | 15/15 | sofort |
| **2 – Nahbereich** | SN (DED), TH (DEG), NI-Ost: Braunschweig (DE91), Hannover (DE92) | 120–250 km | SIGMA plus regionaler Montagepartner | 10/15 | Q1–Q2 2027 |
| **3 – Nord und Mitte** | MV (DE80), HH (DE60), SH (DEF0), HB (DE50), NI-Lüneburg (DE93), Weser-Ems (DE94), HE (DE7) | 200–400 km | nur mit Projektleiter Nord bzw. Partner vor Ort; Hinweis „Partner nötig“ | 5/15 | ab Q2 2027 (Hanse-Lücke MV/SH schon ab sofort beobachten) |

Außerhalb des Suchraums (NRW, RP, SL, BW, BY) wird nur mit dem Hinweis „Partner nötig“ erfasst.

### Handelsstruktur je Stufe (Einkaufswege; Wissensstand, in Phase 3 belegen)
| Stufe | EDEKA-Region | REWE-Region | weitere Schwerpunkte |
|---|---|---|---|
| 1 | Minden-Hannover (belegt: ST, BE, BB) | REWE Ost | nah&gut, Konsum, Bio Company, CAP |
| 2 | Nordbayern-Sachsen-Thüringen (SN, TH); Minden-Hannover (NI-Ost) | REWE Ost/Mitte | Konsum Dresden/Leipzig, Filialbäckereien |
| 3 | EDEKA Nord (SH, HH, MV); Minden-Hannover (HB, NI-West); Hessenring (HE) | REWE Nord, REWE Mitte | famila (Bartels-Langness, Nord), Markant, tegut (HE), Hanse-Altkunden |

## Umsetzung: Arbeitspakete für die Markterkundung

| # | Paket | Stufe | Modul | Ergebnis |
|---|---|---|---|---|
| U1 | Kernregion vollständig erkunden (alle Signale, Accounts, Ausschreibungen) | 1 | A–D | Pipeline, Top-25-Zielkunden |
| U2 | **Hanse-Ladenbau-Lücke:** Hanse-Referenzkunden ermitteln, Verfahrensstand verfolgen (Verwertung, Personal, Fortführung) | 1–3 | C, D | Liste der „verwaisten“ Kunden; Kandidaten für einen Projektleiter Nord (ehemalige Hanse-Außendienstler, nur rollenbasiert und öffentlich) |
| U3 | Nahbereich: Signale nur ab Klasse B, Accounts mit mindestens 5 Filialen | 2 | C, D | Pipeline Stufe 2 |
| U4 | Nord und Mitte: nur Klasse A, Großfilialisten und EDEKA-Nord-/Hessenring-Kaufleute mit Expansion | 3 | C, D | Shortlist mit Hinweis „Partner nötig“ |
| U5 | Öffentliche Vergaben in allen 11 Ländern über die TED- und oeffentlichevergabe.de-API (bundesweit filterbar nach NUTS) | 1–3 | A, E | Ausschreibungen, Zuschläge der letzten 5 Jahre, Volumen |
| U6 | Partner-Mapping je Stufe: Montage, Kälte, Elektro, Tischlerei | 2–3 | D | Partnerliste je Region |
| U7 | Wettbewerb je Stufe, mit Neuverteilung nach dem Ausfall von Hanse | 1–3 | D, E | Wettbewerbskarte |

## Umsetzung: Maßnahmen für SIGMA (Empfehlung, Ableitung)

| Phase | Zeitraum | Maßnahme | Erfolgsmaß |
|---|---|---|---|
| 0 | sofort – 01/2027 | Hanse-Altkunden in ST, BE, BB, MV ansprechen; OHM als Fertigungspartner mitnehmen | ≥ 10 Erstgespräche |
| 1 | Q1 2027 | Montagepartner in Sachsen/Thüringen und NI-Ost vertraglich binden; Referenzseite um Backshop-/Thekenprojekte erweitern | 2 Partner, 3 Angebote in Stufe 2 |
| 2 | Q2 2027 | Projektleiter Nord (Raum Rostock/Hamburg), festangestellt oder als freier Handelsvertreter; Kälte- und Montagepartner im Norden | 1 Person, 2 Projekte in Stufe 3 |
| 3 | H2 2027 | Präqualifizierung (PQ-VOB, alternativ AVPQ) und gemeinsame Referenzbasis mit OHM für Bietergemeinschaften | PQ-Eintrag, 1 öffentliches Verfahren |
| laufend | wöchentlich | scout.py: Module A/B/C wöchentlich, D monatlich, gefiltert nach Stufe | Diff-Report „neu seit letztem Lauf“ |

**Entscheidungstor vor Stufe 3:** Stufe 3 wird erst aktiv bearbeitet, wenn Stufe 2 mindestens 2 Aufträge gebracht hat oder ein Projektleiter Nord feststeht. Bis dahin werden dort nur Klasse-A-Chancen gemeldet.

## Auswirkungen auf das Scoring (Phase 4)
- Kriterium Region: Stufe 1 = 15, Stufe 2 = 10, Stufe 3 = 5 Punkte; außerhalb = 0 plus Hinweis „Partner nötig“.
- Neuer Bonus +5: früherer Hanse-Ladenbau-Kunde, sofern belegt.
- Filter in Phase 3: Stufe 2 nur ab Klasse B, Stufe 3 nur ab Klasse A.
