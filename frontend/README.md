# ScamShield React frontend

This package is the visual landing page for ScamShield OSS. It uses Next.js App Router, React, TypeScript, Tailwind CSS v4, shadcn-compatible conventions, Framer Motion, and Lucide React. The security-sensitive detection logic remains in the Python application.

## Run locally

Use Node.js `22.22.2`, `24.15.0` or newer in the Node 24 line, or Node.js `26+`. These ranges match the frontend test toolchain declared in `package.json`.

Start the analyzer from the repository root:

```bash
source .venv/bin/activate
streamlit run app.py
```

In a second terminal, start the landing page:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The “Analyze something” button opens `http://localhost:8501` by default.

To use another analyzer address, create `frontend/.env.local`:

```dotenv
NEXT_PUBLIC_SCAMSHIELD_APP_URL=http://localhost:8501
```

## Default shadcn paths

- UI components: `components/ui`
- General components: `components`
- Utility helpers: `lib`
- Global Tailwind styles: `app/globals.css`
- CLI configuration: `components.json`

The `@/*` alias maps to the `frontend/` package root, so the hero is imported as `@/components/ui/shape-landing-hero`. Keeping reusable primitives in `components/ui` matters because the shadcn CLI uses the `aliases.ui` entry in `components.json` to place generated files and rewrite imports consistently. A different or missing folder causes copied components and CLI-generated components to diverge.

## Setting up the same structure from scratch

The repository is already configured. For a new project, the official shadcn/Next workflow is:

```bash
npx shadcn@latest init -t next
```

Choose the recommended Next.js defaults: TypeScript, Tailwind CSS, App Router, no `src/` directory, and the `@/*` alias. For an existing compatible Next.js project, run:

```bash
npx shadcn@latest init
npm install lucide-react framer-motion
```

If the project uses a `src/` directory, `components/ui` will normally live at `src/components/ui`, and `@/*` should map to `./src/*`. This package intentionally uses no `src/` directory so the requested `/components/ui` structure remains at the frontend root.

## Component integration

The reusable component is `components/ui/shape-landing-hero.tsx`. `components/demo.tsx` supplies the requested geometric defaults, and `app/page.tsx` provides the analyzer URL.

`HeroGeometric` accepts:

- `badge`, `title1`, `title2`, and `description` for product copy;
- `analyzerHref` for the primary CTA;
- `rotate`, `width`, `height`, and `y` for the main decorative shape.

The `/why-local-matters` route explains the local-first design, explainable scores, private screenshot OCR, and the opt-in nature of URLScan. The landing-page “Why local matters” link opens this page, and its scanner CTA points to the same configurable analyzer URL.

It requires no context provider, global state, image asset, or external font. Its only hook is Framer Motion’s `useReducedMotion`, which disables the entrance and infinite floating motion when the operating system requests reduced motion. Decorative layers are hidden from assistive technology.

Responsive behavior is built into the Tailwind classes: buttons stack on narrow screens, text scales through mobile/tablet/desktop breakpoints, and oversized shapes remain clipped by the full-screen container.

## Verification

```bash
npm test -- --run
npm run typecheck
npm run lint
npm run build
```

If a restricted environment prevents Turbopack from opening its internal worker port, verify with Next’s supported Webpack builder:

```bash
npm run build -- --webpack
```
