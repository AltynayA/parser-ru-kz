from PIL import Image
import pytesseract
from pytesseract import Output

def image_to_text(image: Image.Image) -> str:
    # Simple OCR, preserves Kazakh, Russian, and English
    return pytesseract.image_to_string(
        image,
        lang="rus+kaz+eng",  # add languages as needed
        config="--psm 3"     # Full page OCR
    )


def crop_under_keyword(
    image: Image.Image,
    keyword: str,
    margin: int = 10
) -> Image.Image | None:
    """
    Finds the keyword and crops the image BELOW it.
    Returns None if keyword is not found.
    """

    data = pytesseract.image_to_data(
        image,
        lang="rus+kaz+eng",
        output_type=Output.DICT
    )

    img_w, img_h = image.size

    for i, word in enumerate(data["text"]):
        if not word:
            continue

        if keyword.lower() in word.lower():
            x = data["left"][i]
            y = data["top"][i]
            h = data["height"][i]

            crop_top = min(y + h + margin, img_h)

            return image.crop((
                0,
                crop_top,
                img_w,
                img_h
            ))

    return None