"""Streamlit interface for ScamShield OSS."""

from __future__ import annotations

from typing import Any, Callable, Final

try:
    import streamlit as st
except ImportError as exc:  # pragma: no cover - Streamlit displays the application itself.
    raise SystemExit("Streamlit is not installed. Run: pip install -r requirements.txt") from exc

from detector import OllamaAnalyzer, RiskResult, ScamDetector
from ocr import MAX_IMAGE_BYTES, extract_text
from url_checker import URLAnalysis, analyze_url, extract_urls


APP_TITLE: Final = "ScamShield OSS"
MAX_URLS_PER_ANALYSIS: Final = 5


def configure_page() -> None:
    """Apply page metadata and static dark-theme styles."""

    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        :root { color-scheme: dark; }
        @keyframes scan-entry {
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stApp {
            background:
                radial-gradient(circle at 12% 0%, rgba(99, 102, 241, .20), transparent 28%),
                radial-gradient(circle at 90% 18%, rgba(244, 63, 94, .13), transparent 24%),
                #030303;
            animation: scan-entry .52s cubic-bezier(.16, 1, .3, 1) both;
        }
        .scan-shape-layer { position: fixed; inset: 0; overflow: hidden; pointer-events: none; z-index: 0; }
        .scan-shape {
            position: absolute;
            border: 2px solid rgba(255,255,255,.14);
            border-radius: 999px;
            box-shadow: 0 8px 32px rgba(255,255,255,.08);
            background: linear-gradient(90deg, rgba(129,140,248,.14), transparent);
            backdrop-filter: blur(2px);
        }
        .scan-shape-one { width: 600px; height: 140px; left: -8%; top: 18%; transform: rotate(12deg); }
        .scan-shape-two { width: 500px; height: 120px; right: -8%; top: 74%; transform: rotate(-15deg); background: linear-gradient(90deg, rgba(244,63,94,.14), transparent); }
        .scan-shape-three { width: 300px; height: 80px; left: 10%; bottom: 8%; transform: rotate(-8deg); background: linear-gradient(90deg, rgba(167,139,250,.14), transparent); }
        .scan-shape-four { width: 200px; height: 60px; right: 20%; top: 14%; transform: rotate(20deg); background: linear-gradient(90deg, rgba(251,191,36,.14), transparent); }
        .scan-shape-five { width: 150px; height: 40px; left: 26%; top: 8%; transform: rotate(-25deg); background: linear-gradient(90deg, rgba(34,211,238,.14), transparent); }
        [data-testid="stSidebar"] { background: rgba(11, 11, 16, .94); border-right: 1px solid rgba(255,255,255,.10); }
        [data-testid="stHeader"] { background: transparent; }
        .block-container { position: relative; z-index: 1; max-width: 1120px; padding-top: 4rem; }
        h1, h2, h3 { letter-spacing: -0.035em; }
        [data-testid="stMetric"], [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255,255,255,.035);
            border: 1px solid rgba(255,255,255,.10);
            border-radius: 16px;
            padding: 1rem;
            backdrop-filter: blur(12px);
        }
        button[kind="primary"] {
            border-radius: 999px;
            border: 0;
            background: #fff;
            color: #050505;
            font-weight: 700;
            min-height: 3rem;
            transition: transform .2s ease, background .2s ease;
        }
        button[kind="primary"]:hover { background: rgba(255,255,255,.88); transform: translateY(-1px); }
        .app-kicker {
            display: inline-flex;
            align-items: center;
            gap: .55rem;
            padding: .4rem .8rem;
            border: 1px solid rgba(255,255,255,.12);
            border-radius: 999px;
            color: rgba(255,255,255,.68);
            background: rgba(255,255,255,.035);
            font-size: .85rem;
            letter-spacing: .03em;
        }
        .app-kicker::before { content: ""; width: .5rem; height: .5rem; border-radius: 999px; background: #34d399; }
        .app-hero { margin: .25rem 0 2.25rem; }
        .app-hero h1 { margin: .85rem 0 .75rem; font-size: clamp(2.3rem, 6vw, 4.7rem); line-height: .96; }
        .app-hero p { max-width: 42rem; color: rgba(255,255,255,.55); font-size: 1.05rem; line-height: 1.65; }
        .privacy-note {
            background: rgba(255,255,255,.035);
            border: 1px solid rgba(255,255,255,.10);
            border-radius: 16px;
            padding: .95rem 1.1rem;
            color: rgba(255,255,255,.72);
            margin-bottom: 1.5rem;
        }
        [data-testid="stFileUploader"], [data-testid="stTextArea"], [data-testid="stTextInput"] {
            background: rgba(255,255,255,.025);
            border-radius: 16px;
        }
        @media (prefers-reduced-motion: reduce) {
            .stApp { animation: none; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner=False)
def build_detector(model_name: str) -> ScamDetector:
    """Create and cache a detector for the selected local Ollama model."""

    return ScamDetector(model_analyzer=OllamaAnalyzer(model_name))


def render_url_details(results: tuple[URLAnalysis, ...]) -> None:
    """Render URL checks using safe Streamlit text components."""

    if not results:
        return
    with st.expander("URL analysis", expanded=True):
        for result in results:
            st.text(result.url or "Invalid URL")
            st.text(f"URL risk score: {result.score}/100")
            for signal in result.signals:
                st.text(f"• {signal}")
            st.caption(result.reputation_summary)
            for warning in result.warnings:
                st.warning(warning)


def render_result(result: RiskResult, url_results: tuple[URLAnalysis, ...]) -> None:
    """Render a unified result without interpreting untrusted text as HTML."""

    color_message = {
        "safe": st.success,
        "suspicious": st.warning,
        "scam": st.error,
    }[result.verdict]
    color_message(f"Verdict: {result.verdict.upper()}")

    score_column, source_column = st.columns([1, 2])
    with score_column:
        st.metric("Risk score", f"{result.score}/100")
        st.progress(result.score)
    with source_column:
        st.subheader("Why this result")
        st.text(result.explanation)
        if result.sources:
            st.caption("Signals used: " + ", ".join(result.sources))

    if result.tactics:
        st.subheader("Tactics detected")
        for tactic in result.tactics:
            st.text(f"• {tactic}")

    if result.pattern_matches:
        with st.expander("Community pattern evidence"):
            for match in result.pattern_matches:
                st.text(f"{match.tactic} · +{match.weight} rule weight")
                st.text(match.explanation)
                st.text(f"Matched text: {match.evidence}")

    render_url_details(url_results)
    for warning in result.warnings:
        st.warning(warning)

    st.info(
        "Safety step: do not reply, pay, share credentials, install remote-access apps, or call numbers "
        "in the message. Verify through the organization's official website or phone number."
    )


def _analyze_urls(values: tuple[str, ...], external_lookup: bool) -> tuple[URLAnalysis, ...]:
    return tuple(
        analyze_url(value, use_urlscan=external_lookup)
        for value in values[:MAX_URLS_PER_ANALYSIS]
    )


def preview_image(
    image: object,
    *,
    renderer: Callable[..., Any] | None = None,
) -> str | None:
    """Preview a validated upload and turn rendering errors into a warning."""

    try:
        (renderer or st.image)(image, caption="Uploaded screenshot", width=700)
    except Exception as exc:
        return f"The screenshot preview could not be rendered ({type(exc).__name__})."
    return None


def main() -> None:
    """Run the ScamShield Streamlit application."""

    configure_page()
    st.markdown(
        """
        <div class="scan-shape-layer" aria-hidden="true">
          <div class="scan-shape scan-shape-one"></div>
          <div class="scan-shape scan-shape-two"></div>
          <div class="scan-shape scan-shape-three"></div>
          <div class="scan-shape scan-shape-four"></div>
          <div class="scan-shape scan-shape-five"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <section class="app-hero">
          <span class="app-kicker">Local-first scam intelligence</span>
          <h1>Scan. Understand.<br/>Stay safe.</h1>
          <p>Check suspicious messages, screenshots, job offers, and links before you trust them.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="privacy-note">Text and screenshot analysis stay on this device when Ollama '
        "is available. URLScan is an optional external network lookup and is off by default.</div>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Analysis settings")
        model_choice = st.selectbox(
            "Local Ollama model",
            ("gemma2:2b", "qwen2.5:0.5b", "Custom model…"),
            help="The selected model must already be pulled in Ollama.",
        )
        if model_choice == "Custom model…":
            model_name = st.text_input("Custom Ollama model name", value="gemma2:2b").strip()
        else:
            model_name = model_choice
        external_lookup = st.toggle(
            "Use URLScan.io reputation",
            value=False,
            help="Sends submitted URLs to URLScan.io's public search API. No API key is used.",
        )
        if external_lookup:
            st.warning("External lookup enabled: URLs will leave this device and be sent to URLScan.io.")
        ocr_language = st.text_input(
            "Tesseract language",
            value="eng",
            help="Examples: eng, hin, or eng+hin. The language data must be installed locally.",
        )
        st.divider()
        st.caption("ScamShield provides risk guidance, not a guarantee or legal advice.")

    mode = st.radio(
        "What would you like to check?",
        ("Message", "Screenshot", "URL"),
        horizontal=True,
    )

    content = ""
    direct_urls: tuple[str, ...] = ()
    input_warnings: list[str] = []

    if mode == "Message":
        content = st.text_area(
            "Paste the suspicious message",
            height=220,
            max_chars=20000,
            placeholder="Paste an SMS, WhatsApp message, email, or job offer here…",
        )
    elif mode == "Screenshot":
        uploaded = st.file_uploader(
            "Upload a screenshot",
            type=("png", "jpg", "jpeg", "webp", "bmp", "tiff"),
            help="Maximum processed size: 12 MB. OCR runs through local Tesseract.",
        )
        if uploaded is not None:
            uploaded_bytes = uploaded.getvalue()
            ocr_result = extract_text(uploaded_bytes, ocr_language)
            input_warnings.extend(ocr_result.warnings)
            if len(uploaded_bytes) <= MAX_IMAGE_BYTES:
                preview_warning = preview_image(uploaded)
                if preview_warning:
                    input_warnings.append(preview_warning)
            if ocr_result.success:
                content = ocr_result.text
                with st.expander("Text extracted by OCR"):
                    st.text(content)
    else:
        url_value = st.text_input(
            "Enter a URL",
            placeholder="https://example.com/verify-account",
        )
        if url_value.strip():
            direct_urls = (url_value.strip(),)
            content = url_value.strip()

    submitted = st.button("Analyze risk", type="primary", use_container_width=True)
    if not submitted:
        st.caption("No data is stored by ScamShield. Review URLScan's privacy policy before enabling it.")
        return

    for warning in input_warnings:
        st.warning(warning)
    if not content.strip() and not direct_urls:
        st.warning("Add a message, upload a readable screenshot, or enter a URL before analyzing.")
        return

    discovered_urls = direct_urls or extract_urls(content)
    with st.spinner("Checking patterns and asking the local model…"):
        url_results = _analyze_urls(discovered_urls, external_lookup)
        result = build_detector(model_name).analyze(content, url_results)
    render_result(result, url_results)


if __name__ == "__main__":
    main()
