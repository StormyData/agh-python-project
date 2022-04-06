from pygame import Surface, gfxdraw

from src.LevelObject import LevelObject
from src.Vector import Vector
from src.AssetLoader import AssetLoader


class Level:
    def __init__(self, objects: [LevelObject], background_texture_name: str):
        self.objects = objects
        self.background_texture_name = background_texture_name

    def update(self, dt: float):
        pass

    def draw(self, surface: Surface, offset: Vector):
        background = AssetLoader.get_singleton().get_image(self.background_texture_name)
        width = surface.get_width()
        height = surface.get_height()
        gfxdraw.textured_polygon(surface, [(0, 0),
                                           (0, height),
                                           (width, height),
                                           (width, 0)], background, 0, 0)

        for game_object in self.objects:
            game_object.draw(surface, offset)
