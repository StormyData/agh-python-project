from src.LevelObjects.LevelObject import LevelObject
from src.LevelObjects.Platforms import Platform

class Level:
    def __init__(self, objects: [LevelObject], background_texture_name: str):
        self.objects = objects
        self.background_texture_name = background_texture_name

    def update(self, dt: float):
        for game_object in self.objects:
            if isinstance(game_object, Platform):
                game_object.update(dt)
