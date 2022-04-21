from pygame.surface import Surface

from src.Entity import Entity
from src.Vector import Vector

from pygame import gfxdraw
from src.AssetLoader import AssetLoader

class Player(Entity):
    def __init__(self, position: Vector, size: Vector, texture_name: str):
        super().__init__(position, size, texture_name)
        self.facing_left = True

    def flip(self):
        self.facing_left = not self.facing_left

    def move(self, distance: Vector):
        self.position += distance

    def draw(self, window: Surface, offset: Vector):
        texture = AssetLoader.get_singleton().get_image(self.texture_name)
        # window.blit(texture, (self.position.x, self.position.y), (0, 0, self.size.x + 100, self.size.y + 100))
        gfxdraw.textured_polygon(window, [(self.position.x + offset.x, self.position.y + offset.y),
                                          (self.position.x + offset.x, self.position.y + self.size.y + offset.y),
                                          (self.position.x + self.size.x + offset.x,
                                           self.position.y + self.size.y + offset.y),
                                          (self.position.x + self.size.x + offset.x, self.position.y + offset.y)],
                                 texture, 0, 0)


