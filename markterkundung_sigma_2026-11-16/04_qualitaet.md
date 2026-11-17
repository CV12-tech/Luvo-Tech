# 04 – Qualität, Trichter und Blockaden

Stand: 17.11.2026 (Europe/Berlin)

## Trichter je Modul

| Modul | Rohmenge | nach Region/Relevanzfilter | nach Tiefenprüfung / Bewertung | Ergebnis |
|---|---|---|---|---|
| **A – öffentlich (TED)** | 744 Bekanntmachungen (90 Tage) · 5.835 Zuschläge (5 Jahre) | 46 relevant (90 Tage) · 55 relevante Zuschläge | 12 manuell eingestuft | in `03a` zusammengeführt |
| **A – öffentlich (oeffentlichevergabe.de)** | 1.081 Tagesexporte (01.12.2023–15.11.2026), davon 876.421 Bekanntmachungen und 415.822 in den 11 Ländern | 5.075 Kandidaten (Ziel-CPV oder Leistungs-Fit ≥ 12) · 435 in den letzten 90 Tagen | 34 Ausschreibungen mit Fit ≥ 16; 13 mit offener Frist | – |
| **A gesamt** | – | – | **24 Datensätze in `03a`**: 1 × A, 15 × B, 8 × C | **10 ohne K.-o.**; die einzige A-Chance (Ladenbau Leinefelde-Worbis) ist K.-o., weil die Frist am 17.11.2026 endet |
| **B – privat** | Suchen über Plattformen, Franchise, Portale | 9 Kanäle | – | Tab „Privat“ (öffentlich findbare private Ausschreibungen gibt es praktisch nicht) |
| **C – Signale** | 728 Detailseiten neueroeffnung.info (Schneeball-Crawl) + rund 40 Websuchen | 426 Seiten in der Region; 369 relevant und aktuell; dazu 50 manuell recherchierte Signale | – | **419 Signale**: A 62, B 211, C 144 (in Stufe 1: A 23 / B 31 / C 19) |
| **D – Accounts** | 34.402 OSM-Lebensmittelgeschäfte (mit PLZ) → 15.272 Namensgruppen | 480 Zielkunden (390 mit Präsenz in Stufe 1) | – | **502 Accounts**: 480 Zielkunden, 4 Gatekeeper, 13 Wettbewerber, 3 Partner, 2 Projektentwickler |
| **E – Marktbild** | EHI, ZV Bäckerhandwerk, DFV, BMUKN, Kartellamt | eigene Berechnung des Beschaffungsvolumens aus OCDS | – | Tab „Marktbild“ |

## Stichproben gegen die Originalquelle

Je 5 Treffer pro Modul, zufällig gezogen (seed 7), am 17.11.2026 erneut abgerufen. Das Protokoll liegt in `work/stichproben.json`.

| Modul | ID | Geprüft | Ergebnis |
|---|---|---|---|
| A | A-25960856 (studierendenWERK BERLIN, Bautischler TU-Mensa) | Frist 19.11.2026 im eForms-XML | ✅ bestätigt |
| A | A-781744-2026 (Berliner Bäder-Betriebe, Möbeltischler) | Frist 15.12.2026 über die TED-API | ✅ bestätigt |
| A | A-25955982 (studierendenWERK BERLIN, Küchentechnik) | Frist 18.11.2026 | ✅ bestätigt |
| A | A-819b8d86 (Stadt Oldenburg, Einbaumöbel) | Frist 02.10.2026 | ✅ bestätigt (abgelaufen, korrekt als K.-o. markiert) |
| A | A-645288-2026 (SPSG Neues Palais, Tresen/Museumsshop) | Frist 20.10.2026 | ✅ bestätigt (abgelaufen) |
| C | C-N0118 (Hofbäckerei Klee, Hohenmocker) | PLZ 17111, Termin „4. Quartal 2027“ | ✅ bestätigt |
| C | C-N0389 (Großräschen) | PLZ 01983, Termin 19.11.2026 | ✅ bestätigt |
| C | C-N0086 (REWE Vellmar) | PLZ 34246, Termin „1. Quartal 2027“ | ✅ bestätigt |
| C | C-N0317 (Großenlüder) | PLZ 36110, Termin 05.11.2026 | ✅ bestätigt |
| C | C-M001 (EDEKA Engelhardt, Magdeburg) | Volksstimme-Artikel | ⚠️ teilweise bestätigt: Überschrift „NP wird Edeka … wird umgebaut“ ist sichtbar, der Artikeltext liegt hinter einer Bezahlschranke; Adresse und Datum belegt der zweite Beleg (neueroeffnung.info) |
| D | Bäcker Andresen | OSM-Objekt existiert, Name stimmt | ✅ bestätigt |
| D | Der Bäcker Feihl | dto. | ✅ bestätigt |
| D | mannamia | dto. | ✅ bestätigt |
| D | Bäckerei Düsedau | dto. | ✅ bestätigt |
| D | Lindner | dto. | ✅ bestätigt |

