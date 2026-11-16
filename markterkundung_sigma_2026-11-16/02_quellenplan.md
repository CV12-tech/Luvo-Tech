# 02 – Quellenplan (Stand 16.11.2026)
Priorität: P1 = sofort, P2 = nach P1, P3 = optional · Stufe gemäß 02a · Zugang: API / Export / HTTP / Suche / manuell
**Aktueller Netzstatus:** Nur WebSearch funktioniert. Spalte „ohne Netz“ = Ersatzweg über die Websuche.

## Modul A – Öffentliche Ausschreibungen
| Quelle | P | Stufe | Zugang | Filter | ohne Netz |
|---|---|---|---|---|---|
| TED API v3 (api.ted.europa.eu) | P1 | 1–3 | API | CPV laut Profil × NUTS (11 Länder) × 90 Tage + offene Fristen; Zuschläge 5 J. | ✖ (nur Einzeltreffer über Suche) |
| oeffentlichevergabe.de (Datenservice, auch unterschwellig) | P1 | 1–3 | API/Export | wie TED | ✖ |
| service.bund.de, evergabe-online.de | P2 | 1–3 | HTTP/RSS | Keywords Kantine, Truppenküche, Cafeteria, Ladeneinrichtung | Suche |
| eVergabe ST, Vergabemarktplatz BB, Vergabeplattform Berlin | P1 | 1 | HTTP | Keywords + CPV | Suche |
| sachsen-vergabe.de, Thüringen, NI-Plattform | P2 | 2 | HTTP | ab Klasse B | Suche |
| Vergabe-MV, HH, SH (e-Vergabe SH), HB, HAD Hessen | P3 | 3 | HTTP | nur Klasse A | Suche |
| DTVP, Vergabe24, subreport, cosinex | P2 | 1–3 | HTTP (teils Registrierung) | Keywords | Suche; Registrierung nur markieren |
| Auftraggeber-Liste: Studierendenwerke (11 Länder), Unikliniken, Landtage, Zoos/Schlösser, Kommunen mit Dorfläden | P1 | 1–3 | Suche + Portale | Mensa, Cafeteria, Shop, Ausgabe | Suche |

## Modul B – Private Ausschreibungen & Projektanfragen
| Quelle | P | Stufe | Zugang | ohne Netz |
|---|---|---|---|---|
| ibau, Infobau, BauInfoConsult (Gewerk Ladenbau/Innenausbau) | P2 | 1–3 | Registrierung → nur referenzieren | Suche |
| Lieferantenportale: Schwarz-Gruppe, EDEKA (MH, Nord, NST, Hessenring), REWE, Globus, Netto, Bio Company, Denns, tegut | P1 | 1–3 | HTTP/manuell | Suche |
| Expansionsseiten von Bäckerei-/Café-/Snackketten und Tankstellenbetreibern | P1 | 1–3 | HTTP | Suche |
| GU und Projektentwickler für Nahversorgungszentren | P2 | 1–3 | HTTP/Presse | Suche |
| IHKs, HWKs, Bäcker- und Fleischerinnungen, Handelsverbände der 11 Länder | P3 | 1–3 | manuell | Suche |
| **Hanse-Ladenbau-Insolvenz** (Insolvenzbekanntmachungen, Verwalterin, Presse) | P1 | 1–3 | HTTP | Suche ✔ |

## Modul C – Projekt- & Bedarfssignale (Hauptmodul)
| Quelle | P | Stufe | Zugang | ohne Netz |
|---|---|---|---|---|
| **EDEKA-Regionalpresse** (verbund.edeka MH, Nord, NST, Hessenring): Eröffnungen, Kaufmannswechsel, Existenzgründungen | P1 | 1–3 | HTTP/PDF | Suche ✔ (sehr ergiebig) |
| REWE-, Kaufland-, Netto-, Globus-Eröffnungsmeldungen | P1 | 1–3 | HTTP | Suche ✔ |
| Lokalpresse: Volksstimme, MZ, MOZ, MAZ, Tagesspiegel, LVZ, SZ, TA/OTZ, NDR, OZ, SVZ, KN, HAZ, NOZ, HNA, HNA | P1/P2 | 1–3 | HTTP | Suche ✔ |
| Fachpresse: Lebensmittel Praxis, LZ, Rundschau, ABZ, afz | P2 | 1–3 | HTTP | Suche ✔ |
| Ratsinfo-Systeme: B-Pläne „SO Einzelhandel/Nahversorgung“ in Ober- und Mittelzentren Stufe 1 | P2 | 1 | HTTP (Volltextsuche) | Suche (eingeschränkt) |
| Handelsregister-Neueintragungen „… Markt GmbH“, „… e.K. Lebensmittel“ | P2 | 1–2 | Northdata/HR | ✖ |
| Insolvenzbekanntmachungen Bäckereien/Fleischereien/Handel | P1 | 1–3 | HTTP | Suche ✔ |
| Stellenanzeigen „Neueröffnung“, „neue Filiale“ | P2 | 1–2 | HTTP | Suche ✔ |
| Förderung: LEADER/ELER-Dorfläden, GRW/EFRE Lebensmittelhandwerk, BAFA/KfW EEW | P2 | 1–3 | HTTP/Listen | Suche ✔ |
| Ansiedlungen (Betriebsgastronomie), neue Wohnquartiere | P3 | 1–2 | Presse | Suche ✔ |

## Modul D – Zielkunden & Wettbewerb
| Quelle | P | Stufe | Zugang | ohne Netz |
|---|---|---|---|---|
| Marktfinder EDEKA/REWE/Kaufland/nah&gut/CAP/Konsum | P2 | 1–2 | HTTP | ✖ |
| Google-Maps-Filialnetze (Bright Data data-feeds) | P3 | 1–2 | Skill | ✖ (kein Login) |
| Northdata/Bundesanzeiger (Größe, Inhaber) | P2 | 1–3 | HTTP | ✖ |
| Wettbewerber: Websites, Referenzen, Messen (EuroShop, iba, Internorga, SÜFFA) | P1 | 1–3 | HTTP | Suche ✔ |
| Partner: Kälte, Montage, Elektro, Tischlerei je Stufe | P2 | 1–3 | HTTP/Verzeichnisse | Suche ✔ |

## Modul E – Marktbild
| Quelle | P | Zugang | ohne Netz |
|---|---|---|---|
| EHI (Ladenbau, Investitionen), HDE, Verband Ladenbau (dlv) | P1 | HTTP/Presse | Suche ✔ |
| ZV Bäckerhandwerk, DFV, Statistische Landesämter (Betriebszahlen je Land) | P1 | HTTP | Suche ✔ |
| Beschaffungsvolumen aus TED/oeffentlichevergabe.de selbst berechnet | P1 | API | ✖ |
| F-Gase VO 2024/573, Förderprogramme (BAFA/KfW, Länder) | P1 | HTTP | Suche ✔ |

## Compliance
Es gelten robots.txt und AGB der Plattformen; Inhalte hinter Registrierung werden nur referenziert. Personen werden nur in ihrer beruflichen Rolle und nur dann aufgeführt, wenn sie öffentlich genannt sind; selbstständige Kaufleute stehen als „Inhaber/Kaufmann“ mit dem Marktnamen in den Daten.
