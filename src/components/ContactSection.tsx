"use client";

import { useState, type FormEvent } from "react";
import { Mail } from "lucide-react";
import ScrollReveal from "@/components/ScrollReveal";

const CONTACT_EMAIL = "kontakt@luvo-tech.de";

export default function ContactSection() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const subject = encodeURIComponent(`Kontaktanfrage von ${name || "Website"}`);
    const body = encodeURIComponent(
      `${message}\n\n---\nName: ${name}\nE-Mail: ${email}`
    );
    window.location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;
    setSubmitted(true);
  };

  return (
    <section
      id="kontakt"
      aria-labelledby="kontakt-heading"
      className="relative border-t border-border bg-bg px-6 py-28"
    >
      <div className="mx-auto max-w-6xl">
        <div className="grid gap-16 lg:grid-cols-2">
          <ScrollReveal>
            <p className="font-mono-tech text-xs uppercase tracking-[0.25em] text-accent-cyan">
              Kontakt
            </p>
            <h2
              id="kontakt-heading"
              className="mt-4 font-display text-3xl font-semibold tracking-tight text-text-primary sm:text-4xl"
            >
              Ein erstes Gespräch, ganz unverbindlich
            </h2>
            <p className="mt-6 max-w-md text-lg leading-relaxed text-text-secondary">
              Sie überlegen, wo Digitalisierung oder KI in Ihrer Organisation
              ansetzen könnte? Schreiben Sie uns kurz, worum es geht — wir
              melden uns mit einer ehrlichen Einschätzung zurück.
            </p>
            <a
              href={`mailto:${CONTACT_EMAIL}`}
              className="mt-8 inline-flex items-center gap-3 text-text-primary transition-colors hover:text-accent-cyan"
            >
              <Mail className="h-5 w-5 text-accent-cyan" aria-hidden="true" />
              <span className="font-mono-tech text-sm">{CONTACT_EMAIL}</span>
            </a>
          </ScrollReveal>

          <ScrollReveal delay={0.1}>
            <form
              onSubmit={handleSubmit}
              className="rounded-2xl border border-border bg-surface p-8 border-glow"
            >
              <div className="grid gap-5">
                <div>
                  <label
                    htmlFor="name"
                    className="text-sm text-text-secondary"
                  >
                    Name
                  </label>
                  <input
                    id="name"
                    name="name"
                    type="text"
                    required
                    value={name}
                    onChange={(event) => setName(event.target.value)}
                    className="mt-2 w-full rounded-lg border border-border bg-bg px-4 py-3 text-text-primary outline-none transition-colors focus:border-accent-cyan/60"
                  />
                </div>
                <div>
                  <label
                    htmlFor="email"
                    className="text-sm text-text-secondary"
                  >
                    E-Mail
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    className="mt-2 w-full rounded-lg border border-border bg-bg px-4 py-3 text-text-primary outline-none transition-colors focus:border-accent-cyan/60"
                  />
                </div>
                <div>
                  <label
                    htmlFor="message"
                    className="text-sm text-text-secondary"
                  >
                    Nachricht
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows={4}
                    required
                    value={message}
                    onChange={(event) => setMessage(event.target.value)}
                    className="mt-2 w-full resize-none rounded-lg border border-border bg-bg px-4 py-3 text-text-primary outline-none transition-colors focus:border-accent-cyan/60"
                  />
                </div>
                <button
                  type="submit"
                  className="mt-2 inline-flex items-center justify-center rounded-full border border-accent-cyan/40 px-6 py-3 font-body text-sm text-text-primary transition-colors hover:border-accent-cyan hover:text-accent-cyan"
                >
                  Nachricht senden
                </button>
                <p role="status" className="min-h-5 text-sm text-success">
                  {submitted &&
                    "Ihr E-Mail-Programm öffnet sich mit der vorbereiteten Nachricht."}
                </p>
              </div>
            </form>
          </ScrollReveal>
        </div>
      </div>
    </section>
  );
}