Modul B hat keine Einzeltreffer, deshalb gibt es dort keine Stichprobe. Modul E besteht aus Quellenangaben; jede Kennzahl im Tab „Marktbild“ hat einen Link.

## Fehler, Blockaden und Einschränkungen

1. **sigma-ladenbau.de nicht abrufbar.** Der Server setzt die TLS-Verbindung aus dem Rechenzentrum zurück, auch bei unbeschränktem Netz. Die Angaben im Firmenprofil stützen sich deshalb nur auf Auszüge aus dem Suchindex. Ungeprüft bleiben: „600 Projekte“, „35 Jahre“, das Hygiene-Spezialgebiet sowie mehrere Referenzkunden.
2. **Overpass-API und Geofabrik bauen die Verbindung ab.** Ersatzweg war der OSM-Deutschland-Auszug von openstreetmap.fr (5,9 GB, nach der Auswertung gelöscht).
3. **neueroeffnung.info:** Listen ab Seite 2 sind kostenpflichtig (Premium) und wurden nicht genutzt. Die Erfassung lief über öffentliche Detailseiten und deren Umgebungslinks. Folge: Die Abdeckung ist vollständig in der Nähe der Ausgangsseiten, aber **nicht flächendeckend**.
4. **OSM-Filialzahlen sind Untergrenzen.** Gezählt sind nur Objekte mit PLZ-Tag. Viele EDEKA-Märkte heißen in OSM nur „EDEKA“, deshalb sind die Kaufmannsnamen unvollständig.
5. **oeffentlichevergabe.de:** Nur rund 25 % der Zuschläge nennen einen Wert. Neun Ausreißer über 5 Mio. € (Gesamtwerte von Bauaufträgen mit einem Nebencode) habe ich ausgeschlossen. Das Beschaffungsvolumen ist daher eine bereinigte Untergrenze.
6. **TED-Zuschlagswerte im Tab „Marktbild“ sind unbereinigt**, z. B. 2025 mit 326,7 Mio. €. Sie enthalten Gesamtwerte von Bauaufträgen und dienen nur zur Einordnung.
7. **Nicht abgefragt** (kostenpflichtig, Registrierung oder automatisierter Zugriff untersagt): ibau, Infobau, BauInfoConsult, DTVP-/Vergabe24-Privatbereich, LinkedIn, Instagram, Facebook, Bundesanzeiger-Abschlüsse, Northdata-Detaildaten.
8. **CRM-Abgleich nicht möglich.** Kein CRM-Konnektor ist verbunden bzw. autorisiert.
9. **Bewertung:** Die Score-Gewichte sind wie vorgegeben. Kalibriert habe ich zwei Punkte: Gerüchte und Projekte mehr als 24 Monate in der Zukunft bekommen höchstens 10 Phasenpunkte; Neueröffnungen ohne Betreibernamen bekommen 18 statt 25 Punkte für den Segment-Fit. Der Leistungs-Fit der Ausschreibungen ist manuell nach Lektüre der Texte vergeben (`scripts/build_*` bzw. `FIT` in der Bewertungslogik).

## Reproduktion / erneuter Lauf

```bash
gunzip -k raw/**/*.gz              # komprimierte Rohdaten entpacken (osm, ted)
python3 scripts/build_signale.py   # 03b
python3 scripts/build_accounts.py  # 03c
python3 scripts/marktbild.py       # Volumen
python3 scripts/build_xlsx.py      # markterkundung_sigma.xlsx
python3 scout.py                   # inkrementell A + C, Diff-Report unter laeufe/JJJJ-MM-TT/
```

## Testlauf scout.py (17.11.2026)
`python3 scout.py --module A` lief erfolgreich: 5 neue Ausschreibungen, Diff-Report unter `laeufe/2026-11-17/diff_report.md`. Dieser erste Lauf ist die Ausgangsbasis für den Diff.
Hinweis: Die automatische Bewertung in scout.py nutzt den Relevanzfilter, keine manuelle Lektüre. Dadurch gibt es Fehltreffer, z. B. „Tischlerarbeiten Innentüren, Neubau und Mensa“ (Hannover) als A. Treffer der Klasse A vor einer Aktion deshalb immer im Original prüfen.
