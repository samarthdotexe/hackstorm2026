"""Deterministic URL checks and optional external URLScan reputation lookup."""

from __future__ import annotations

import ipaddress
import json
import re
from dataclasses import dataclass
from typing import Any, Callable
from urllib.parse import quote, urlparse, urlunparse
from urllib.request import Request, urlopen


URL_PATTERN = re.compile(r"(?:(?:https?://)|(?:www\.))[^^\s<>'\"]+", re.IGNORECASE)
SHORTENERS = {
    "bit.ly",
    "cutt.ly",
    "goo.gl",
    "is.gd",
    "rb.gy",
    "shorturl.at",
    "tinyurl.com",
    "t.co",
}
SUSPICIOUS_WORDS = {
    "account",
    "bank",
    "bonus",
    "claim",
    "kyc",
    "login",
    "pay",
    "prize",
    "refund",
    "secure",
    "update",
    "verify",
    "wallet",
}


@dataclass(frozen=True, slots=True)
class URLAnalysis:
    """Explainable URL risk information for one normalized URL."""

    url: str
    score: int
    signals: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    external_checked: bool = False
    reputation_summary: str = "External reputation lookup was not requested."


def _clamp(value: int | float) -> int:
    return max(0, min(100, round(value)))


def normalize_url(value: str) -> str | None:
    """Normalize an HTTP(S) URL, adding HTTPS when the scheme is omitted."""

    candidate = (value or "").strip().rstrip(".,;:!?)}")
    if not candidate or any(character.isspace() for character in candidate):
        return None
    try:
        if candidate.lower().startswith("www."):
            candidate = "https://" + candidate
        parsed = urlparse(candidate)
        if not parsed.scheme:
            candidate = "https://" + candidate
            parsed = urlparse(candidate)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            return None
        raw_hostname = parsed.hostname
        port = parsed.port
        try:
            address = ipaddress.ip_address(raw_hostname)
        except ValueError:
            if ".." in raw_hostname or raw_hostname.startswith(".") or raw_hostname.endswith("."):
                return None
            hostname = raw_hostname.encode("idna").decode("ascii").lower()
            if len(hostname) > 253 or any(not label for label in hostname.split(".")):
                return None
        else:
            hostname = f"[{address.compressed}]" if address.version == 6 else address.compressed
    except (UnicodeError, ValueError):
        return None
    netloc = hostname
    if port is not None:
        netloc += f":{port}"
    if parsed.username or parsed.password:
        credentials = parsed.username or ""
        if parsed.password:
            credentials += ":" + parsed.password
        netloc = credentials + "@" + netloc
    return urlunparse((parsed.scheme.lower(), netloc, parsed.path or "", "", parsed.query, ""))


def extract_urls(text: str) -> tuple[str, ...]:
    """Extract unique normalized HTTP(S) URLs from free-form text."""

    values: list[str] = []
    for match in URL_PATTERN.finditer(text or ""):
        normalized = normalize_url(match.group(0))
        if normalized and normalized not in values:
            values.append(normalized)
    return tuple(values)


def _local_signals(url: str) -> tuple[int, tuple[str, ...]]:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    score = 0
    signals: list[str] = []

    if parsed.scheme == "http":
        score += 18
        signals.append("The page uses unencrypted HTTP instead of HTTPS.")
    try:
        host_is_ip = bool(ipaddress.ip_address(host))
    except ValueError:
        host_is_ip = False
    if host_is_ip:
        score += 32
        signals.append("The link uses a raw IP address instead of a recognizable domain.")
    if "xn--" in host:
        score += 28
        signals.append("The domain uses Punycode, which can disguise look-alike characters.")
    if "@" in parsed.netloc:
        score += 25
        signals.append("The link contains an @ sign that can hide its true destination.")
    if host in SHORTENERS:
        score += 22
        signals.append("A URL shortener hides the final destination.")
    labels = [label for label in host.split(".") if label]
    if len(labels) >= 5:
        score += 15
        signals.append("The domain has an unusually deep chain of subdomains.")
    combined = f"{host}{parsed.path}".lower()
    keyword_count = sum(word in combined for word in SUSPICIOUS_WORDS)
    if keyword_count >= 2:
        score += min(24, keyword_count * 6)
        signals.append("The link contains several account, payment, or verification lure words.")
    if len(url) > 180:
        score += 12
        signals.append("The URL is unusually long and may conceal its destination.")
    if host.count("-") >= 4:
        score += 12
        signals.append("The domain contains an unusual number of hyphens.")
    return _clamp(score), tuple(signals)


