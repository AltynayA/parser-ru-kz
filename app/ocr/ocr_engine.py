from PIL import Image
import pytesseract

def image_to_text(image: Image.Image) -> str:
    # Simple OCR, preserves Kazakh, Russian, and English
    return pytesseract.image_to_string(
        image,
        lang="rus+kaz+eng",  # add languages as needed
        config="--psm 3"     # Full page OCR
    )
