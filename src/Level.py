from .LevelObjects.Entities import Monster
from .LevelObjects.LevelObject import LevelObject
from .LevelObjects.Platforms import Platform
from .Vector import Vector


class Level:
    def __init__(self, objects: [LevelObject], background_texture_name: str, level_name: str,
                 initial_player_pos: Vector):
        self.objects = objects
        self._find_entities(objects)
        self.background_texture_name = background_texture_name
        self.level_name = level_name
        self.initial_player_pos = initial_player_pos

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
