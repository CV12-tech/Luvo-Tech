# 00 – Werkzeuge & Zugriffswege (Stand 16.11.2026, Europe/Berlin)

## Inventur
| Werkzeug | Status | Bemerkung |
|---|---|---|
| WebSearch | ✅ verfügbar | einziger funktionierender Webzugang; liefert Titel, URL und Kurzsynthese |
| WebFetch | ❌ blockiert | DNS/Allowlist: wolkenhof.com, ted.europa.eu, wirtschaftsforum.de nicht erlaubt |
| curl/requests (Bash) | ❌ blockiert | Proxy antwortet 403 auf CONNECT (gleiche Allowlist) |
| TED API v3 / oeffentlichevergabe.de API | ❌ blockiert | Host nicht in Allowlist |
| brightdata-plugin:* (Skills) | ❌ nicht nutzbar | brauchen Bright-Data-API (Host blockiert, kein MCP verbunden) |
| scrapling-official, Playwright/Chromium | ⚠️ installiert, aber ohne Netz nutzlos | gleiche Allowlist |
| sales:* MCPs (Apollo, Crunchbase, HubSpot, Salesforce, ZoomInfo …) | ❌ Verbindung fehlgeschlagen | Proxy 403 |
| CRM | ❌ keins verbunden | kein Abgleich möglich |
| Python (openpyxl, pyyaml, requests) | ✅ | lokale Auswertung, xlsx, scout.py |
| xlsx / docx / pdf Skills | ✅ | Ausgabe |

Versuchte Freigabe (neue Umgebung bzw. Allowlist-Erweiterung der Default-Umgebung) wurde vom Environments-Dienst abgelehnt.

## Werkzeug-Hierarchie (Soll → Ist)
Soll: offizielle API > Export/RSS > HTTP-Abruf > Scraping-Skill > Browser.
Ist in diesem Lauf: **nur WebSearch** (Suchindex-Snippets). Folgen:
- Keine Volltexte von Bekanntmachungen/Vergabeunterlagen; Fristen, Werte und Lose nur soweit im Snippet sichtbar → jeder Treffer mit Vertrauensgrad.
- Keine systematische API-Abfrage (TED/oeffentlichevergabe.de) → Modul A unvollständig, Beschaffungsvolumen (Modul E) nicht selbst berechenbar.
- `scout.py` wird für API-Zugriff geschrieben, ist hier aber nicht ausführbar.

## Benötigte Freigaben (für vollständigen Lauf)
In den Umgebungseinstellungen (Network access → Allowed domains) mindestens:
wolkenhof.com, api.ted.europa.eu, ted.europa.eu, oeffentlichevergabe.de, vergabe.niedersachsen.de, www.dtvp.de, www.evergabe-online.de, www.service.bund.de, www.vergabe24.de, www.subreport.de, www.northdata.de, www.handelsregister.de, www.az-online.de, www.landeszeitung.de, Ratsinfo-Hosts der Kommunen.
Doku: https://code.claude.com/docs/en/cloud-environments#network-access
