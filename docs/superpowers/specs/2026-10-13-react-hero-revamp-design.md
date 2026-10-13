# ScamShield React Hero Revamp Design

## Goal

Add a polished React landing experience based on the supplied geometric hero while preserving the complete local Streamlit analyzer. The landing page should explain ScamShield immediately and route users into the running analyzer.

## Architecture

The repository gains an isolated `frontend/` Next.js App Router package with TypeScript, Tailwind CSS v4, and shadcn-compatible aliases. Reusable UI lives at `frontend/components/ui`; global styles live at `frontend/app/globals.css`; `frontend/lib/utils.ts` provides shadcn's `cn` helper.

The React frontend does not duplicate detection logic. Its primary CTA points to `NEXT_PUBLIC_SCAMSHIELD_APP_URL`, defaulting to `http://localhost:8501`, where the existing Streamlit application continues to run. This keeps the security-sensitive Python/Ollama/OCR pipeline single-sourced.

## Visual Design

The supplied dark geometric hero becomes ScamShield's landing surface. Five slow translucent shapes frame the content without obscuring it. Product-specific copy, shield iconography, trust signals, and a strong CTA replace the generic design-agency content. The layout remains full-screen and responsive from mobile through desktop.

Motion honors the operating system's reduced-motion preference. Decorative shapes become static when reduced motion is enabled, and all nonessential decorative layers are hidden from assistive technology.

## Dependencies and Conventions

- Next.js App Router, React, TypeScript, Tailwind CSS v4.
- `framer-motion` and `lucide-react` as explicitly requested.
- `clsx` and `tailwind-merge` for the shadcn-compatible `cn` helper.
- Vitest, Testing Library, and jsdom for component behavior tests.
- shadcn CLI configuration in `frontend/components.json`, with `@/components/ui` mapping to `frontend/components/ui`.

No image asset is required by the component. Adding an unrelated stock photo would compete with its geometric visual language.

## Verification

Component tests verify product copy and analyzer-link behavior. TypeScript type checking, ESLint, production build, and a browser smoke test verify integration and responsive rendering. Existing Python tests must remain green.
