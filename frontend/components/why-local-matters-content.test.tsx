import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import WhyLocalMattersContent from "@/components/why-local-matters-content";

describe("WhyLocalMattersContent", () => {
  it("explains local processing and clearly marks the optional external lookup", () => {
    render(<WhyLocalMattersContent analyzerHref="http://localhost:8501" />);

    expect(screen.getByRole("heading", { name: /why local matters/i })).toBeInTheDocument();
    expect(screen.getByText(/when the analyzer runs on this device, messages and screenshots are processed locally/i)).toBeInTheDocument();
    expect(screen.getByText(/urlscan is optional\. when enabled, submitted or extracted urls are sent outside your device/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /open the scanner/i })).toHaveAttribute(
      "href",
      "http://localhost:8501",
    );
    expect(screen.getByRole("link", { name: /back to scamshield/i })).toHaveAttribute("href", "/");
  });
});
