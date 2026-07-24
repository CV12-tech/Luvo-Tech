# Sentry — Brand Package

Überarbeitete B2B-Cybersecurity-Markenidentität für die bestehende G&R-Lösung ("Sentry —
powered by G&R Cybersecurity"). Der eingeführte Produktname **Sentry** wird beibehalten
(Entscheidungsdokumentation in `00-brand-strategy.md`, Abschnitt 0); überarbeitet wurden
Positionierung, Tone of Voice, Visual Identity und die inhaltlichen Compliance-Korrekturen.
Basiert ausschließlich auf dem bestätigten Faktenstand Juli 2026.

## Inhalt

| Datei | Inhalt |
|---|---|
| [`00-brand-strategy.md`](./00-brand-strategy.md) | Namensentscheidung, Positionierung, Tone of Voice, Messaging, Compliance-Korrekturen |
| [`01-visual-identity.md`](./01-visual-identity.md) | Farbpalette, Typografie, Logo-Guidelines, Iconografie, Bildsprache |
| [`assets/icon.svg`](./assets/icon.svg) | Icon-only Logo (Favicon/App-Icon) |
| [`assets/logo-dark-bg.svg`](./assets/logo-dark-bg.svg) | Vollmarke (Icon + Wordmark) für dunkle Hintergründe |
| [`assets/logo-light-bg.svg`](./assets/logo-light-bg.svg) | Vollmarke (Icon + Wordmark) für helle Hintergründe |
| [`landing-page/index.html`](./landing-page/index.html) | Vollständige, responsive Single-File-Landingpage (Tailwind CDN, zum lokalen Bearbeiten) |
| [`landing-page/dist/index.html`](./landing-page/dist/index.html) | Standalone-Build derselben Landingpage — Fonts & Styles inline, keine externen Abhängigkeiten (für Artifact-Links, Mailanhang, Offline-Hosting) |
| [`pitch-deck.md`](./pitch-deck.md) | 8-Slide Pitch Deck, Marp-kompatibel |
| [`exports/sentry-pitch-deck.pdf`](./exports/sentry-pitch-deck.pdf) / [`.pptx`](./exports/sentry-pitch-deck.pptx) | Gerenderte Pitch-Deck-Exporte |

## Landingpage lokal ansehen

Kein Build nötig — reines Static HTML mit Tailwind über CDN:

```bash
open brand/sentry/landing-page/index.html
# oder: python3 -m http.server -d brand/sentry/landing-page
```

## Pitch Deck rendern (Marp)

```bash
npx @marp-team/marp-cli brand/sentry/pitch-deck.md -o pitch-deck.pdf
# oder als HTML/PPTX:
npx @marp-team/marp-cli brand/sentry/pitch-deck.md -o pitch-deck.pptx
```

## Wichtiger Hinweis

Alle Aussagen sind bewusst auf den bestätigten Faktenstand begrenzt (siehe Faktenblatt Stand
Juli 2026). Insbesondere **keine** Zertifizierungs-Behauptungen (ISO 27001/BSI) und **keine**
24/7-SLA-Zusagen außerhalb einer klar gekennzeichneten Partner-Option. Vor Veröffentlichung:
Rücksprache mit G&R Cybersecurity sowie markenrechtliche Prüfung des gewählten Namens.
