# 04 – Qualitätsbericht (16.11.2026)

## Trichter je Modul
| Modul | Suchen (ca.) | Rohtreffer gesichtet | erfasst | davon verwertbar | Ergebnis |
|---|---|---|---|---|---|
| A – Öffentlich | 45 | ca. 400 Suchtreffer | 25 Treffer + 12 Zuschläge | 7 offen, 6 Frist unbekannt, 12 abgelaufen oder vermutlich abgelaufen | 3 A-Chancen offen (davon 1 unbestätigt) |
| B – Privat | 10 (Teil von B+C) | ca. 90 | 3 | 3 (alle Vertrauensgrad niedrig) | keine echte private Ausschreibung gefunden |
| C – Signale | 34 (Teil von B+C) | ca. 300 | 37 | 37 | 20 × A, 16 × B, 1 × C |
| D – Accounts/Wettbewerb | 50 | ca. 450 | 126 Accounts, 36 Wettbewerber, 11 Partner | 6 Bestandskunden ohne Beleg-URL | 6 × A, Rest B/C |
| E – Markt | 33 | ca. 300 | 74 Kennzahlen | 74 (Sekundärquellen markiert) | – |

## Fehler und Blockaden
1. **Netzwerk:** WebFetch, curl, TED-API, Bright Data und CRM-Verbindungen blockiert (Allowlist der Umgebung). Die Freigabeanfragen hat der Dienst abgelehnt. → Kein Volltext, keine API-Abfragen, kein eigenes Beschaffungsvolumen nach CPV.
2. **Suchbudget:** gemeinsames Limit für alle Subagenten pro Lauf erschöpft (siehe Abschnitt „Grenzen“ im Bericht).
3. **Aggregatoren** (it-ausschreibung.de, tendigo, vergabehero, ausschreibungen-deutschland): Fristen und Auftraggeber zum Teil nur im Snippet, teils widersprüchlich.
4. **Gewinner in Zuschlägen:** Bei keinem der 12 Zuschläge war der Gewinner im Snippet erkennbar.
5. **Heuristik im Scoring:** Frist unbekannt und Veröffentlichung älter als 45 Tage → „vermutlich abgelaufen“ (0 Punkte für Zeit). Regionale Zuordnung per Ortsliste (`build.py`).

## Stichprobe: 5 Treffer je Modul gegen die Quelle
Ein Abgleich mit dem Original war nicht möglich. Geprüft wurde deshalb durch eine **unabhängige zweite Websuche** bzw. den Vergleich mit dem Quell-Snippet. Status: ✅ bestätigt · ⚠️ teilweise · ❌ nicht bestätigt.

### Modul A
| ID | Prüfung | Ergebnis |
|---|---|---|
| A-004 OPTICUM-Möblierung | Zweitsuche (TED, LUH) | ⚠️ Projekt OPTICUM bestätigt (Wissenschaftsrat 2021, TED-Bauvergaben); **Möblierungs-Ausschreibung nur über tendigo**, Frist nicht unabhängig bestätigt |
| A-002 Burgdorf Schul-IT | Zweitsuche (TED) | ⚠️ Vorvertrag bestätigt (298.512 €, 3+1 Jahre, TED 015005-2023); Neuausschreibung 2026 nur über it-ausschreibung.de |
| A-003 Cloud-Kommunikation | Zweitsuche des Subagenten | ❌ nicht bestätigt (Vertrauensgrad niedrig, im Excel markiert) |
| A-013 LK Celle Palo Alto | Quell-Snippet (TED 449815-2026) | ✅ ISO-27001-Forderung im TED-Snippet |
| A-011 IT-Verbund Uelzen Citrix-Server | Quell-Snippet (TED 589283-2026) | ✅ Bekanntmachung vom 26.08.2026 bestätigt; Frist fehlt → vermutlich abgelaufen |

### Modul B
| ID | Prüfung | Ergebnis |
|---|---|---|
| B-001 | Snippet freelancermap | ⚠️ Projekt existiert, Datum/Status unbekannt |
| B-002 | Snippet freelancermap | ⚠️ wie B-001 |
| B-003 | Snippet freelancermap | ⚠️ wie B-001 |
| – | Suche nach privaten Ausschreibungen (Diakonie, Lebenshilfe, Kirchenkreise) | ❌ nicht im Suchindex; vermutlich nicht öffentlich ausgeschrieben |
| – | IHK-Kooperationsbörse | ❌ keine aktuellen Einträge gefunden |

### Modul C
| ID | Prüfung | Ergebnis |
|---|---|---|
| C-001 Volksbank-Fusion | Zweitsuche (Börsen-Zeitung) | ✅ Gespräche bestätigt; Name „Volksbank Bremen Lüneburger Heide“, ca. 8 Mrd. € Bilanzsumme, ca. 1.000 MA; noch kein Beschluss |
| C-036 Server 2016 | Microsoft-Lifecycle (Erweiterter Support endet 12.01.2027) | ✅ |
| C-035 NIS2 | Subagent: NIS2UmsuCG in Kraft seit 06.12.2025 | ⚠️ in mehreren Quellen konsistent, Original-BGBl. nicht geprüft |
| C-010 Heidekreis-Klinikum | Snippet | ⚠️ Fertigstellung 01/2027 laut Presse-Snippet |
| C-009 LK Lüneburg Dachausbau | Snippet | ⚠️ Zuordnung der Beleg-URL unsicher (vom Subagenten markiert) |

### Modul D
| Objekt | Prüfung | Ergebnis |
|---|---|---|
| TELCAT IT Services Uelzen | Zweitsuche | ✅ 25 MA in Uelzen, Telcat-Gruppe seit 2018; Übernahme von Exabyters bestätigt |
| hagel IT „CO2-neutrales RZ“ | Snippet | ⚠️ Eigenangabe des Wettbewerbers |
| Lebenshilfe Lüneburg-Harburg 41 Standorte | Snippet | ⚠️ |
| Bestandskunden Öko Korn, Gerald Peters, Hoppe, Wittig, mycity, Fachakademie | – | ❌ keine Beleg-URL (nur aus dem Briefing bzw. von der Website) |
| Stadtwerke Uelzen, SVO, WELLERGRUPPE | – | ⚠️ Beleg-URL fehlt oder ist unsicher (markiert) |

### Modul E
| Kennzahl | Prüfung | Ergebnis |
|---|---|---|
| Bitkom ITK-Markt 2026: 246,4 Mrd. €, +4,1 % | Zweitsuche | ✅ (Bitkom, 07.07.2026) |
| IT-Services +3,1 % | Zweitsuche | ⚠️ Teilmarktwert nicht eindeutig bestätigt |
| EnEfG: 300-kW-Schwelle, Ökostrom ab 2027 | Snippet | ⚠️ Novelle (Kabinett 24.06.2026) noch offen |
| NWertVO Niedersachsen: Direktauftrag bis 20 T€ | Snippet | ⚠️ ob die Grenzen für Kommunen gelten, ist ungeklärt |
| IBA Büromöbel 2024: 2,4 Mrd. € | Snippet | ⚠️ Sekundärquelle |

## Fazit
Die Daten taugen zur **Priorisierung und Gesprächsvorbereitung**. Vor jedem Angebot muss die Originalbekanntmachung geprüft werden. Der nächste Lauf sollte mit API-Zugriff erfolgen (`scout.py`, Hosts siehe `00_tools.md`).
