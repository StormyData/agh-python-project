from pygame import Surface


class AssetLoader:
    @staticmethod
    def get_singleton():
        pass

    def get_image(self, name: str) -> Surface:
        pass

    def get_sound_buffer(self, name: str) -> bytes:
        pass
