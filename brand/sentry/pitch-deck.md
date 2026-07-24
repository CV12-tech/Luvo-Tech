---
marp: true
theme: default
paginate: true
backgroundColor: "#020617"
color: "#E2E8F0"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
  section {
    font-family: 'Inter', 'Space Grotesk', ui-sans-serif, system-ui, sans-serif;
    padding: 64px 72px;
  }
  h1, h2 {
    font-family: 'Space Grotesk', ui-sans-serif, system-ui, sans-serif;
    color: #F8FAFC;
    letter-spacing: -0.02em;
  }
  h1 { font-size: 2.1em; }
  h2 { font-size: 1.5em; border-bottom: 1px solid #1E293B; padding-bottom: 0.3em; }
  strong { color: #34D399; }
  code, pre { font-family: 'JetBrains Mono', ui-monospace, monospace; }
  a { color: #34D399; }
  table { font-size: 0.75em; }
  th { color: #94A3B8; }
  section.title {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  section.title h1 { font-size: 2.6em; }
  .tag {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 0.55em;
    color: #64748B;
    letter-spacing: 0.15em;
    text-transform: uppercase;
  }
  .callout {
    border-left: 3px solid #F59E0B;
    background: rgba(245, 158, 11, 0.08);
    padding: 0.7em 1em;
    border-radius: 6px;
    font-size: 0.85em;
    color: #FCD9A8;
  }
---

<!-- _class: title -->

<span class="tag">Powered by G&R Cybersecurity</span>

# sentry

## Sichtbarkeit für dein Netzwerk — ohne SOC-Overhead.

Pragmatische Netzwerk-Anomalie-Erkennung als Plug-and-Play-Sensor.
Aufgestellt in < 5 Minuten. Kein Fernzugriff. Datensparsam by design.

---

## Das KMU-Sicherheits-Dilemma

Interner Netzwerkverkehr ist für die meisten KMU und Sozialeinrichtungen
**komplett unsichtbar** — bis etwas schiefgeht.

- Volle SIEM/SOC-Stacks verlangen Personal für Regelpflege, Auswertung, Triage
- Solche Projekte sprengen Budget **und** Zeitplan kleiner IT-Teams
- Portscans, Lateral Movement, verdächtige externe Verbindungen bleiben unbemerkt
- Klassische Fernwartungs-Tools schaffen selbst zusätzliche Angriffsfläche

**Ergebnis:** Ein blinder Fleck genau dort, wo Angriffe sich am längsten unbemerkt bewegen —
im internen Netz.

---

## Die Lösung: Plug-and-Play IDS Sensor

**sentry** ist ein hardware-basierter Netzwerksensor für Intrusion Detection &
Anomaly Detection — konzipiert für Organisationen, die heute **keine** Sichtbarkeit
in ihren internen Traffic haben.

- Hardware-agnostisch konzipiert, im Einsatz: **Raspberry Pi 5 (4 GB RAM)**
- Anbindung per **Port-Mirroring** am Master-Switch
- Aufbau **in der Regel ≤ 5 Minuten**, meist ein Gerät pro Standort
- **Kein Fernzugriff** auf das Gerät — Konfiguration liegt lokal auf SD-Karte

<div class="callout">
Kein Deception-System mit voller Layer-7-Nachbildung: offene Ports dienen als
Ablenkpunkte ohne dahinterliegenden Service.
</div>

---

## Funktionsweise

1. **Port-Mirroring** — der Sensor sieht nur den Traffic, der auf ihn selbst
   gespiegelt wird (nicht den vollständigen SPAN-Verkehr im weiteren Sinne)
2. **Statistische Anomalie-Erkennung** — Erwartungswerte für Traffic werden
   statistisch gebildet, ergänzt um feste Regeln (kein klassisches ML/Deep Learning)
3. **Reputations- & Musterabgleich** — Hochrisiko-Verbindungen (z. B. TOR) werden
   über feste Regeln plus externe/interne Reputationsdaten erkannt
4. **Zero-Remote-Attack-Surface** — keine Fernkonfiguration; Updates laufen
   automatisiert über einen auf der SD-Karte festgelegten Release-Channel

<div class="callout">
"Regel-Treffer" ≠ "bestätigter Vorfall". sentry bewertet nicht, ob ein Treffer
ein echter Angriff ist — das bleibt bewusst beim Kunden bzw. Reseller.
</div>

---

## Reseller & MSP Opportunities

**Erklärtes Ziel:** wenig eigene Dienstleistung, Fokus auf Produkt — die Bühne
gehört den Partnern.

- **Recurring Revenue:** Fixpreis + Preis pro Gerät und Jahr als Basis für
  wiederkehrenden Umsatz bei euren Bestandskunden
- **White-Labeling** möglich — Auftritt unter eigener Marke
- **Erstreaktion beim Partner:** ihr entscheidet über Triage & Eskalation,
  sentry liefert das Signal
- **Multi-Tenant-Plattform** — selbst hostbar oder gehostet, je nach Bedarf
- **Informelles, schnelles Onboarding** in der Startphase statt formaler
  Zertifizierungspflicht (strukturierte Programme folgen mit wachsender Partneranzahl)

---

## Privacy & Architecture

- **AVV nach Art. 28 DSGVO** liegt als Muster vor
- **Datenverarbeitung:** standardmäßig Cloud, alternativ vollständiges
  **On-Premises-Hosting** beim Kunden möglich
- **SD-Karten-Setup:** Konfiguration wird vorbereitet, vor Ort installiert,
  bei Bedarf lokal entnommen und bearbeitet — kein Fernzugriff, auch nicht durch uns
- Es werden **praktisch keine personenbezogenen Daten** verarbeitet

<div class="callout">
Transparenz statt Greenwashing: aktuell liegen <strong>keine</strong> geprüften
Zertifizierungen (ISO 27001 / BSI IT-Grundschutz) vor. Keine DSFA, keine
auditfähige Versicherer-Dokumentation. Wir kommunizieren das offen.
</div>

---

## Plug & Play Onboarding

**In der Regel betriebsbereit in 5 Minuten.**

| Schritt | Ablauf |
|---|---|
| 1. Vorbereitung | Konfiguration wird vorab auf SD-Karte vorbereitet |
| 2. Installation | Sensor am Master-Switch per Port-Mirroring anbinden |
| 3. Inbetriebnahme | Gerät startet automatisch, in der Regel ≤ 5 Minuten |
| 4. Updates | Automatisiert über festgelegten Release-Channel |
| 5. Hardwaredefekt | Austauschgerät statt Vor-Ort-Reparatur |

Kein Rollout-Projekt, kein Consulting-Aufwand für den Reseller — Hardware
aufstellen, fertig.

---

<!-- _class: title -->

# Let's talk.

## Reseller-Partner werden oder Demo anfordern

**G&R Cybersecurity**
Leopoldstraße 31, 80802 München

office@gr-sec.com &nbsp;·&nbsp; +49 89 189170715 &nbsp;·&nbsp; www.gr-sec.com

<span class="tag">sentry — powered by G&R Cybersecurity · Stand Juli 2026</span>
