import { HeroGeometric, type HeroGeometricProps } from "@/components/ui/shape-landing-hero";

const settings = {
  rotate: 12,
  width: 600,
  height: 140,
  y: 15,
};

export default function Demo(props: Partial<HeroGeometricProps>) {
  const configuredProps = { ...settings, ...props };

  return (
    <div className="min-h-screen w-full">
      <HeroGeometric {...configuredProps} />
    </div>
  );
}
