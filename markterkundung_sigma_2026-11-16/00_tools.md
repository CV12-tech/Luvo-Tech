# 00 – Werkzeuge und Zugriffswege (Stand 16.11.2026, Europe/Berlin)

## Werkzeug-Hierarchie (Soll)
offizielle API > Datenexport/RSS > HTTP-Abruf > Scraping-Skill > Browser-Automatisierung

## Ist-Zustand in dieser Sitzung

| Werkzeug | Status | Bemerkung |
|---|---|---|
| **WebSearch** (serverseitig) | ✅ funktioniert | einziger offener Webkanal; liefert Titel, URL und Auszüge aus dem Suchindex (teils veraltet, z. B. sigma-ladenbau.de vor ca. 555 Tagen indexiert) |
| WebFetch | ❌ blockiert | Hosts außerhalb der Netzwerk-Allowlist lösen nicht auf (ENOTFOUND) |
| curl / python requests / Playwright (Container) | ❌ blockiert | Egress-Proxy lehnt CONNECT ab (403) für alle Zielhosts (sigma-ladenbau.de, TED-API, oeffentlichevergabe.de, Northdata, Vergabeportale, Presse) |
| TED API v3, oeffentlichevergabe.de API | ❌ blockiert | wäre Stufe 1 (offizielle API) für Modul A und E |
| Bright Data (search, scrape, data-feeds, discover-api) | ❌ nicht nutzbar | erfordert `bdata` CLI und Login; api.brightdata.com blockiert, kein Zugangsschlüssel |
| chrome-browser / built-in-browser | ❌ nicht nutzbar | gleiche Netzsperre |
| sales:* MCP (Apollo, Clay, Crunchbase, HubSpot, Salesforce, ZoomInfo …) | ❌ nicht verbunden | MCP-Verbindung scheitert (Proxy 403); kein CRM-Abgleich möglich |
| Python 3 + openpyxl, pandas, pyyaml, requests, bs4 | ✅ | für Normalisierung, Scoring, xlsx, scout.py |
| Skills xlsx, docx, pdf, data:* | ✅ | für Auswertung und Ausgabe |

## Versuche, das Netz freizugeben
- `create_environment` (persönliche Umgebung mit 20 Hosts) → vom Umgebungsdienst 3× abgelehnt, ohne Begründung
- `update_environment` (20 Hosts in der Default-Umgebung) → abgelehnt

**Lösung für dich:** In der Cloud-Umgebung (Titelleiste der Sitzung → Umgebung → Bearbeiten → Network access)
entweder **„Full/Unrestricted“** wählen oder mindestens diese Domains erlauben:
sigma-ladenbau.de, www.sigma-ladenbau.de, api.ted.europa.eu, ted.europa.eu, oeffentlichevergabe.de,
www.northdata.de, www.bundesanzeiger.de, www.service.bund.de, www.evergabe-online.de, www.dtvp.de,
vergabemarktplatz.brandenburg.de, www.berlin.de, www.evergabe.sachsen-anhalt.de, www.sachsen-vergabe.de,
verbund.edeka, www.volksstimme.de, www.mz.de, lebensmittelpraxis.de, www.lebensmittelzeitung.net, www.handelsregister.de.
Doku: https://code.claude.com/docs/en/cloud-environments#network-access

## Konsequenz für die Methodik (bis zur Freigabe)
- Alle Belege kommen aus WebSearch-Ergebnissen (Quell-URL + Index-Auszug). Belegqualität wird als **„Index-Auszug, Originalseite nicht abgerufen“** markiert.
- Modul A: keine API-Abfragen (TED, oeffentlichevergabe.de); nur über Suchindex auffindbare Bekanntmachungen und Aggregatoren (z. B. tendigo.de) → Abdeckung deutlich unvollständig.
- Modul E: öffentliches Beschaffungsvolumen ist ohne TED-API nicht selbst berechenbar.
- Rate-Limit: ca. 4 parallele Suchen pro Runde.

## Nachtrag 16.11.2026, ca. 21:30 Uhr – Netz freigegeben (Unrestricted)
- Funktioniert: TED API v3, oeffentlichevergabe.de (API), Volksstimme, Northdata, verbund.edeka (teilweise), neueroeffnung.info, openplzapi.org, OSM-API, download.openstreetmap.fr, Playwright/Chromium
- Weiterhin **nicht erreichbar** (der Server setzt die TLS-Verbindung zurück, vermutlich eine Sperre gegen Rechenzentrums-IPs): **sigma-ladenbau.de**, overpass-api.de, download.geofabrik.de
- WebFetch (serverseitig) verwendet die alte Allowlist → ersetzt durch eigenen HTTP-Abruf `scripts/fetch.py` mit Ablage der Rohdaten
- Tatsächliche Hierarchie: offizielle API (TED, oeffentlichevergabe.de, OpenPLZ) > Datenexport (OSM-PBF) > HTTP-Abruf (fetch.py) > Websuche (Discovery) > Browser (Playwright, nur bei Bedarf)
