"""
ocr_parser.py — OCR Text Extraction for NexusOps AI
Accepts image bytes or file path, extracts text using EasyOCR
(with pytesseract as fallback), and outputs structured JSON.
"""

import re
import io
import json
from pathlib import Path
from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)

# Known error codes and model patterns for structured extraction
KNOWN_ERROR_CODES = {
    "E3", "E5", "U0", "103", "A6",
    "E1", "E2", "E4", "E6", "E7", "E8",
    "F1", "F2", "F3", "A1", "A2", "A3",
    "U1", "U2", "U3", "101", "102", "104", "105"
}

KNOWN_MODELS = [
    "30RAP", "30XA", "30HXC", "30RB", "30RA",    # Carrier
    "YVAA", "YVWA", "YKVL", "YK", "YMC2",         # York
    "CGAX", "CGWH", "RTAF", "RTHD",               # Trane
    "WMC", "WSC", "WGS",                           # McQuay
]

KNOWN_MANUFACTURERS = {
    "CARRIER": "Carrier",
    "YORK": "York",
    "TRANE": "Trane",
    "MCQUAY": "McQuay",
    "DAIKIN": "Daikin",
    "LENNOX": "Lennox",
    "JOHNSON CONTROLS": "Johnson Controls",
}


def extract_with_easyocr(image_source: Union[bytes, str, Path]) -> str:
    """
    Use EasyOCR to extract text from an image.
    Returns raw extracted text string.
    """
    try:
        import easyocr
        import numpy as np
        from PIL import Image

        reader = easyocr.Reader(["en"], gpu=False, verbose=False)

        if isinstance(image_source, (str, Path)):
            results = reader.readtext(str(image_source), detail=0, paragraph=False)
        elif isinstance(image_source, bytes):
            img = Image.open(io.BytesIO(image_source))
            img_array = np.array(img)
            results = reader.readtext(img_array, detail=0, paragraph=False)
        else:
            raise ValueError("image_source must be bytes, str, or Path")

        raw_text = "\n".join(results)
        logger.info(f"[EasyOCR] Extracted {len(results)} text blocks")
        return raw_text

    except ImportError:
        logger.warning("[EasyOCR] Not installed — trying pytesseract fallback")
        raise
    except Exception as e:
        logger.error(f"[EasyOCR] Extraction failed: {e}")
        raise


def extract_with_tesseract(image_source: Union[bytes, str, Path]) -> str:
    """
    Fallback: Use pytesseract to extract text from an image.
    """
    try:
        import pytesseract
        from PIL import Image

        if isinstance(image_source, bytes):
            img = Image.open(io.BytesIO(image_source))
        elif isinstance(image_source, (str, Path)):
            img = Image.open(str(image_source))
        else:
            raise ValueError("image_source must be bytes, str, or Path")

        # Tesseract config for control panel text (alphanumeric, clear font)
        config = "--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-/ "
        raw_text = pytesseract.image_to_string(img, config=config)
        logger.info(f"[pytesseract] Extracted {len(raw_text)} characters")
        return raw_text

    except ImportError:
        logger.error("[pytesseract] Not installed — OCR unavailable")
        raise RuntimeError("No OCR engine available. Install easyocr or pytesseract.")
    except Exception as e:
        logger.error(f"[pytesseract] Extraction failed: {e}")
        raise


def extract_text(image_source: Union[bytes, str, Path]) -> str:
    """
    Extract text from image, trying EasyOCR first then pytesseract fallback.
    """
    try:
        return extract_with_easyocr(image_source)
    except Exception:
        logger.info("[OCR] Falling back to pytesseract")
        return extract_with_tesseract(image_source)


def parse_error_code(text: str) -> Optional[str]:
    """
    Extract error/alarm code from OCR text.
    Tries known codes first, then regex patterns.
    """
    text_upper = text.upper()

    # Check known codes directly
    for code in KNOWN_ERROR_CODES:
        # Look for the code as a standalone token (not part of longer string)
        if re.search(rf"\b{re.escape(code)}\b", text_upper):
            return code

    # Regex patterns for alarm codes
    patterns = [
        r"\bALARM[:\s]+([A-Z]\d+|\d{3})\b",
        r"\bFAULT[:\s]+([A-Z]\d+|\d{3})\b",
        r"\bERROR[:\s]+([A-Z]\d+|\d{3})\b",
        r"\bCODE[:\s]+([A-Z]\d+|\d{3})\b",
        r"\b([EFU]\d{1,2})\b",
        r"\b(\d{3})\b",  # 3-digit codes like 103
    ]
    for pattern in patterns:
        match = re.search(pattern, text_upper)
        if match:
            candidate = match.group(1)
            return candidate

    return None


