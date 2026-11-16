# 02 – Quellenplan (Stand 16.11.2026)

Zugriff in diesem Lauf: **nur WebSearch** (siehe 00_tools.md). Spalte „Soll-Zugriff“ = Weg für spätere Läufe mit freigegebenen Hosts (scout.py).

| Modul | Prio | Quelle | Soll-Zugriff | Ist-Zugriff | Filter |
|---|---|---|---|---|---|
| A | 1 | TED (ted.europa.eu) | API v3 `POST /v3/notices/search` | WebSearch `site:ted.europa.eu` | CPV-Liste, buyer-country=DEU, NUTS DE9*, DE60, DEE0, DE80, DE50; publication-date ≥ 18.08.2026 |
| A | 1 | oeffentlichevergabe.de (Datenservice) | OCDS-/eForms-Export (API) | WebSearch | CPV, NUTS, Datum |
| A | 1 | Vergabeplattform Niedersachsen (vergabe.niedersachsen.de) | HTTP/RSS | WebSearch | IT, Möbel, Kopierer |
| A | 1 | DTVP, Vergabe24, subreport/ELViS, evergabe.de, cosinex-Marktplätze | HTTP (Suchseiten) | WebSearch | Region, Keywords |
| A | 2 | service.bund.de, evergabe-online.de | RSS/HTTP | WebSearch | Keywords |
| A | 2 | Hamburg (Bieterportal), eVergabe LSA, Vergabe-MV, e-Vergabe SH, Bremen | HTTP | WebSearch | Keywords |
| A | 2 | Kommunen der Kernregion (Websites, Ausschreibungsseiten) | HTTP | WebSearch | „Ausschreibung“ + Kommune |
| A | 2 | Rahmenverträge: Kaufhaus des Bundes, LZN, IT.Niedersachsen, KDO, ITEOS | manuell | WebSearch | IT, Möbel, MFP |
| A | 3 | Zuschläge, letzte 5 Jahre (TED-Vergabebekanntmachungen) | API | WebSearch (stichprobenartig) | CPV × Kernregion |
| B | 2 | Private Plattformen (Vergabe24/DTVP Privat, subreport, wlw, Ariba Discovery, Onventis) | manuell (AGB) | WebSearch | Keywords |
| B | 2 | Sozialträger, Kirchenkreise, Diakonie (eigene Ausschreibungen) | HTTP | WebSearch | IT-Dienstleister, Möbel |
| B | 3 | Projektbörsen (freelancermap, GULP, freelance.de, Malt) | manuell | WebSearch | Admin/M365/Migration Nord |
| B | 3 | IHK Lüneburg-Wolfsburg, HWK, WiSU, Süderelbe AG, EEN | manuell | WebSearch | Kooperationsgesuche |
| C | 1 | Ratsinformationssysteme der Kernregion | HTTP (ALLRIS/SessionNet) | WebSearch | IT, Digitalisierung, Neubau, Haushalt |
| C | 1 | Lokalpresse (AZ Uelzen, LZ Lüneburg, Cellesche Zeitung, Kreiszeitung Wochenblatt) | HTTP/RSS | WebSearch | Neubau, Umzug, Fusion, Cyberangriff |
| C | 2 | Förderung (NBank, Digitalpakt, EFRE-Transparenzliste) | Download | WebSearch | Kernregion |
| C | 2 | Handelsregister-Bekanntmachungen | Portal (manuell) | WebSearch/Northdata-Snippets | Verschmelzung, Sitzverlegung |
| C | 2 | Stellenanzeigen (BA-Jobbörse API, StepStone) | BA-API | WebSearch | IT-Admin/IT-Leitung, Kernregion |
| C | 3 | Sicherheitsvorfälle (Presse, BSI) | RSS | WebSearch | Norddeutschland |
| D | 1 | Zielkunden: Northdata, IHK, Verbände, Kammern | API/HTTP | WebSearch | Segmente, Kernregion |
| D | 1 | Wettbewerber: Websites, Zuschläge, Stellen | HTTP | WebSearch | Region |
| E | 2 | Bitkom, Destatis, Lünendonk, IBA, GCB/EITW | HTTP/PDF | WebSearch | Kennzahlen 2025/2026 |

Rechtlicher Rahmen: nur öffentlich zugängliche Daten, keine Registrierung oder Anmeldung, Plattform-AGB beachten (Vergabe24/DTVP/Ariba nur manuell referenzieren), Personen nur in beruflicher Rolle.
