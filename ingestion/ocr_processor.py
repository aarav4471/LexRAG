import pytesseract
from PIL import Image


class OCRProcessor:

    @staticmethod
    def extract_text(image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)