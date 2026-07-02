import type { Metadata } from "next";
import Link from "next/link";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Impressum — LuVo Tech",
};

export default function ImpressumPage() {
  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-3xl flex-1 px-6 pb-24 pt-40">
        <h1 className="font-display text-3xl font-semibold tracking-tight text-text-primary">
          Impressum
        </h1>

        <div className="mt-8 space-y-6 text-text-secondary">
          <p>
            Angaben gemäß § 5 TMG — Platzhalterinhalt, wird vor Veröffentlichung
            durch die finalen Angaben ersetzt.
          </p>

          <div>
            <p className="font-medium text-text-primary">Vollmer GmbH</p>
            <p>LuVo Tech ist eine Marke der Vollmer GmbH</p>
            <p>Musterstraße 1</p>
            <p>12345 Musterstadt</p>
          </div>

          <div>
            <p className="font-medium text-text-primary">Kontakt</p>
            <p>E-Mail: kontakt@luvo-tech.de</p>
          </div>

          <div>
            <p className="font-medium text-text-primary">Vertretungsberechtigt</p>
            <p>Geschäftsführung Vollmer GmbH (Platzhalter)</p>
          </div>

          <div>
            <p className="font-medium text-text-primary">Handelsregister</p>
            <p>Registergericht: Platzhalter · Registernummer: Platzhalter</p>
          </div>

          <p className="text-sm">
            Zurück zur{" "}
            <Link href="/" className="text-accent-cyan hover:underline">
              Startseite
            </Link>
            .
          </p>
        </div>
      </main>
      <Footer />
    </>
  );
}
