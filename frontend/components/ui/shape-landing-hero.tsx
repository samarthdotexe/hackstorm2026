"use client";

import { useEffect, useState } from "react";
import { motion, useReducedMotion, type MotionProps, type Variants } from "framer-motion";
import { ArrowRight, Circle, LockKeyhole, ShieldCheck } from "lucide-react";

import { cn } from "@/lib/utils";

type ElegantShapeProps = {
  className?: string;
  delay?: number;
  width?: number;
  height?: number;
  rotate?: number;
  y?: number;
  gradient?: string;
};

export function getFloatingMotion(
  shouldReduceMotion: boolean,
  y: number,
): Pick<MotionProps, "animate" | "transition"> {
  if (shouldReduceMotion) {
    return { animate: undefined, transition: undefined };
  }

  return {
    animate: { y: [0, y, 0] },
    transition: {
      duration: 12,
      repeat: Number.POSITIVE_INFINITY,
      ease: "easeInOut",
    },
  };
}

function ElegantShape({
  className,
  delay = 0,
  width = 400,
  height = 100,
  rotate = 0,
  y = 15,
  gradient = "from-white/[0.08]",
}: ElegantShapeProps) {
  const shouldReduceMotion = useReducedMotion();
  const floatingMotion = getFloatingMotion(Boolean(shouldReduceMotion), y);

  return (
    <motion.div
      aria-hidden="true"
      initial={
        shouldReduceMotion
          ? false
          : {
              opacity: 0,
              y: -150,
              rotate: rotate - 15,
            }
      }
      animate={{ opacity: 1, y: 0, rotate }}
      transition={
        shouldReduceMotion
          ? { duration: 0 }
          : {
              duration: 2.4,
              delay,
              ease: [0.23, 0.86, 0.39, 0.96],
              opacity: { duration: 1.2 },
            }
      }
      className={cn("absolute", className)}
    >
      <motion.div
        animate={floatingMotion.animate}
        transition={floatingMotion.transition}
        style={{ width, height }}
        className="relative"
      >
        <div
          className={cn(
            "absolute inset-0 rounded-full",
            "bg-gradient-to-r to-transparent",
            gradient,
            "border-2 border-white/[0.15] backdrop-blur-[2px]",
            "shadow-[0_8px_32px_0_rgba(255,255,255,0.1)]",
            "after:absolute after:inset-0 after:rounded-full",
            "after:bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.2),transparent_70%)]",
          )}
        />
      </motion.div>
    </motion.div>
  );
}

export type HeroGeometricProps = {
  badge?: string;
  title1?: string;
  title2?: string;
  description?: string;
  analyzerHref?: string;
  rotate?: number;
  width?: number;
  height?: number;
  y?: number;
};

