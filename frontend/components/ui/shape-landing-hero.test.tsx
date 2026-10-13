import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { getFloatingMotion, HeroGeometric } from "@/components/ui/shape-landing-hero";

describe("HeroGeometric", () => {
  it("introduces ScamShield and links to the local analyzer", () => {
    render(<HeroGeometric analyzerHref="http://localhost:8501" />);

    expect(
      screen.getByRole("heading", { name: /stop\. check\. stay safe\./i }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/messages, screenshots, job offers, and suspicious links/i),
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /analyze something/i })).toHaveAttribute(
      "href",
      "http://localhost:8501",
    );
  });

  it("honors the operating system reduced-motion preference", () => {
    const reduced = getFloatingMotion(true, 15);
    const animated = getFloatingMotion(false, 15);

    expect(reduced.animate).toBeUndefined();
    expect(reduced.transition).toBeUndefined();
    expect(animated.animate).toEqual({ y: [0, 15, 0] });
    expect(animated.transition).toMatchObject({
      duration: 12,
      repeat: Number.POSITIVE_INFINITY,
    });
  });

  it("shows a secure-workspace handoff before opening the analyzer", () => {
    render(<HeroGeometric analyzerHref="http://localhost:8501" />);

    const analyzerLink = screen.getByRole("link", { name: /analyze something/i });
    fireEvent.click(analyzerLink);

    expect(screen.getByRole("status")).toHaveTextContent(/opening secure workspace/i);
    expect(fireEvent.click(analyzerLink)).toBe(false);
  });
});
