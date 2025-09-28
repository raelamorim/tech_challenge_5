from abc import ABC, abstractmethod


class ImageService(ABC):
    @abstractmethod
    def get_image_and_markdown(self, image) -> dict:
        pass
