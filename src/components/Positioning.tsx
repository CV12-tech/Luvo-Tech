import ScrollReveal from "@/components/ScrollReveal";

export default function Positioning() {
  return (
    <section
      id="positionierung"
      aria-labelledby="positionierung-heading"
      className="relative border-t border-white/5 bg-bg px-6 py-28"
    >
      <div className="mx-auto max-w-4xl">
        <ScrollReveal>
          <p className="font-mono-tech text-xs uppercase tracking-[0.25em] text-accent-cyan">
            Positionierung
          </p>
        </ScrollReveal>

        <ScrollReveal delay={0.08}>
          <h2
            id="positionierung-heading"
            className="mt-4 font-display text-3xl font-semibold tracking-tight text-text-primary sm:text-4xl"
          >
            Kein austauschbarer Umsetzer. Ein Sparringspartner, der einordnet
            und liefert.
          </h2>
        </ScrollReveal>

        <ScrollReveal delay={0.16}>
          <div className="mt-8 space-y-6 text-lg leading-relaxed text-text-secondary">
            <p>
              LuVo Tech begleitet Organisationen bei Digitalisierung und
              KI-Einsatz — nicht als externer Dienstleister, der eine Liste
              abarbeitet, sondern als Sparringspartner, der versteht, wie
              Ihre Organisation tatsächlich funktioniert, bevor er
              Empfehlungen ausspricht.
            </p>
            <p>
              KI-Projekte scheitern selten an der Technik — meistens an der
              Frage, wo sie wirklich etwas verändern. Genau da setzen wir an:
              mit strategischem Blick auf Prozesse, Strukturen und
              realistische Umsetzbarkeit. Und wir bleiben nicht bei der
              Empfehlung stehen, sondern liefern die technische Lösung
              gleich mit.
            </p>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
