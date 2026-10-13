# ScamShield OSS Implementation Plan

**Spec:** `docs/superpowers/specs/2026-10-13-scamshield-oss-design.md`

## Global constraints

Use Python 3.11+, pathlib-relative resources, public typed APIs, defensive optional integrations, no secret-bearing URLScan configuration, exact verdicts (`safe`, `suspicious`, `scam`), and scores clamped to 0–100. Keep the UI safe from untrusted HTML.

## Task 1: Detection core and community patterns

**Files:** `tests/test_detector.py`, `detector.py`, `patterns.json`

1. Write failing tests for clamping, verdict thresholds, malformed/missing pattern fallback, Indian/community pattern matching, malformed Ollama output, and deterministic fallback.
2. Run `python -m unittest tests.test_detector -v`; confirm failures are missing-module/behavior failures.
3. Implement `RiskResult`, `PatternDatabase`, `OllamaAnalyzer`, response parsing, and `ScamDetector.analyze`.
4. Re-run the focused tests and confirm they pass.

## Task 2: URL analysis

**Files:** `tests/test_url_checker.py`, `url_checker.py`

1. Write failing tests for normalization, invalid schemes, risky URL signals, safe public-search parsing, and network failure.
2. Run `python -m unittest tests.test_url_checker -v`; confirm the expected failures.
3. Implement typed URL result models, deterministic heuristics, URL extraction, and opt-in URLScan lookup using the standard library.
4. Re-run focused tests and the full suite.

## Task 3: OCR boundary

**Files:** `tests/test_ocr.py`, `ocr.py`

1. Write failing tests for missing image data and graceful dependency/executable failures.
2. Run `python -m unittest tests.test_ocr -v`; confirm expected failures.
3. Implement optional Pillow preprocessing and Tesseract extraction with typed results.
4. Re-run focused tests and the full suite.

## Task 4: Streamlit experience and open-source release files

**Files:** `app.py`, `requirements.txt`, `README.md`, `LICENSE`, `.github/CONTRIBUTING.md`

1. Implement the dark, safe Streamlit workflow for text, screenshots, and URLs, including privacy labels, service warnings, model selection, and explainable results.
2. Add pinned-minimum runtime dependencies, installation/demo documentation, troubleshooting, architecture, limitations, and contribution guidance.
3. Run `python -m compileall`, the full unit suite, JSON validation, placeholder scan, and a noninteractive Streamlit startup smoke test when Streamlit is installed.

## Review focus

- Malformed Ollama output must never bypass score clamping or verdict normalization.
- A malformed `patterns.json` must preserve usable built-in detection.
- URLScan must be opt-in, keyless, labeled external, and fail closed to a warning rather than a crash.
- OCR must distinguish missing Python integration from a missing Tesseract executable.
- Streamlit must never render user/model content through unsafe HTML.
