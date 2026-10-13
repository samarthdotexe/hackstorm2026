# ScamShield React Hero Revamp Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a shadcn-compatible React/TypeScript/Tailwind landing page using the supplied geometric hero and route users into the existing analyzer.

**Architecture:** Create an isolated Next.js package under `frontend/`, keeping the Python analysis stack unchanged. The reusable hero lives in `components/ui`, and the page passes a configurable Streamlit analyzer URL.

**Tech Stack:** Next.js, React, TypeScript, Tailwind CSS v4, shadcn conventions, Framer Motion, Lucide React, Vitest, Testing Library

**Spec:** `docs/superpowers/specs/2026-10-13-react-hero-revamp-design.md`

## Global Constraints

- Preserve `streamlit run app.py` and all existing detector behavior.
- Place reusable UI at `frontend/components/ui` and global CSS at `frontend/app/globals.css`.
- Use TypeScript, Tailwind CSS, and the `@/*` root alias.
- Install and use `lucide-react` and `framer-motion`.
- Respect reduced-motion preferences and responsive layouts.

## Review Focus

- Missing `NEXT_PUBLIC_SCAMSHIELD_APP_URL` must fall back to `http://localhost:8501`.
- Mobile widths must not overflow because of decorative shapes.
- Reduced-motion users must not receive infinite shape animations.
- The page must remain meaningful if JavaScript animation is unavailable.
- The frontend build must not alter the Python runtime or analysis modules.

### Task 1: Frontend foundation and component contract

**Files:** Create `frontend/package.json`, configuration files, `frontend/components.json`, `frontend/lib/utils.ts`, and `frontend/components/ui/shape-landing-hero.test.tsx`.

- [ ] Write a failing component test asserting the ScamShield heading, descriptive copy, and analyzer CTA destination.
- [ ] Run `npm test -- --run`; expect failure because the hero component does not exist.
- [ ] Install the runtime and test dependencies and add the typed `cn` helper.

### Task 2: Geometric hero and page integration

**Files:** Create `frontend/components/ui/shape-landing-hero.tsx`, `frontend/components/demo.tsx`, `frontend/app/page.tsx`, `frontend/app/layout.tsx`, and `frontend/app/globals.css`.

- [ ] Implement the supplied geometric composition with product copy, CTA, Lucide icons, and reduced-motion behavior.
- [ ] Re-run the component tests; expect all tests to pass.
- [ ] Run TypeScript and ESLint checks.

### Task 3: Documentation and runtime verification

**Files:** Create `frontend/README.md`; modify root `README.md` and `.gitignore`.

- [ ] Document default paths, shadcn CLI setup, dependency installation, and the two-process local workflow.
- [ ] Run the frontend production build and existing Python tests.
- [ ] Start the Next.js dev server and verify the rendered landing page in a browser at desktop and mobile widths.
