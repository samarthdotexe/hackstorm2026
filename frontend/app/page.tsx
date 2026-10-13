import Demo from "@/components/demo";

export default function Home() {
  const analyzerUrl = process.env.NEXT_PUBLIC_SCAMSHIELD_APP_URL || "http://localhost:8501";

  return <Demo analyzerHref={analyzerUrl} />;
}
