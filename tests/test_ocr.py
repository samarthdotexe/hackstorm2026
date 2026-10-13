"""Behavior tests for the optional OCR boundary."""

from __future__ import annotations

import unittest
from unittest.mock import patch

import ocr


class OcrTests(unittest.TestCase):
    def test_empty_image_is_rejected_without_exception(self) -> None:
        result = ocr.extract_text(b"")

        self.assertFalse(result.success)
        self.assertEqual(result.text, "")
        self.assertTrue(result.warnings)

    def test_missing_python_dependencies_return_actionable_warning(self) -> None:
        with patch.object(ocr, "_load_dependencies", return_value=(None, None, "OCR packages are missing.")):
            result = ocr.extract_text(b"image bytes")

        self.assertFalse(result.success)
        self.assertIn("missing", result.warnings[0].lower())

    def test_tesseract_executable_failure_is_graceful(self) -> None:
        class FakeImageModule:
            @staticmethod
            def open(stream: object) -> object:
                return FakeImage()

        class FakeImage:
            def convert(self, mode: str) -> "FakeImage":
                return self

            def point(self, function: object) -> "FakeImage":
                return self

        class FakeTesseract:
            class TesseractNotFoundError(Exception):
                """Test double for pytesseract's missing-executable error."""

            @staticmethod
            def image_to_string(image: object, lang: str, config: str) -> str:
                raise FakeTesseract.TesseractNotFoundError("not installed")

        with patch.object(
            ocr,
            "_load_dependencies",
            return_value=(FakeImageModule, FakeTesseract, None),
        ):
            result = ocr.extract_text(b"image bytes")

        self.assertFalse(result.success)
        self.assertTrue(any("executable" in warning.lower() for warning in result.warnings))


if __name__ == "__main__":
    unittest.main()
