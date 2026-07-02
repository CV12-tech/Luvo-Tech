# LuVo Tech — Landingpage

Marken-Landingpage für LuVo Tech: strategische Beratung für Digitalisierung, KI-Implementierung und individuelle Softwareentwicklung. Gebaut mit Next.js (App Router), TypeScript und Tailwind CSS.

## Tech-Stack

- **Next.js 16** (App Router) + **TypeScript**
- **Tailwind CSS v4** (CSS-first Theme in `src/app/globals.css`)
- **react-three-fiber** / **three.js** für den WebGL-Partikelhintergrund im Hero (mit statischem Fallback für `prefers-reduced-motion` und leistungsschwache Geräte)
- **framer-motion** für Scroll-Reveals, Stagger-Animationen und den 3D-Tilt-Effekt der Leistungssäulen-Karten
- **lucide-react** für Icons
- Fonts über `next/font/google`: Space Grotesk (Headlines), Inter (Fließtext), JetBrains Mono (technische Akzente)

## Struktur

```
src/
  app/
    page.tsx          Startseite (setzt alle Sections zusammen)
    layout.tsx         Root-Layout, Fonts, Metadata
    impressum/         Platzhalter-Impressum
    datenschutz/        Platzhalter-Datenschutzerklärung
  components/
    Header.tsx          Sticky Nav mit mobilem Menü
    Hero.tsx             Hero-Section
    HeroBackground3D.tsx WebGL-Partikelnetz + Fallback
    Positioning.tsx       "Wer ist LuVo Tech"
    ServicePillars.tsx    Drei Leistungssäulen (Tilt-Cards)
    TiltCard.tsx           Wiederverwendbare 3D-Tilt-Karte
    WhyUs.tsx               "Warum LuVo Tech" inkl. animierter Zähler
    Counter.tsx              Animierter Zähler (reduced-motion-sicher)
    WorkingMethod.tsx         Arbeitsweise/Prinzipien
    ContactSection.tsx         Kontaktformular (mailto-basiert)
    Footer.tsx                  Footer mit Impressum/Datenschutz-Links
    CursorGlow.tsx                Cursor-Glow-Effekt (Desktop, motion-safe)
    ScrollReveal.tsx               Scroll-in-View-Wrapper
    Wordmark.tsx                    Text-Platzhalter-Wordmark
```

## Entwicklung

```bash
npm install
npm run dev
```

Öffne [http://localhost:3000](http://localhost:3000).

```bash
npm run lint   # ESLint
npm run build  # Production-Build inkl. Type-Check
```

## Hinweise

- Es werden keine Kunden-Cases oder Referenzen gezeigt.
- Der Bezug zur Vollmer GmbH ist bewusst nur im Footer/Impressum sichtbar.
- Die Wordmark in `Wordmark.tsx` ist ein Platzhalter und kann später durch ein echtes Logo-Asset ersetzt werden.
- Impressum/Datenschutz enthalten Platzhaltertexte, die vor Live-Schaltung durch rechtsgeprüfte Inhalte ersetzt werden müssen.
