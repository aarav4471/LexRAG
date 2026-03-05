from PIL import Image
import pytesseract


class ImageProcessor:

    def process(self, image_path):
        # Open image
        image = Image.open(image_path)

        # OCR text extraction
        extracted_text = pytesseract.image_to_string(image)

        # Return text only (no image embeddings)
        return {
            "text": extracted_text
        }