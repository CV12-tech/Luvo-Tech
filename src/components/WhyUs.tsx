import ScrollReveal from "@/components/ScrollReveal";
import Counter from "@/components/Counter";

const STATS = [
  {
    value: 3,
    suffix: "",
    label: "Leistungssäulen unter einem Dach — Strategie, KI und Umsetzung",
  },
  {
    value: 1,
    suffix: "",
    label: "Ansprechpartner von der Analyse bis zum laufenden Betrieb",
  },
  {
    value: 0,
    suffix: "",
    label: "Standardlösungen von der Stange",
  },
];

export default function WhyUs() {
  return (
    <section
      id="warum-luvo-tech"
      aria-labelledby="warum-heading"
      className="relative border-t border-border bg-surface px-6 py-28"
    >
      <div className="mx-auto max-w-6xl">
        <div className="grid gap-16 lg:grid-cols-2 lg:items-start">
          <div>
            <ScrollReveal>
              <p className="font-mono-tech text-xs uppercase tracking-[0.25em] text-accent-cyan">
                Warum LuVo Tech
              </p>
            </ScrollReveal>
            <ScrollReveal delay={0.08}>
              <h2
                id="warum-heading"
                className="mt-4 font-display text-3xl font-semibold tracking-tight text-text-primary sm:text-4xl"
              >
                Gewachsene Erfahrung statt theoretisches Beraterwissen
              </h2>
            </ScrollReveal>
            <ScrollReveal delay={0.16}>
              <div className="mt-6 space-y-5 text-lg leading-relaxed text-text-secondary">
                <p>
                  Organisationen unterscheiden sich stark — im kleinen
                  Betrieb entscheidet oft eine Person, in der großen
                  Institution greifen viele Ebenen ineinander. Diese
                  Unterschiede aus eigener Erfahrung zu kennen, verändert die
                  Art, wie man berät.
                </p>
                <p>
                  LuVo Tech bringt gelebtes Verständnis dafür mit, wie
                  Organisationen und Projekte tatsächlich funktionieren —
                  vom kleinen Betrieb bis zur großen Institution — und
                  verbindet es mit strategischer Perspektive. Das Ergebnis:
                  Empfehlungen, die zur Realität passen, nicht nur zur
                  Theorie.
                </p>
              </div>
            </ScrollReveal>
          </div>

          <ScrollReveal delay={0.1} className="grid gap-6 sm:grid-cols-3 lg:gap-4">
            {STATS.map((stat) => (
              <div
                key={stat.label}
                className="rounded-2xl border border-border bg-bg p-6"
              >
                <Counter value={stat.value} suffix={stat.suffix} />
                <p className="mt-3 text-sm leading-relaxed text-text-secondary">
                  {stat.label}
                </p>
              </div>
            ))}
          </ScrollReveal>
        </div>
      </div>
    </section>
  );
}
