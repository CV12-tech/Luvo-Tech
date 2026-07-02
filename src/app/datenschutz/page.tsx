import type { Metadata } from "next";
import Link from "next/link";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Datenschutz — LuVo Tech",
};

export default function DatenschutzPage() {
  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-3xl flex-1 px-6 pb-24 pt-40">
        <h1 className="font-display text-3xl font-semibold tracking-tight text-text-primary">
          Datenschutzerklärung
        </h1>

        <div className="mt-8 space-y-6 text-text-secondary">
          <p>
            Platzhalterinhalt — wird vor Veröffentlichung durch eine
            vollständige, rechtsgeprüfte Datenschutzerklärung ersetzt.
          </p>

          <div>
            <h2 className="font-display text-lg font-semibold text-text-primary">
              Verantwortlicher
            </h2>
            <p className="mt-2">
              Vollmer GmbH, Musterstraße 1, 12345 Musterstadt, E-Mail:
              kontakt@luvo-tech.de
            </p>
          </div>

          <div>
            <h2 className="font-display text-lg font-semibold text-text-primary">
              Kontaktformular
            </h2>
            <p className="mt-2">
              Nachrichten über das Kontaktformular werden über Ihr
              E-Mail-Programm versendet. Es findet keine serverseitige
              Speicherung der Formulardaten durch diese Website statt.
            </p>
          </div>

          <div>
            <h2 className="font-display text-lg font-semibold text-text-primary">
              Ihre Rechte
            </h2>
            <p className="mt-2">
              Sie haben das Recht auf Auskunft, Berichtigung, Löschung und
              Einschränkung der Verarbeitung Ihrer personenbezogenen Daten.
            </p>
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
