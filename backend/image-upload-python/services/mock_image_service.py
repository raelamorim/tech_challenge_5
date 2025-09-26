import base64
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
    
from services.image_service import ImageService

    
class MockImageService(ImageService):
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.img_path = os.path.join(self.base_path, "../assets/mock-image.png")
        self.md_path = os.path.join(self.base_path, "../assets/mock-doc.md")

    def get_image_and_markdown(self, image) -> dict:
        print("MockImageService: retornando dados mockados.")
        print(f"Imagem recebida: {image[:100] + "..." if image and len(image) > 100 else image }")
        
        if not os.path.exists(self.img_path) or not os.path.exists(self.md_path):
            raise FileNotFoundError("Arquivo(s) não encontrado(s) no diretório ./assets.")

        # Converte imagem para Base64
        with open(self.img_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode("utf-8")

        # Lê markdown
        with open(self.md_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        return {
            "image": img_base64,
            "markdown": markdown_content
        }
