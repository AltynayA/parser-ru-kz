from pdf2image import convert_from_path
from PIL import Image

def pdf_to_images(pdf_path: str):
    # Convert each PDF page to a PIL Image
    images = convert_from_path(pdf_path)
    return images
