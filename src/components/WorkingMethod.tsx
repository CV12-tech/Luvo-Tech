"use client";

import { motion, type Variants } from "framer-motion";
import { Search, ListTree, Wrench, ShieldCheck } from "lucide-react";

const STEPS = [
  {
    icon: Search,
    number: "01",
    title: "Verstehen",
    description:
      "Wir schauen uns Prozesse, Strukturen und Entscheidungswege genau an, bevor wir über Lösungen sprechen.",
  },
  {
    icon: ListTree,
    number: "02",
    title: "Einordnen",
    description:
      "Aus dem Verständnis entsteht eine klare Priorisierung: Wo lohnt sich Digitalisierung oder KI wirklich — und wo nicht.",
  },
  {
    icon: Wrench,
    number: "03",
    title: "Umsetzen",
    description:
      "Wir bleiben nicht bei der Empfehlung stehen, sondern entwickeln und implementieren die Lösung selbst mit.",
  },
  {
    icon: ShieldCheck,
    number: "04",
    title: "Verantworten",
    description:
      "Ergebnisse werden nachvollziehbar dokumentiert und so übergeben, dass Ihre Organisation eigenständig weiterarbeiten kann.",
  },
];

const containerVariants: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.55, ease: [0.16, 1, 0.3, 1] },
  },
};

export default function WorkingMethod() {
  return (
    <section
      id="arbeitsweise"
      aria-labelledby="arbeitsweise-heading"
      className="relative border-t border-white/5 bg-bg px-6 py-28"
    >
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto max-w-2xl text-center">
          <p className="font-mono-tech text-xs uppercase tracking-[0.25em] text-accent-cyan">
            Arbeitsweise
          </p>
          <h2
            id="arbeitsweise-heading"
            className="mt-4 font-display text-3xl font-semibold tracking-tight text-text-primary sm:text-4xl"
          >
            Vier Prinzipien, ein durchgängiger Ansatz
          </h2>
        </div>

        <motion.ol
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
          variants={containerVariants}
          className="mt-16 grid gap-px overflow-hidden rounded-2xl border border-white/10 bg-white/5 sm:grid-cols-2 lg:grid-cols-4"
        >
          {STEPS.map((step) => (
            <motion.li
              key={step.number}
              variants={itemVariants}
              className="relative bg-bg p-8"
            >
              <span className="font-mono-tech text-xs text-text-secondary">
                {step.number}
              </span>
              <step.icon
                aria-hidden="true"
                strokeWidth={1.5}
                className="mt-4 h-7 w-7 text-accent-cyan"
              />
              <h3 className="mt-4 font-display text-lg font-semibold text-text-primary">
                {step.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-text-secondary">
                {step.description}
              </p>
            </motion.li>
          ))}
        </motion.ol>
      </div>
    </section>
  );
}