def _lookup_urlscan(
    url: str,
    opener: Callable[..., Any],
    timeout: float,
) -> tuple[int | None, bool, str, str | None]:
    escaped_url = url.replace("\\", "\\\\").replace('"', '\\"')
    query = quote(f'canonical.page.url:"{escaped_url}"', safe="")
    request = Request(
        f"https://urlscan.io/api/v1/search/?q={query}&size=10",
        headers={"Accept": "application/json", "User-Agent": "ScamShield-OSS/1.0"},
    )
    try:
        with opener(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        results = payload.get("results", []) if isinstance(payload, dict) else []
        if not isinstance(results, list):
            raise ValueError("unexpected results format")
        scan_ids: list[str] = []
        for result in results:
            if not isinstance(result, dict):
                continue
            page = result.get("page", {})
            task = result.get("task", {})
            candidates = []
            if isinstance(page, dict):
                candidates.append(page.get("url"))
            if isinstance(task, dict):
                candidates.append(task.get("url"))
            identifier = result.get("_id")
            if (
                any(isinstance(item, str) and normalize_url(item) == url for item in candidates)
                and isinstance(identifier, str)
                and re.fullmatch(r"[A-Za-z0-9-]{1,80}", identifier)
            ):
                scan_ids.append(identifier)
        if not scan_ids:
            return None, True, "URLScan search found no exact public scan results for this URL.", None

        inspected = 0
        for identifier in scan_ids[:3]:
            result_request = Request(
                f"https://urlscan.io/api/v1/result/{identifier}/",
                headers={"Accept": "application/json", "User-Agent": "ScamShield-OSS/1.0"},
            )
            with opener(result_request, timeout=timeout) as response:
                result_payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(result_payload, dict):
                raise ValueError("unexpected result format")
            inspected += 1
            verdicts = result_payload.get("verdicts", {})
            if not isinstance(verdicts, dict):
                continue
            sections = (
                verdicts.get("overall", {}),
                verdicts.get("urlscan", {}),
                verdicts.get("community", {}),
            )
            if any(isinstance(section, dict) and section.get("malicious") is True for section in sections):
                return (
                    85,
                    True,
                    f"URLScan marked a historical public scan as malicious ({inspected} inspected).",
                    None,
                )
        return (
            10,
            True,
            f"URLScan inspected {inspected} exact historical scan(s); none was marked malicious.",
            None,
        )
    except Exception as exc:
        return (
            None,
            False,
            "URLScan reputation could not be checked.",
            f"URLScan external lookup failed ({type(exc).__name__}); local URL checks are still shown.",
        )


def analyze_url(
    value: str,
    *,
    use_urlscan: bool = False,
    opener: Callable[..., Any] | None = None,
    timeout: float = 6.0,
) -> URLAnalysis:
    """Analyze a URL locally and optionally query URLScan's public search API."""

    normalized = normalize_url(value)
    if normalized is None:
        return URLAnalysis(
            url=(value or "").strip(),
            score=0,
            warnings=("Enter a valid HTTP or HTTPS URL.",),
            reputation_summary="The URL was invalid, so no reputation lookup was performed.",
        )

    local_score, signals = _local_signals(normalized)
    if not use_urlscan:
        return URLAnalysis(url=normalized, score=local_score, signals=signals)

    external_score, checked, summary, warning = _lookup_urlscan(
        normalized,
        opener or urlopen,
        max(1.0, min(15.0, timeout)),
    )
    warnings = (warning,) if warning else ()
    score = max(local_score, external_score or 0)
    if external_score and external_score >= 70:
        signals = signals + ("Public URLScan results include a malicious verdict.",)
    return URLAnalysis(
        url=normalized,
        score=_clamp(score),
        signals=signals,
        warnings=warnings,
        external_checked=checked,
        reputation_summary=summary,
    )
