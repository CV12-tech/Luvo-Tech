"use client";

import { motion } from "framer-motion";
import { ChevronDown } from "lucide-react";
import HeroBackground3D from "@/components/HeroBackground3D";

export default function Hero() {
  return (
    <section
      id="top"
      className="relative flex min-h-screen items-center overflow-hidden bg-bg pt-24"
      aria-label="Einleitung"
    >
      <HeroBackground3D />
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-bg" />

      <div className="relative mx-auto flex w-full max-w-6xl flex-col px-6 py-24">
        <motion.p
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="font-mono-tech text-xs uppercase tracking-[0.25em] text-accent-cyan"
        >
          Strategische Beratung für Digitalisierung &amp; KI
        </motion.p>

        <motion.h1
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="mt-6 max-w-3xl font-display text-4xl font-semibold leading-tight tracking-tight text-text-primary sm:text-5xl lg:text-6xl"
        >
          Digitalisierung und KI brauchen einen Sparringspartner, der liefert
          — nicht nur präsentiert.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mt-6 max-w-xl text-lg leading-relaxed text-text-secondary"
        >
          LuVo Tech verbindet gewachsene Erfahrung aus Organisationen jeder
          Größe mit strategischem Blick. Wir verstehen Strukturen, bevor wir
          empfehlen — und setzen um, statt nur zu moderieren.
        </motion.p>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.7, delay: 0.5 }}
          className="mt-20"
        >
          <a
            href="#positionierung"
            className="group inline-flex flex-col items-start gap-3 text-sm text-text-secondary transition-colors hover:text-accent-cyan"
          >
            <span>Mehr erfahren</span>
            <span className="flex h-9 w-9 items-center justify-center rounded-full border border-white/10 text-accent-cyan transition-all group-hover:border-accent-cyan/60 motion-safe:animate-bounce">
              <ChevronDown className="h-4 w-4" aria-hidden="true" />
            </span>
          </a>
        </motion.div>
      </div>
    </section>
  );
}
