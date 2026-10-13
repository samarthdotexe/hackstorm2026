"""Behavior tests for ScamShield's detection core."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from detector import (
    ModelAssessment,
    OllamaAnalyzer,
    PatternDatabase,
    ScamDetector,
    clamp_score,
    parse_model_payload,
    verdict_for_score,
)


class ScoreTests(unittest.TestCase):
    def test_clamp_score_rejects_non_finite_and_bounds_numbers(self) -> None:
        self.assertEqual(clamp_score(-5), 0)
        self.assertEqual(clamp_score(115.4), 100)
        self.assertEqual(clamp_score(float("nan")), 0)

    def test_verdict_thresholds_are_normalized(self) -> None:
        self.assertEqual(verdict_for_score(34.9), "safe")
        self.assertEqual(verdict_for_score(35), "suspicious")
        self.assertEqual(verdict_for_score(70), "scam")


class PatternDatabaseTests(unittest.TestCase):
    def test_malformed_file_falls_back_to_builtin_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "patterns.json"
            path.write_text("{not valid json", encoding="utf-8")
            database = PatternDatabase.from_file(path)

        matches = database.match("Share your OTP now to unblock your account")
        self.assertTrue(matches)
        self.assertTrue(any("OTP" in match.tactic for match in matches))
        self.assertTrue(database.warnings)

    def test_community_patterns_detect_indian_upi_scam(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "patterns.json"
            path.write_text(
                json.dumps(
                    {
                        "patterns": [
                            {
                                "id": "upi-collect",
                                "regex": "approve\\s+(?:the\\s+)?upi\\s+collect",
                                "weight": 48,
                                "tactic": "UPI collect request",
                                "explanation": "Receiving money never requires approving a collect request.",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            matches = PatternDatabase.from_file(path).match(
                "Approve the UPI collect request to receive your refund"
            )

        self.assertEqual(matches[0].identifier, "upi-collect")
        self.assertEqual(matches[0].weight, 48)

    def test_null_pattern_fields_activate_builtin_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "patterns.json"
            path.write_text(
                json.dumps(
                    {
                        "patterns": [
                            {
                                "id": None,
                                "regex": None,
                                "weight": "heavy",
                                "tactic": None,
                                "explanation": None,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            database = PatternDatabase.from_file(path)

        self.assertTrue(database.warnings)
        self.assertTrue(database.match("Please share your OTP now"))

    def test_extreme_integer_weight_is_clamped_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "patterns.json"
            path.write_text(
                json.dumps(
                    {
                        "patterns": [
                            {
                                "id": "extreme",
                                "regex": "extreme",
                                "weight": 10**400,
                                "tactic": "Extreme value",
                                "explanation": "The score is clamped.",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            matches = PatternDatabase.from_file(path).match("extreme")

        self.assertEqual(matches[0].weight, 100)


class ModelPayloadTests(unittest.TestCase):
    def test_parser_extracts_fenced_json_and_clamps_score(self) -> None:
        payload = parse_model_payload(
            'Analysis follows.```json\n{"risk_score": 140, "verdict": "dangerous", '
            '"explanation": "Credential theft attempt", "tactics": ["impersonation"]}\n```'
        )

        self.assertIsNotNone(payload)
        assert payload is not None
        self.assertEqual(payload.score, 100)
        self.assertEqual(payload.verdict, "scam")
        self.assertEqual(payload.tactics, ("impersonation",))

    def test_parser_rejects_non_json_model_output(self) -> None:
        self.assertIsNone(parse_model_payload("I cannot produce the requested structure."))

    def test_parser_rejects_missing_or_non_numeric_scores(self) -> None:
        self.assertIsNone(parse_model_payload("{}"))
        self.assertIsNone(parse_model_payload('{"risk_score": null}'))
        self.assertIsNone(parse_model_payload('{"risk_score": "high", "verdict": "scam"}'))


class OllamaAnalyzerTests(unittest.TestCase):
    def test_analyzer_uses_loopback_client_with_finite_timeout(self) -> None:
        captured: dict[str, object] = {}

        class FakeClient:
            def chat(self, **kwargs: object) -> dict[str, object]:
                return {
                    "message": {
                        "content": '{"risk_score": 82, "explanation": "High pressure payment request", "tactics": []}'
                    }
                }

        def client_factory(**kwargs: object) -> FakeClient:
            captured.update(kwargs)
            return FakeClient()

        assessment, warning = OllamaAnalyzer(
            "gemma2:2b",
            client_factory=client_factory,
        ).analyze("Pay immediately")

        self.assertIsNone(warning)
        self.assertEqual(assessment.score if assessment else None, 82)
        self.assertEqual(captured["host"], "http://127.0.0.1:11434")
        self.assertEqual(captured["timeout"], 45.0)
        self.assertIs(captured["follow_redirects"], False)
        self.assertIs(captured["trust_env"], False)


class ScamDetectorTests(unittest.TestCase):
    def test_deterministic_result_survives_unavailable_model(self) -> None:
        class UnavailableAnalyzer:
            def analyze(self, text: str) -> tuple[ModelAssessment | None, str | None]:
                return None, "Ollama is unavailable; showing local pattern results only."

        result = ScamDetector(model_analyzer=UnavailableAnalyzer()).analyze(
            "URGENT: share your OTP and pay a processing fee immediately"
        )

        self.assertGreaterEqual(result.score, 35)
        self.assertIn(result.verdict, {"suspicious", "scam"})
        self.assertTrue(result.pattern_matches)
        self.assertTrue(any("Ollama" in warning for warning in result.warnings))

    def test_empty_text_returns_safe_explained_result(self) -> None:
        result = ScamDetector().analyze("   ")

        self.assertEqual(result.score, 0)
        self.assertEqual(result.verdict, "safe")
        self.assertIn("No content", result.explanation)

    def test_high_model_risk_is_not_diluted_by_absent_pattern_matches(self) -> None:
        class HighRiskAnalyzer:
            def analyze(self, text: str) -> tuple[ModelAssessment | None, str | None]:
                return ModelAssessment(100, "scam", "Clear impersonation", ("impersonation",)), None

        result = ScamDetector(model_analyzer=HighRiskAnalyzer()).analyze("Call the supplied number")

        self.assertEqual(result.score, 100)
        self.assertEqual(result.verdict, "scam")


if __name__ == "__main__":
    unittest.main()
