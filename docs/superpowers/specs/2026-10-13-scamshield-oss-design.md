# ScamShield OSS Design

## Goal

Build a local-first Streamlit application that helps everyday users assess suspicious messages, job offers, phishing attempts, URLs, and screenshots. It combines explainable community patterns with optional local Ollama reasoning and optional external URLScan reputation data.

## Architecture

- `detector.py` owns normalized risk results, defensive pattern loading and matching, defensive Ollama parsing, and score fusion.
- `url_checker.py` owns URL extraction, normalization, deterministic URL heuristics, and opt-in URLScan search.
- `ocr.py` owns optional Pillow preprocessing and optional Tesseract extraction.
- `app.py` owns the Streamlit interface and never treats user or model text as HTML.
- `patterns.json` is the editable community rule database.

The deterministic path is always usable. Ollama enriches the result when installed and reachable. OCR and URLScan failures become user-visible warnings rather than crashes.

## Scoring and Verdicts

Every contributing score is clamped to 0–100. Pattern evidence, URL heuristics, URLScan reputation, and Ollama output are combined with explicit weights only when each source is available. Verdicts are derived from the final score: `safe` below 35, `suspicious` from 35 through 69, and `scam` from 70 upward.

## Security and Privacy

Text and OCR analysis stay on the local machine when Ollama is available. URLScan is disabled by default, clearly labeled external, and uses its public search API without secrets. The UI displays untrusted content with Streamlit text primitives; HTML is limited to static application CSS.

## Failure Handling

Empty input is rejected without an exception. Missing Python packages, missing executables, unavailable models and services, malformed JSON, invalid pattern data, invalid URLs, unsupported images, timeouts, and malformed model responses return actionable warnings while preserving deterministic results.

## Verification

Standard-library unit tests cover score clamping, verdict boundaries, malformed patterns, pattern matching, Ollama response parsing/fallback, URL validation and heuristics, URLScan failure handling, and OCR dependency/error handling. Final checks compile all Python modules, run the complete test suite, and import the Streamlit application when dependencies permit.