function HeroGeometric({
  badge = "Local-first scam intelligence",
  title1 = "Stop. Check.",
  title2 = "Stay safe.",
  description = "Analyze messages, screenshots, job offers, and suspicious links before you trust them.",
  analyzerHref = "http://localhost:8501",
  rotate = 12,
  width = 600,
  height = 140,
  y = 15,
}: HeroGeometricProps) {
  const shouldReduceMotion = useReducedMotion();
  const [isLeaving, setIsLeaving] = useState(false);
  const fadeUpVariants: Variants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 30 },
    visible: (index: number) => ({
      opacity: 1,
      y: 0,
      transition: shouldReduceMotion
        ? { duration: 0 }
        : {
            duration: 1,
            delay: 0.35 + index * 0.16,
            ease: [0.25, 0.4, 0.25, 1] as const,
          },
    }),
  };

  useEffect(() => {
    if (!isLeaving) {
      return;
    }

    const navigationTimer = window.setTimeout(() => {
      window.location.assign(analyzerHref);
    }, 460);

    return () => window.clearTimeout(navigationTimer);
  }, [analyzerHref, isLeaving]);

  function beginAnalyzerHandoff(event: React.MouseEvent<HTMLAnchorElement>) {
    if (isLeaving) {
      event.preventDefault();
      return;
    }

    if (shouldReduceMotion) {
      return;
    }

    event.preventDefault();
    setIsLeaving(true);
  }

  return (
    <main className="relative flex min-h-screen w-full items-center justify-center overflow-hidden bg-[#030303] text-white">
      <div
        aria-hidden="true"
        className="absolute inset-0 bg-gradient-to-br from-indigo-500/[0.07] via-transparent to-rose-500/[0.07] blur-3xl"
      />

      <div aria-hidden="true" className="absolute inset-0 overflow-hidden">
        <ElegantShape
          delay={0.3}
          width={width}
          height={height}
          rotate={rotate}
          y={y}
          gradient="from-indigo-500/[0.15]"
          className="left-[-45%] top-[12%] sm:left-[-18%] md:left-[-5%] md:top-[20%]"
        />
        <ElegantShape
          delay={0.5}
          width={500}
          height={120}
          rotate={-15}
          y={y}
          gradient="from-rose-500/[0.15]"
          className="right-[-55%] top-[72%] sm:right-[-22%] md:right-0 md:top-[75%]"
        />
        <ElegantShape
          delay={0.4}
          width={300}
          height={80}
          rotate={-8}
          y={y}
          gradient="from-violet-500/[0.15]"
          className="bottom-[6%] left-[-20%] sm:left-[2%] md:left-[10%] md:bottom-[10%]"
        />
        <ElegantShape
          delay={0.6}
          width={200}
          height={60}
          rotate={20}
          y={y}
          gradient="from-amber-500/[0.15]"
          className="right-[-15%] top-[8%] sm:right-[8%] md:right-[20%] md:top-[15%]"
        />
        <ElegantShape
          delay={0.7}
          width={150}
          height={40}
          rotate={-25}
          y={y}
          gradient="from-cyan-500/[0.15]"
          className="left-[6%] top-[3%] sm:left-[16%] md:left-[25%] md:top-[10%]"
        />
      </div>

      <div className="relative z-10 mx-auto w-full max-w-6xl px-5 py-20 md:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            custom={0}
            variants={fadeUpVariants}
            initial={false}
            animate="visible"
            className="mb-8 inline-flex items-center gap-2 rounded-full border border-white/[0.1] bg-white/[0.04] px-3.5 py-1.5 backdrop-blur-md md:mb-12"
          >
            <Circle className="h-2 w-2 fill-emerald-400 text-emerald-400" aria-hidden="true" />
            <span className="text-sm tracking-wide text-white/65">{badge}</span>
          </motion.div>

          <motion.div custom={1} variants={fadeUpVariants} initial={false} animate="visible">
            <h1
              aria-label={`${title1} ${title2}`}
              className="mb-6 text-5xl font-bold tracking-[-0.045em] sm:text-6xl md:mb-8 md:text-8xl"
            >
              <span className="bg-gradient-to-b from-white to-white/75 bg-clip-text text-transparent">
                {title1}
              </span>
              <br />
              <span className="bg-gradient-to-r from-indigo-300 via-white/90 to-rose-300 bg-clip-text text-transparent">
                {title2}
              </span>
            </h1>
          </motion.div>

          <motion.div custom={2} variants={fadeUpVariants} initial={false} animate="visible">
            <p className="mx-auto mb-9 max-w-2xl px-2 text-base font-light leading-relaxed tracking-wide text-white/50 sm:text-lg md:text-xl">
              {description}
            </p>
          </motion.div>

          <motion.div
            custom={3}
            variants={fadeUpVariants}
            initial={false}
            animate="visible"
            className="flex flex-col items-center justify-center gap-3 sm:flex-row"
          >
            <a
              href={analyzerHref}
              onClick={beginAnalyzerHandoff}
              aria-disabled={isLeaving || undefined}
              className="group inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-full bg-white px-6 py-3 text-sm font-semibold text-black shadow-[0_12px_40px_rgba(255,255,255,0.14)] transition hover:bg-white/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-black sm:w-auto"
            >
              <ShieldCheck className="h-4 w-4" aria-hidden="true" />
              Analyze something
              <ArrowRight
                className="h-4 w-4 transition-transform group-hover:translate-x-0.5"
                aria-hidden="true"
              />
            </a>
            <a
              href="/why-local-matters"
              className="inline-flex min-h-12 w-full items-center justify-center rounded-full border border-white/[0.12] bg-white/[0.04] px-6 py-3 text-sm font-medium text-white/70 backdrop-blur-md transition hover:border-white/25 hover:bg-white/[0.08] hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/80 sm:w-auto"
            >
              Why local matters
            </a>
          </motion.div>

          <motion.div
            id="privacy"
            custom={4}
            variants={fadeUpVariants}
            initial={false}
            animate="visible"
            className="mx-auto mt-10 flex max-w-xl flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs text-white/60 sm:text-sm"
          >
            <span className="inline-flex items-center gap-1.5">
              <LockKeyhole className="h-3.5 w-3.5" aria-hidden="true" />
              Runs locally
            </span>
            <span>Explainable scores</span>
            <span>Built for Indian scam patterns</span>
          </motion.div>
        </div>
      </div>

      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-gradient-to-t from-[#030303] via-transparent to-[#030303]/80"
      />

      {isLeaving ? (
        <div
          role="status"
          aria-live="polite"
          className="handoff-overlay fixed inset-0 z-50 flex items-center justify-center bg-[#030303] px-6 text-center"
        >
          <div className="handoff-card max-w-sm">
            <LockKeyhole className="mx-auto mb-5 h-6 w-6 text-indigo-200" aria-hidden="true" />
            <p className="text-sm font-semibold tracking-[0.18em] text-white/70 uppercase">
              Opening secure workspace
            </p>
            <p className="mt-3 text-sm leading-relaxed text-white/45">
              Your analysis stays under your control.
            </p>
          </div>
        </div>
      ) : null}
    </main>
  );
}

export { HeroGeometric };
export default HeroGeometric;
