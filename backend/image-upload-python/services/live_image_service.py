import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
    
    
from services.image_service import ImageService
from adapters.openai_adapter import StrideAPI
from adapters.render_image_adapter import render_overlay_on_image

def base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def resources_path(*parts):
    return os.path.join(base_dir(), "../resources", *parts)

def load_prompt() -> str:
    p = resources_path("prompt.txt")
    with open(p, "r", encoding="utf-8") as fh:
        return fh.read()


class LiveImageService(ImageService):
    def get_image_and_markdown(self, image) -> dict:
        prompt = load_prompt()
        api = StrideAPI()

        markdown_content, overlay_content = api.analyze_and_annotate(
            image_base64=image,
            prompt=prompt
        )

        image = render_overlay_on_image(
            image_base64=image,
            overlay_spec=overlay_content,
        )
        
        return {
            "image": image,
            "markdown": markdown_content
        }