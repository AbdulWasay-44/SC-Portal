from typing import Optional
import io

import easyocr
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import streamlit as st


class OCRService:
    """Local OCR service backed by EasyOCR for image uploads."""

    _reader = None

    def __init__(self):
        self.reader = self._get_reader()

    @classmethod
    def _get_reader(cls):
        """Create and cache the EasyOCR reader once per process."""
        if cls._reader is None:
            try:
                cls._reader = easyocr.Reader(["en"], gpu=False, verbose=False)
            except Exception as e:
                st.error(f"Failed to initialize local OCR engine: {str(e)}")
                cls._reader = None
        return cls._reader

    def extract_text_from_image(self, uploaded_file) -> Optional[str]:
        """
        Extract text from an uploaded image file using local OCR.

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            Extracted text content or None if extraction fails
        """
        if self.reader is None:
            st.error("Local OCR engine is not available.")
            return None

        try:
            image_bytes = self.preprocess_image_for_ocr(uploaded_file)
            if not image_bytes:
                return None

            image_array = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
            results = self.reader.readtext(image_array, detail=1, paragraph=True)

            lines = []
            for item in results:
                if len(item) < 2:
                    continue
                text = str(item[1]).strip()
                confidence = float(item[2]) if len(item) > 2 else 1.0
                if text and confidence >= 0.2:
                    lines.append(text)

            extracted_text = "\n".join(lines).strip()
            if extracted_text:
                return extracted_text

            st.warning("No text detected in the image. Please try a clearer image.")
            return None

        except Exception as e:
            st.error(f"Error during OCR processing: {str(e)}")
            return None

    def extract_text_with_confidence(self, uploaded_file) -> Optional[dict]:
        """Extract text and return a basic confidence summary."""
        if self.reader is None:
            return None

        try:
            image_bytes = self.preprocess_image_for_ocr(uploaded_file)
            if not image_bytes:
                return None

            image_array = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
            results = self.reader.readtext(image_array, detail=1, paragraph=True)

            texts = []
            confidences = []
            for item in results:
                if len(item) < 2:
                    continue
                text = str(item[1]).strip()
                confidence = float(item[2]) if len(item) > 2 else 1.0
                if text:
                    texts.append(text)
                    confidences.append(confidence)

            full_text = "\n".join(texts).strip()
            if not full_text:
                return None

            average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            return {
                "full_text": full_text,
                "confidence_score": average_confidence,
            }

        except Exception as e:
            st.error(f"Error extracting OCR confidence data: {str(e)}")
            return None

    def preprocess_image_for_ocr(self, uploaded_file):
        """Preprocess image to improve OCR quality before recognition."""
        try:
            image_content = uploaded_file.read()
            uploaded_file.seek(0)

            pil_image = Image.open(io.BytesIO(image_content))
            pil_image = ImageOps.exif_transpose(pil_image).convert("RGB")

            width, height = pil_image.size
            if width < 1200 or height < 1200:
                scale_factor = max(1200 / max(width, 1), 1200 / max(height, 1))
                new_width = max(1, int(width * scale_factor))
                new_height = max(1, int(height * scale_factor))
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Improve readability without destroying anti-aliased text.
            pil_image = ImageOps.autocontrast(pil_image)
            pil_image = ImageEnhance.Sharpness(pil_image).enhance(1.8)
            pil_image = ImageEnhance.Contrast(pil_image).enhance(1.2)

            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format="PNG")
            return img_byte_arr.getvalue()

        except Exception as e:
            st.error(f"Error preprocessing image: {str(e)}")
            uploaded_file.seek(0)
            return uploaded_file.read()

    def validate_api_connection(self) -> bool:
        """Retained for compatibility; validates local OCR availability instead."""
        return self.reader is not None
