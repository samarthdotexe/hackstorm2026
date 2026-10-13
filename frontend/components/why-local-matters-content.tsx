"use client";

import { motion, useReducedMotion } from "framer-motion";
import Link from "next/link";
import {
  ArrowLeft,
  ArrowRight,
  Eye,
  FileImage,
  Globe2,
  LockKeyhole,
  Server,
  ShieldCheck,
} from "lucide-react";

type WhyLocalMattersContentProps = {
  analyzerHref: string;
};

const principles = [
  {
    icon: Server,
    title: "Messages stay local",
    description:
      "When the analyzer runs on this device, messages and screenshots are processed locally by Ollama and OCR. A remote analyzer changes that boundary.",
  },
  {
    icon: Eye,
    title: "Every score is explainable",
    description:
      "See the tactics, URL signals, and community patterns behind a risk score instead of receiving a black-box verdict.",
  },
  {
    icon: FileImage,
    title: "Screenshots work privately",
    description:
      "Upload a screenshot for local OCR when text is hard to copy. The extracted content stays in the local workflow.",
  },
  {
    icon: Globe2,
    title: "External lookups are opt-in",
    description:
      "URLScan is optional. When enabled, submitted or extracted URLs are sent outside your device for reputation lookup.",
  },
];

export default function WhyLocalMattersContent({ analyzerHref }: WhyLocalMattersContentProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#030303] text-white">
      <div aria-hidden="true" className="absolute inset-0 bg-gradient-to-br from-indigo-500/[0.08] via-transparent to-rose-500/[0.08] blur-3xl" />
      <div aria-hidden="true" className="absolute inset-0 overflow-hidden">
        <div className="absolute left-[-18%] top-[12%] h-36 w-[620px] rotate-12 rounded-full border-2 border-white/[0.14] bg-gradient-to-r from-indigo-500/[0.15] to-transparent shadow-[0_8px_32px_rgba(255,255,255,0.08)]" />
        <div className="absolute right-[-14%] top-[68%] h-32 w-[520px] -rotate-12 rounded-full border-2 border-white/[0.14] bg-gradient-to-r from-rose-500/[0.15] to-transparent shadow-[0_8px_32px_rgba(255,255,255,0.08)]" />
      </div>

      <div className="relative z-10 mx-auto w-full max-w-6xl px-5 py-8 md:px-8 md:py-12">
        <nav aria-label="Page navigation" className="flex items-center justify-between">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm font-medium text-white/60 transition hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/80"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            Back to ScamShield
          </Link>
          <span className="inline-flex items-center gap-2 text-xs tracking-[0.16em] text-white/45 uppercase">
            <LockKeyhole className="h-3.5 w-3.5" aria-hidden="true" />
            Privacy by default
          </span>
        </nav>

        <motion.section
          initial={false}
          animate={{ opacity: 1, y: 0 }}
          transition={shouldReduceMotion ? { duration: 0 } : { duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          className="mx-auto max-w-4xl py-24 text-center md:py-32"
        >
          <span className="mb-7 inline-flex items-center gap-2 rounded-full border border-white/[0.1] bg-white/[0.04] px-3.5 py-1.5 text-sm tracking-wide text-white/65 backdrop-blur-md">
            <ShieldCheck className="h-4 w-4 text-emerald-300" aria-hidden="true" />
            Understand before you act
          </span>
          <h1 aria-label="Why local matters" className="text-5xl font-bold tracking-[-0.05em] sm:text-6xl md:text-8xl">
            Why local
            <br />
            <span className="bg-gradient-to-r from-indigo-300 via-white/90 to-rose-300 bg-clip-text text-transparent">
              matters.
            </span>
          </h1>
          <p className="mx-auto mt-7 max-w-2xl text-base leading-relaxed tracking-wide text-white/55 sm:text-lg">
            ScamShield is designed to help you slow down, see the evidence, and keep sensitive content under your control.
          </p>
        </motion.section>

        <section aria-labelledby="principles-heading" className="mx-auto max-w-5xl pb-20">
          <h2 id="principles-heading" className="sr-only">
            ScamShield privacy principles
          </h2>
          <div className="grid gap-4 md:grid-cols-2">
            {principles.map(({ icon: Icon, title, description }) => (
              <article
                key={title}
                className="rounded-3xl border border-white/[0.1] bg-white/[0.035] p-6 backdrop-blur-md md:p-8"
              >
                <Icon className="mb-7 h-5 w-5 text-indigo-200" aria-hidden="true" />
                <h3 className="text-xl font-semibold tracking-tight text-white">{title}</h3>
                <p className="mt-3 text-sm leading-relaxed text-white/55 md:text-base">{description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="mx-auto flex max-w-4xl flex-col items-center justify-between gap-6 rounded-3xl border border-white/[0.1] bg-white/[0.04] p-6 backdrop-blur-md md:flex-row md:p-8">
          <div>
            <p className="text-sm font-semibold tracking-[0.14em] text-white/55 uppercase">Ready to check something?</p>
            <p className="mt-2 text-lg text-white">Bring the evidence. Keep the control.</p>
          </div>
          <a
            href={analyzerHref}
            className="group inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-full bg-white px-6 py-3 text-sm font-semibold text-black shadow-[0_12px_40px_rgba(255,255,255,0.14)] transition hover:bg-white/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-black md:w-auto"
          >
            Open the scanner
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
          </a>
        </section>

        <p className="mx-auto max-w-3xl py-10 text-center text-xs leading-relaxed text-white/60 sm:text-sm">
          ScamShield provides risk guidance, not certainty or legal advice. Always verify important requests through an organization&apos;s official channels.
        </p>
      </div>

      <div aria-hidden="true" className="pointer-events-none absolute inset-0 bg-gradient-to-t from-[#030303] via-transparent to-[#030303]/70" />
    </main>
  );
}
