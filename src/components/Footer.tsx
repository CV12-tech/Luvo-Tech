import Link from "next/link";
import Wordmark from "@/components/Wordmark";

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-white/5 bg-surface/30 px-6 py-12">
      <div className="mx-auto flex max-w-6xl flex-col gap-8 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <Wordmark />
          <p className="mt-3 max-w-sm text-sm leading-relaxed text-text-secondary">
            Strategische Beratung für Digitalisierung, KI und
            Softwareentwicklung.
          </p>
        </div>

        <div className="flex flex-col gap-2 text-sm text-text-secondary sm:items-end">
          <nav aria-label="Rechtliches" className="flex gap-6">
            <Link
              href="/impressum"
              className="transition-colors hover:text-accent-cyan"
            >
              Impressum
            </Link>
            <Link
              href="/datenschutz"
              className="transition-colors hover:text-accent-cyan"
            >
              Datenschutz
            </Link>
          </nav>
          <p className="text-xs text-text-secondary/70">
            LuVo Tech ist eine Marke der Vollmer GmbH.
          </p>
          <p className="text-xs text-text-secondary/70">
            © {year} Vollmer GmbH. Alle Rechte vorbehalten.
          </p>
        </div>
      </div>
    </footer>
  );
}
