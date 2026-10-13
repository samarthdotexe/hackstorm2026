"""UI boundary tests that do not require a browser."""

from __future__ import annotations

import unittest
from pathlib import Path

from app import preview_image
from streamlit.testing.v1 import AppTest


class PreviewTests(unittest.TestCase):
    def test_preview_failure_returns_warning_instead_of_raising(self) -> None:
        def failing_renderer(image: object, **kwargs: object) -> None:
            raise ValueError("not an image")

        warning = preview_image(b"corrupt image", renderer=failing_renderer)

        self.assertIsNotNone(warning)
        self.assertIn("preview", warning.lower())


class StreamlitInteractionTests(unittest.TestCase):
    def test_empty_submission_warns_without_crashing(self) -> None:
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        application = AppTest.from_file(str(app_path)).run(timeout=10)

        self.assertFalse(application.exception)
        application.button[0].click().run(timeout=10)

        self.assertFalse(application.exception)
        self.assertTrue(
            any("before analyzing" in warning.value for warning in application.warning)
        )


if __name__ == "__main__":
    unittest.main()
