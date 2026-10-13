import type { Metadata } from "next";

import WhyLocalMattersContent from "@/components/why-local-matters-content";

export const metadata: Metadata = {
  title: "Why Local Matters — ScamShield OSS",
  description: "How ScamShield keeps analysis local, explainable, and opt-in by design.",
};

export default function WhyLocalMattersPage() {
  const analyzerUrl = process.env.NEXT_PUBLIC_SCAMSHIELD_APP_URL || "http://localhost:8501";

  return <WhyLocalMattersContent analyzerHref={analyzerUrl} />;
}