def parse_model(text: str) -> Optional[str]:
    """
    Extract chiller model number from OCR text.
    """
    text_upper = text.upper()

    # Check known models
    for model in KNOWN_MODELS:
        if model in text_upper:
            # Try to extract full model with suffix (e.g., 30RAP060)
            idx = text_upper.find(model)
            # Grab surrounding context
            snippet = text_upper[max(0, idx - 5): idx + len(model) + 10]
            full_model_match = re.search(
                rf"{re.escape(model)}[\s\-]?([0-9A-Z]{{0,6}})", snippet
            )
            if full_model_match:
                suffix = full_model_match.group(1).strip()
                return f"{model}{suffix}" if suffix else model
            return model

    # Generic model pattern
    model_match = re.search(
        r"\bMODEL[:\s#]+([A-Z0-9\-]{4,20})\b", text_upper
    )
    if model_match:
        return model_match.group(1)

    return None


def parse_manufacturer(text: str) -> Optional[str]:
    """Extract manufacturer name from OCR text."""
    text_upper = text.upper()
    for keyword, name in KNOWN_MANUFACTURERS.items():
        if keyword in text_upper:
            return name
    return None


def parse_serial_number(text: str) -> Optional[str]:
    """Extract serial number from OCR text if present."""
    text_upper = text.upper()
    serial_match = re.search(
        r"(?:SERIAL|S/N|SN)[:\s#]+([A-Z0-9]{6,20})\b", text_upper
    )
    return serial_match.group(1) if serial_match else None


def parse_temperature(text: str) -> Optional[float]:
    """Extract temperature reading if visible on panel."""
    temp_match = re.search(r"(\d{1,3}\.?\d?)\s*°?[CF]\b", text, re.IGNORECASE)
    if temp_match:
        return float(temp_match.group(1))
    return None


def parse_pressure(text: str) -> Optional[float]:
    """Extract pressure reading if visible on panel."""
    pressure_match = re.search(r"(\d{2,4}\.?\d?)\s*(?:PSIG|PSI|BAR)\b", text, re.IGNORECASE)
    if pressure_match:
        return float(pressure_match.group(1))
    return None


def structure_ocr_result(raw_text: str, source: str = "ocr") -> dict:
    """
    Parse raw OCR text into a structured JSON-compatible dictionary.
    
    Returns:
    {
        "model": "Carrier 30RAP",
        "manufacturer": "Carrier",
        "error_code": "E3",
        "serial_number": "ABC12345",
        "temperature_f": 242.0,
        "pressure_psig": 665.0,
        "raw_text": "...",
        "confidence": "high|medium|low",
        "source": "easyocr|tesseract|manual"
    }
    """
    error_code = parse_error_code(raw_text)
    model = parse_model(raw_text)
    manufacturer = parse_manufacturer(raw_text)
    serial = parse_serial_number(raw_text)
    temp = parse_temperature(raw_text)
    pressure = parse_pressure(raw_text)

    # If model found, try to determine manufacturer from model prefix
    if model and not manufacturer:
        if any(m in model.upper() for m in ["30RAP", "30XA", "30HXC", "30RB"]):
            manufacturer = "Carrier"
        elif any(m in model.upper() for m in ["YVAA", "YVWA", "YK"]):
            manufacturer = "York"
        elif any(m in model.upper() for m in ["RTAF", "RTHD", "CGAX"]):
            manufacturer = "Trane"

    # Build display model string
    display_model = model
    if manufacturer and model and manufacturer.upper() not in model.upper():
        display_model = f"{manufacturer} {model}"

    # Confidence scoring
    if error_code and model:
        confidence = "high"
    elif error_code or model:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "model": display_model,
        "manufacturer": manufacturer,
        "error_code": error_code,
        "serial_number": serial,
        "temperature_f": temp,
        "pressure_psig": pressure,
        "raw_text": raw_text.strip(),
        "confidence": confidence,
        "source": source,
    }


def extract_from_image(image_source: Union[bytes, str, Path]) -> dict:
    """
    Full pipeline: Extract text from image and return structured result.
    
    Args:
        image_source: Image bytes, file path string, or Path object
        
    Returns:
        Structured dict with model, error_code, raw_text, etc.
    """
    if isinstance(image_source, bytes) and len(image_source) == 0:
        raise ValueError("Empty image bytes provided")

    ocr_source = "easyocr"
    try:
        raw_text = extract_with_easyocr(image_source)
    except Exception:
        ocr_source = "tesseract"
        try:
            raw_text = extract_with_tesseract(image_source)
        except Exception as e:
            logger.error(f"All OCR engines failed: {e}")
            return {
                "model": None,
                "manufacturer": None,
                "error_code": None,
                "serial_number": None,
                "temperature_f": None,
                "pressure_psig": None,
                "raw_text": "",
                "confidence": "failed",
                "source": "none",
                "error": str(e),
            }

    return structure_ocr_result(raw_text, source=ocr_source)


def extract_from_text_input(text: str) -> dict:
    """
    For manual text input (when no image is available),
    parse structured result from typed text.
    """
    return structure_ocr_result(text, source="manual_input")


if __name__ == "__main__":
    # Test with synthetic text
    test_text = """
    CARRIER PRO-DIALOG PLUS
    MODEL: 30RAP060
    SERIAL: 0516G12345
    ALARM ACTIVE
    CODE: E3
    HIGH PRESSURE TRIP
    DISCHARGE: 668 PSIG
    TEMP: 242F
    CONTACT SERVICE
    """
    result = extract_from_text_input(test_text)
    print(json.dumps(result, indent=2))
