# Sentry — Visual Identity & Design Guidelines

Begleitdokument zu `00-brand-strategy.md`. Referenz-Logo liegt in `assets/logo.svg`
(Vollmarke) und `assets/icon.svg` (Icon-only, für Favicon/App-Icons).

---

## 1. Markenidee in Bildsprache

Das Icon ist eine **Signal-/Wellenlinie**: eine ruhige Baseline, die einmal ausschlägt — die
grafische Übersetzung von "statistischer Erwartungswert vs. Anomalie". Keine Schilde, keine
Adler, keine Schloss-Icons — das Motiv bleibt technisch und nah am tatsächlichen Produkt
(Traffic-Graph), nicht an Security-Klischees.

---

## 2. Farbpalette

Basis: Tailwind-Farbwerte, damit die Palette 1:1 in Tailwind-Config oder CDN-Klassen nutzbar ist.

### Primärfarben

| Rolle | Name | Hex | Tailwind-Referenz |
|---|---|---|---|
| Hintergrund / Basis | Obsidian | `#020617` | `slate-950` |
| Fläche / Cards | Deep Navy | `#0B1120` | custom (zwischen `slate-950`/`slate-900`) |
| Fläche erhöht | Navy Elevated | `#111827` | `gray-900` |
| Primär-Akzent | Cyber Emerald | `#10B981` | `emerald-500` |
| Akzent hell | Neon Mint | `#34D399` | `emerald-400` |
| Akzent-Glow | Mint Glow | `#6EE7B7` | `emerald-300` |

### Neutrale/Text

| Rolle | Name | Hex | Tailwind-Referenz |
|---|---|---|---|
| Text primär (auf dunkel) | Off-White | `#F8FAFC` | `slate-50` |
| Text sekundär | Slate | `#94A3B8` | `slate-400` |
| Text tertiär / Meta | Slate Dim | `#64748B` | `slate-500` |
| Rahmen/Trenner | Line | `#1E293B` | `slate-800` |

### Statusfarben (bewusst sparsam, nie als Hype-Signal)

| Rolle | Hex | Tailwind | Verwendung |
|---|---|---|---|
| Info | `#38BDF8` | `sky-400` | neutrale Systemmeldungen |
| Regel-Treffer (nicht "Alarm=Angriff"!) | `#F59E0B` | `amber-500` | Pattern-Match, unbewertet |
| Hochrisiko-Reputation (z. B. TOR) | `#F87171` | `red-400` | nur für definierte Hochrisiko-Regeln |

