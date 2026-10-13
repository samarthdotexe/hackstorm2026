# ScamShield OSS

ScamShield OSS is a local-first scam detection app for suspicious messages, fake job offers, phishing attempts, fraudulent URLs, screenshots, and common Indian scam patterns. It combines transparent community rules with a locally running open-weight model through Ollama and presents a plain-English score from 0 to 100.

The deterministic checks still work when Ollama, Tesseract, or the network is unavailable. URLScan lookup is optional, disabled by default, and is the only feature that intentionally sends submitted data to an external service.

## What it detects

- OTP, PIN, CVV, and credential theft
- UPI collect requests and QR payment reversal tricks
- fake jobs and advance-fee demands
- KYC, SIM, electricity, parcel, customs, and authority impersonation
- “digital arrest” and remote-access-app scams
- suspicious URL structure and optional public URLScan reputation
- scam text extracted from screenshots with local Tesseract OCR

ScamShield is decision support, not a guarantee. A low score does not prove that a message or URL is safe.

## Quick start

### 1. Requirements

- Python 3.11 or newer
- [Ollama](https://ollama.com/) for local model reasoning
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for screenshots

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`.

### 2. Install the local model

Start Ollama, then pull either supported lightweight model:

```bash
ollama pull gemma2:2b
```

or:

```bash
ollama pull qwen2.5:0.5b
```

Ollama model tags can vary by release. The sidebar also accepts a custom locally installed model name.

### 3. Install Tesseract for screenshots

macOS with Homebrew:

```bash
brew install tesseract
```

Ubuntu or Debian:

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

Windows users can install a maintained Tesseract build and add its installation directory to `PATH`. Additional languages such as Hindi require the matching Tesseract language data; enter `hin` or `eng+hin` in the app after installation.

### 4. Run

```bash
streamlit run app.py
```

Paste a message, upload a screenshot, or enter a URL. The first Ollama request can take longer while the model loads.

## React landing page

The optional `frontend/` package adds a polished Next.js landing page using TypeScript, Tailwind CSS, shadcn conventions, Framer Motion, and Lucide icons. It preserves the Streamlit analyzer as the single source of detection behavior.

Run the analyzer in one terminal, then the landing page in another:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The primary CTA opens the analyzer at `http://localhost:8501`. Override that destination with `NEXT_PUBLIC_SCAMSHIELD_APP_URL` when needed. See `frontend/README.md` for component paths, shadcn CLI setup, props, and build commands.

## Privacy and network behavior

Message text and screenshot OCR stay on the machine. The Ollama client is pinned to the loopback address `127.0.0.1:11434`, does not follow redirects, and has a finite request timeout; an `OLLAMA_HOST` environment variable cannot redirect content to a remote server. No analytics, database, login, or cloud model is used.

URLScan is an optional external lookup. When enabled, the entered or extracted URL is sent to URLScan.io's public **search** endpoint to find exact historical scans. ScamShield validates each returned URL, then reads at most three matching public Result API records to check their verdicts. It does not submit pages for scanning, does not use or request an API key or paid search fields, and never labels this lookup as local. Leave the toggle off for fully local analysis.

## How scoring works

`detector.py` loads `patterns.json`, matches conservative regular expressions, and asks the selected Ollama model for structured JSON. `url_checker.py` scores URL characteristics and, only when enabled, public URLScan search results. Available signals are combined, clamped to 0–100, and mapped to exactly three verdicts:

| Score | Verdict |
| ---: | --- |
| 0–34 | `safe` |
| 35–69 | `suspicious` |
| 70–100 | `scam` |

The result includes matched tactics, plain-English reasoning, source labels, and warnings when an integration is unavailable. Deterministic evidence is never hidden by a lower model score.

## Project layout

```text
app.py                         Streamlit UI and orchestration
detector.py                    patterns, Ollama parsing, score fusion
url_checker.py                 local URL checks and optional URLScan search
ocr.py                         Pillow preprocessing and Tesseract boundary
patterns.json                  community-maintained detection rules
frontend/                      Next.js, Tailwind, and shadcn landing page
tests/                         standard-library behavior tests
.github/CONTRIBUTING.md        contribution guide
```

All project data paths resolve relative to their source files, so the app can be launched from other working directories.

## Graceful fallback behavior

- **Ollama package missing or server stopped:** community patterns and URL checks still produce a result.
- **Selected model not pulled:** the app shows an Ollama warning and retains deterministic results.
- **Pillow or pytesseract missing:** screenshot mode explains which Python dependencies to install.
- **Tesseract executable missing:** screenshot mode gives an executable/PATH warning.
- **Unsupported or unreadable image:** the upload is rejected with a safe message.
- **URLScan unavailable:** local URL signals remain visible and a warning identifies the failed external lookup.
- **Malformed `patterns.json`:** a small built-in safety rule set is activated automatically.
- **Malformed model output:** it is discarded rather than displayed or trusted.

## Tests

The test suite has no extra test framework dependency:

```bash
python -m unittest discover -s tests -v
python -m compileall app.py detector.py url_checker.py ocr.py
```

## Updating community patterns

Patterns are regular expressions stored in `patterns.json`. Keep them narrow, evidence-based, and explainable. Broad terms such as “bank” or “offer” should not be suspicious by themselves. See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) for the required fields and testing guidance.

## Responsible use

Do not use ScamShield to make automated decisions about a person. Do not paste secrets you would not ordinarily process on your computer, and remember that enabling URLScan sends URLs to an external service. If money or an account is at risk, stop communicating through the suspicious channel and contact the organization using details from its official website.

## License

ScamShield OSS is available under the [MIT License](LICENSE).
