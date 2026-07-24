# Greyline — Brand Package

Neue B2B-Cybersecurity-Marke für die bestehende G&R-Sentry-Lösung ("Greyline — powered by
G&R Cybersecurity"). Basiert ausschließlich auf dem bestätigten Faktenstand Juli 2026.

## Inhalt

| Datei | Inhalt |
|---|---|
| [`00-brand-strategy.md`](./00-brand-strategy.md) | Namensfindung (3 Optionen + Favorit), Positionierung, Tone of Voice, Messaging, Compliance-Korrekturen |
| [`01-visual-identity.md`](./01-visual-identity.md) | Farbpalette, Typografie, Logo-Guidelines, Iconografie, Bildsprache |
| [`assets/icon.svg`](./assets/icon.svg) | Icon-only Logo (Favicon/App-Icon) |
| [`assets/logo-dark-bg.svg`](./assets/logo-dark-bg.svg) | Vollmarke (Icon + Wordmark) für dunkle Hintergründe |
| [`assets/logo-light-bg.svg`](./assets/logo-light-bg.svg) | Vollmarke (Icon + Wordmark) für helle Hintergründe |
| [`landing-page/index.html`](./landing-page/index.html) | Vollständige, responsive Single-File-Landingpage (Tailwind CDN) |
| [`pitch-deck.md`](./pitch-deck.md) | 8-Slide Pitch Deck, Marp-kompatibel |

## Landingpage lokal ansehen

Kein Build nötig — reines Static HTML mit Tailwind über CDN:

```bash
open brand/greyline/landing-page/index.html
# oder: python3 -m http.server -d brand/greyline/landing-page
```

## Pitch Deck rendern (Marp)

```bash
npx @marp-team/marp-cli brand/greyline/pitch-deck.md -o pitch-deck.pdf
# oder als HTML/PPTX:
npx @marp-team/marp-cli brand/greyline/pitch-deck.md -o pitch-deck.pptx
```

## Wichtiger Hinweis

Alle Aussagen sind bewusst auf den bestätigten Faktenstand begrenzt (siehe Faktenblatt Stand
Juli 2026). Insbesondere **keine** Zertifizierungs-Behauptungen (ISO 27001/BSI) und **keine**
24/7-SLA-Zusagen außerhalb einer klar gekennzeichneten Partner-Option. Vor Veröffentlichung:
Rücksprache mit G&R Cybersecurity sowie markenrechtliche Prüfung des gewählten Namens.
