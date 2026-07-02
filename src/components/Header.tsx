"use client";

import { useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion } from "framer-motion";
import { Menu, X } from "lucide-react";
import Wordmark from "@/components/Wordmark";

const NAV_LINKS = [
  { href: "#positionierung", label: "Positionierung" },
  { href: "#leistungen", label: "Leistungen" },
  { href: "#warum-luvo-tech", label: "Warum LuVo Tech" },
  { href: "#arbeitsweise", label: "Arbeitsweise" },
  { href: "#kontakt", label: "Kontakt" },
];

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="fixed inset-x-0 top-0 z-40 border-b border-border bg-bg/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link
          href="#top"
          aria-label="LuVo Tech Startseite"
          onClick={() => setIsMenuOpen(false)}
        >
          <Wordmark />
        </Link>
        <nav aria-label="Hauptnavigation" className="hidden md:block">
          <ul className="flex items-center gap-8 font-body text-sm text-text-secondary">
            {NAV_LINKS.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  className="transition-colors hover:text-accent-cyan"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <a
          href="#kontakt"
          className="hidden rounded-full border border-accent-cyan/30 px-4 py-2 font-body text-sm text-text-primary transition-colors hover:border-accent-cyan/70 hover:text-accent-cyan md:inline-block"
        >
          Kontakt
        </a>
        <button
          type="button"
          onClick={() => setIsMenuOpen((open) => !open)}
          aria-expanded={isMenuOpen}
          aria-controls="mobile-menu"
          aria-label={isMenuOpen ? "Menü schließen" : "Menü öffnen"}
          className="flex h-10 w-10 items-center justify-center rounded-full border border-border text-text-primary transition-colors hover:border-accent-cyan/50 hover:text-accent-cyan md:hidden"
        >
          {isMenuOpen ? (
            <X className="h-5 w-5" aria-hidden="true" />
          ) : (
            <Menu className="h-5 w-5" aria-hidden="true" />
          )}
        </button>
      </div>

      <AnimatePresence>
        {isMenuOpen && (
          <motion.nav
            id="mobile-menu"
            aria-label="Mobile Hauptnavigation"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className="overflow-hidden border-t border-border md:hidden"
          >
            <ul className="flex flex-col gap-1 px-6 py-4">
              {NAV_LINKS.map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    onClick={() => setIsMenuOpen(false)}
                    className="block py-3 text-base text-text-secondary transition-colors hover:text-accent-cyan"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}
