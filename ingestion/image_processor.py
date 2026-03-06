from PIL import Image
import pytesseract
import torch
from transformers import CLIPProcessor, CLIPModel


class ImageProcessor:

    def __init__(self):
        """
        Initialize CLIP model for image embeddings
        """
        self.model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

    def extract_text(self, image_path):
        """
        Extract text from image using OCR
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()

        except Exception:
            return ""

    def embed_image(self, image_path):
        """
        Generate image embedding using CLIP
        """
        try:
            image = Image.open(image_path)

            inputs = self.processor(
                images=image,
                return_tensors="pt"
            )

            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)

            embedding = image_features[0].numpy()

            return embedding

        except Exception as e:
            raise Exception(f"Image embedding failed: {str(e)}")

    def process(self, image_path):
        """
        Full image processing pipeline
        """
        text = self.extract_text(image_path)
        embedding = self.embed_image(image_path)

        return {
            "text": text,
            "embedding": embedding
        }