**Prinzip:** Rot wird ausschließlich für die tatsächlich definierten Hochrisiko-Regeln (z. B.
TOR-Reputationstreffer) verwendet — nicht als generisches "Gefahr"-Rot für jede Anomalie. Das
hält die Farbsprache ehrlich zur eigentlichen Aussage ("Regel X hat ausgelöst", nicht "Angriff
bestätigt").

### Tailwind-Config-Snippet

```js
// tailwind.config.js (Ausschnitt)
colors: {
  obsidian: '#020617',
  navy: { DEFAULT: '#0B1120', elevated: '#111827' },
  emerald: { glow: '#6EE7B7' }, // ergänzt Tailwinds emerald-Skala
}
```

---

## 3. Typografie

| Zweck | Font | Fallback-Stack |
|---|---|---|
| Headlines / Display | **Space Grotesk** (500/700) | `'Space Grotesk', ui-sans-serif, system-ui` |
| Fließtext / UI | **Inter** (400/500) | `Inter, ui-sans-serif, system-ui` |
| Daten, Logs, Specs, Code | **JetBrains Mono** (400/500) | `'JetBrains Mono', ui-monospace, monospace` |

**Update:** Die Display-Schrift wurde von Plus Jakarta Sans auf **Space Grotesk** umgestellt —
kantigere, geometrische Formen (u. a. die charakteristische offene "G"-Form) wirken technischer
und zeitgemäßer als die eher freundlich-rundliche Plus Jakarta Sans und passen besser zu einer
Security-Marke, die auf Nüchternheit statt Zugänglichkeit setzt.

- Headlines immer **satzweise klein geschrieben oder Sentence case** — keine durchgehenden
  Großbuchstaben-Wände (wirkt schnell reißerisch/marktschreierisch, widerspricht "No-BS"-Ton).
  Ausnahme: kurze Labels/Badges (z. B. `LIVE`, `NEW`) dürfen Caps + Letter-Spacing nutzen.
- Technische Werte (IP-Adressen, Portnummern, Zeitangaben wie "< 5 Min") immer in Mono setzen —
  unterstreicht die "wir zeigen echte Daten, keine Marketing-Zahlen"-Haltung.

---

## 4. Logo

### Aufbau
- **Icon:** abgerundetes Quadrat (Radius ~22 % der Kantenlänge) in Obsidian/Navy als Badge,
  darin eine monoline Signalkurve in Neon Mint (`#34D399`), ein Ausschlag hervorgehoben.
- **Wordmark:** `sentry` in Plus Jakarta Sans SemiBold, durchgängig kleingeschrieben (bewusst
  kein CamelCase, kein Ausrufezeichen-Energy) — signalisiert Nüchternheit statt Startup-Hype.
- **Lockup:** Icon + Wordmark horizontal, optional mit Mono-Suffix `SECURITY` klein darunter/
  daneben für Erstnennungen (z. B. Website-Header, erste Slide).

### Varianten
1. **Full color** (Standard) — Navy-Badge + Mint-Linie + helle Wordmark. Für helle & dunkle
   Hintergründe geeignet, solange genug Kontrast besteht.
2. **Reversed/Mono-Light** — komplett in Off-White, für dunkle/fotografische Hintergründe.
3. **Mono-Dark** — komplett in Obsidian, für helle Hintergründe/Print ohne Farbdruck.
4. **Icon-only** — für Favicon, App-Icons, Social-Avatar, Gerätesticker auf dem Sensor selbst.

### Schutzraum & Mindestgröße
- Schutzraum rundum ≥ Höhe des Icon-Badges (·1×).
- Mindestgröße Lockup: 96 px Breite (digital) / 24 mm (Print).
- Mindestgröße Icon-only: 24 px (Favicon-Grenze).

### Don'ts
- Icon nicht neu einfärben außerhalb der definierten Varianten.
- Wordmark nicht in Versalien setzen.
- Kein Drop-Shadow, kein 3D-Bevel, kein Glow-Filter über die definierte Mint-Farbe hinaus.
- Icon nicht ohne Wordmark in Erstkontakt-Materialien (Pitch Deck Titel, Homepage) verwenden.

---

## 5. Iconographie & UI-Stil

- Line-Icons, 1.5–2 px Stroke, abgerundete Enden (konsistent zum Logo-Motiv) — z. B. Lucide-Icon-
  Set als Basis, keine gefüllten Glyphen, keine Emoji-artigen Icons.
- Karten/Panels: `rounded-2xl`, dezente Border (`slate-800`), kein starker Schlagschatten —
  flaches, technisches UI statt verspieltem SaaS-Look.
- Datenvisualisierung (Traffic-Graphen) ist das zentrale wiederkehrende visuelle Element auf
  Landingpage, Pitch Deck und Produkt-UI — durchgängig als Linien-/Flächendiagramm im
  Mint-auf-Navy-Stil, nicht als Balkendiagramm.

## 6. Bildsprache

- Reale Produktfotos (Sensor-Gehäuse, Rack, Port-Mirroring-Setup am Switch) statt Stock-Fotos.
- Keine "Hacker im Hoodie vor grünem Matrix-Code"-Klischees.
- Wenn Menschen gezeigt werden: reale Arbeitskontext-Fotos (Serverraum, IT-Büro), keine gestellten
  Stock-"Cyber"-Bilder mit Schloss-Hologrammen.
