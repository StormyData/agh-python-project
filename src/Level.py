from src.LevelObjects.LevelObject import LevelObject
from src.LevelObjects.Platforms import Platform
from src.LevelObjects.Entities import Monster

class Level:
    def __init__(self, objects: [LevelObject], background_texture_name: str):
        self.objects = objects
        self._find_entities(objects)
        self.background_texture_name = background_texture_name

    def _find_entities(self, objects):
        self.entities = []
        for game_object in objects:
            if isinstance(game_object, Monster):
                self.entities.append(game_object)

    def update(self, dt: float):
        for game_object in self.objects:
            if isinstance(game_object, Platform):
                game_object.update(dt)
            if isinstance(game_object, Monster):
                game_object.update(dt)
