"use client";

import { motion, type Variants } from "framer-motion";
import { Compass, BrainCircuit, Code2 } from "lucide-react";
import TiltCard from "@/components/TiltCard";

const PILLARS = [
  {
    icon: Compass,
    title: "Digitalisierungsberatung",
    description:
      "Wir analysieren Prozesse und Strukturen, bevor wir Empfehlungen aussprechen. Daraus entsteht eine Roadmap, die zu Ihrer Organisation passt — nicht zu einer Vorlage.",
  },
  {
    icon: BrainCircuit,
    title: "KI-Implementierung",
    description:
      "Von der Potenzialanalyse bis zur produktiven Lösung: Wir zeigen, wo KI tatsächlich etwas verändert, und begleiten die Umsetzung bis der Betrieb läuft.",
  },
  {
    icon: Code2,
    title: "Softwareentwicklung",
    description:
      "Individuelle Lösungen für individuelle Anforderungen — kein Standard von der Stange, sondern Software, die zu Ihren Abläufen passt.",
  },
];

const containerVariants: Variants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.12 },
  },
};

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 28 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] },
  },
};

export default function ServicePillars() {
  return (
    <section
      id="leistungen"
      aria-labelledby="leistungen-heading"
      className="relative border-t border-border bg-bg px-6 py-28"
    >
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto max-w-2xl text-center">
          <p className="font-mono-tech text-xs uppercase tracking-[0.25em] text-accent-cyan">
            Leistungssäulen
          </p>
          <h2
            id="leistungen-heading"
            className="mt-4 font-display text-3xl font-semibold tracking-tight text-text-primary sm:text-4xl"
          >
            Drei gleichrangige Perspektiven auf dieselbe Aufgabe
          </h2>
          <p className="mt-4 text-lg leading-relaxed text-text-secondary">
            Strategie, KI und Umsetzung greifen ineinander. Je nach
            Ausgangslage setzen wir bei einer Säule an — immer mit Blick auf
            die anderen beiden.
          </p>
        </div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
          variants={containerVariants}
          className="mt-16 grid gap-6 md:grid-cols-3"
        >
          {PILLARS.map((pillar) => (
            <motion.div key={pillar.title} variants={cardVariants}>
              <TiltCard className="h-full">
                <pillar.icon
                  aria-hidden="true"
                  className="h-8 w-8 text-accent-cyan"
                  strokeWidth={1.5}
                />
                <h3 className="mt-6 font-display text-xl font-semibold text-text-primary">
                  {pillar.title}
                </h3>
                <p className="mt-3 text-base leading-relaxed text-text-secondary">
                  {pillar.description}
                </p>
              </TiltCard>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
