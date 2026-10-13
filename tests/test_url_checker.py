"""Behavior tests for URL normalization and reputation analysis."""

from __future__ import annotations

import io
import json
import unittest

from url_checker import analyze_url, extract_urls, normalize_url


class UrlNormalizationTests(unittest.TestCase):
    def test_normalize_url_adds_https_and_rejects_unsafe_schemes(self) -> None:
        self.assertEqual(normalize_url("example.com/login"), "https://example.com/login")
        self.assertIsNone(normalize_url("javascript:alert(1)"))
        self.assertIsNone(normalize_url("not a url"))

    def test_normalize_url_rejects_malformed_hosts_without_raising(self) -> None:
        self.assertIsNone(normalize_url("https://["))
        self.assertIsNone(normalize_url("https://example..com"))

    def test_normalize_url_preserves_ipv6_brackets(self) -> None:
        self.assertEqual(
            normalize_url("https://[2001:db8::1]/login"),
            "https://[2001:db8::1]/login",
        )
        self.assertEqual(
            normalize_url("https://[2001:db8::1]"),
            "https://[2001:db8::1]",
        )

    def test_extract_urls_trims_sentence_punctuation(self) -> None:
        self.assertEqual(
            extract_urls("Review https://example.com/pay, then reply."),
            ("https://example.com/pay",),
        )


class UrlAnalysisTests(unittest.TestCase):
    def test_risky_ip_http_url_produces_explainable_score(self) -> None:
        result = analyze_url("http://192.0.2.4/verify-account")

        self.assertGreaterEqual(result.score, 35)
        self.assertTrue(any("IP address" in signal for signal in result.signals))
        self.assertTrue(any("unencrypted" in signal for signal in result.signals))
        self.assertFalse(result.external_checked)

    def test_urlscan_result_raises_score_when_malicious(self) -> None:
        search_body = json.dumps(
            {
                "results": [
                    {
                        "_id": "scan-id",
                        "page": {"url": "https://bad.example"},
                        "task": {"url": "https://bad.example"},
                    }
                ]
            }
        ).encode()
        result_body = json.dumps(
            {"verdicts": {"overall": {"malicious": True}, "urlscan": {"malicious": True}}}
        ).encode()

        def opener(request: object, timeout: float) -> io.BytesIO:
            if "/search/" in request.full_url:
                self.assertIn("canonical.page.url", request.full_url)
                self.assertNotIn("verdicts.malicious", request.full_url)
                return io.BytesIO(search_body)
            self.assertIn("/result/scan-id/", request.full_url)
            return io.BytesIO(result_body)

        result = analyze_url("https://bad.example", use_urlscan=True, opener=opener)

        self.assertTrue(result.external_checked)
        self.assertGreaterEqual(result.score, 70)
        self.assertIn("malicious", result.reputation_summary.lower())

    def test_urlscan_ignores_mismatched_search_results(self) -> None:
        body = json.dumps(
            {"results": [{"_id": "scan-id", "page": {"url": "https://other.example"}}]}
        ).encode()

        def opener(request: object, timeout: float) -> io.BytesIO:
            return io.BytesIO(body)

        result = analyze_url("https://bad.example", use_urlscan=True, opener=opener)

        self.assertTrue(result.external_checked)
        self.assertLess(result.score, 70)
        self.assertIn("no exact public scan", result.reputation_summary.lower())

    def test_urlscan_network_failure_returns_warning(self) -> None:
        def failing_opener(request: object, timeout: float) -> io.BytesIO:
            raise OSError("network blocked")

        result = analyze_url("https://example.com", use_urlscan=True, opener=failing_opener)

        self.assertFalse(result.external_checked)
        self.assertTrue(any("URLScan" in warning for warning in result.warnings))

    def test_invalid_url_returns_zero_score_without_exception(self) -> None:
        result = analyze_url("javascript:alert(1)")

        self.assertEqual(result.score, 0)
        self.assertTrue(result.warnings)


if __name__ == "__main__":
    unittest.main()
