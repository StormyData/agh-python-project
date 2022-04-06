from pygame import Surface, gfxdraw
from src.Collider import Collider
from src.LevelObject import LevelObject
from src.Vector import Vector
from src.AssetLoader import AssetLoader


class Platform(LevelObject):
    def __init__(self, position: Vector, size: Vector, texture_name: str):
        super().__init__(position)
        self.size = size
        self.texture_name = texture_name

    def draw(self, window: Surface, offset: Vector):
        texture = AssetLoader.get_singleton().get_image(self.texture_name)
        # window.blit(texture, (self.position.x, self.position.y), (0, 0, self.size.x + 100, self.size.y + 100))
        gfxdraw.textured_polygon(window, [(self.position.x + offset.x, self.position.y + offset.y),
                                          (self.position.x + offset.x, self.position.y + self.size.y + offset.y),
                                          (self.position.x + self.size.x + offset.x,
                                           self.position.y + self.size.y + offset.y),
                                          (self.position.x + self.size.x + offset.x, self.position.y + offset.y)],
                                 texture, 0, 0)

    def get_collider(self) -> Collider:
        pass
