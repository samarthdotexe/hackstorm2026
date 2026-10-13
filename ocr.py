"""Optional screenshot preprocessing and local Tesseract OCR."""

from __future__ import annotations

import io
import re
from dataclasses import dataclass
from typing import Any


MAX_IMAGE_BYTES = 12 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class OCRResult:
    """Text and non-fatal warnings produced by screenshot OCR."""

    text: str
    success: bool
    warnings: tuple[str, ...] = ()


def _load_dependencies() -> tuple[Any | None, Any | None, str | None]:
    try:
        from PIL import Image  # type: ignore[import-not-found]
        import pytesseract  # type: ignore[import-not-found]
    except ImportError:
        return (
            None,
            None,
            "OCR Python packages are missing. Install Pillow and pytesseract to analyze screenshots.",
        )
    return Image, pytesseract, None


def extract_text(image_bytes: bytes, language: str = "eng") -> OCRResult:
    """Preprocess an uploaded image and extract text with local Tesseract."""

    if not image_bytes:
        return OCRResult("", False, ("The uploaded image is empty.",))
    if len(image_bytes) > MAX_IMAGE_BYTES:
        return OCRResult("", False, ("The image is larger than the 12 MB safety limit.",))

    image_module, tesseract_module, dependency_warning = _load_dependencies()
    if dependency_warning or image_module is None or tesseract_module is None:
        return OCRResult("", False, (dependency_warning or "OCR dependencies are unavailable.",))

    safe_language = language if re.fullmatch(r"[A-Za-z0-9_+.-]{1,40}", language or "") else "eng"
    try:
        image = image_module.open(io.BytesIO(image_bytes))
        grayscale = image.convert("L")
        processed = grayscale.point(lambda pixel: 0 if pixel < 165 else 255)
        text = tesseract_module.image_to_string(
            processed,
            lang=safe_language,
            config="--oem 3 --psm 6",
        )
    except Exception as exc:
        not_found_error = getattr(tesseract_module, "TesseractNotFoundError", ())
        if not_found_error and isinstance(exc, not_found_error):
            return OCRResult(
                "",
                False,
                (
                    "The Tesseract executable is not installed or is not on PATH. "
                    "Install Tesseract, then retry the screenshot.",
                ),
            )
        return OCRResult(
            "",
            False,
            (f"The screenshot could not be processed ({type(exc).__name__}). Try a PNG or JPEG image.",),
        )

    normalized = "\n".join(line.strip() for line in str(text).splitlines() if line.strip()).strip()
    if not normalized:
        return OCRResult(
            "",
            False,
            ("Tesseract found no readable text. Try a clearer, tightly cropped screenshot.",),
        )
    return OCRResult(normalized[:20000], True)
