# Contributing to ScamShield OSS

Thank you for helping make scam warnings clearer and more useful.

## Development setup

1. Fork and clone the repository.
2. Create a virtual environment with Python 3.11 or newer.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Install Ollama and Tesseract if you plan to test those integrations.
5. Run `python -m unittest discover -s tests -v` before opening a pull request.

## Adding a detection pattern

Edit `patterns.json` and add one narrowly scoped entry with:

- a unique kebab-case `id`;
- a conservative, case-insensitive-compatible `regex`;
- a `weight` from 0 to 100;
- a short plain-language `tactic` name; and
- an `explanation` that helps a non-technical user act safely.

Avoid patterns that identify protected groups, contain personal data, or match broad everyday language. Add a unit test that demonstrates a true positive and, when the expression is broad, a nearby legitimate message that must not match.

## Code contributions

- Keep modules focused and public functions typed and documented.
- Add behavior tests before implementation changes.
- Preserve graceful fallback behavior for every optional service.
- Do not add telemetry, secrets, API keys, or remote text-analysis services.
- Never render submitted or model-generated content as HTML.

Use clear commit messages and explain the user-facing reason for the change in the pull request. By contributing, you agree that your contribution is licensed under the MIT License.
