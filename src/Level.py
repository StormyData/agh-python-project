from pygame import Surface

from src.LevelObject import LevelObject


class Level:
    def __init__(self, objects: [LevelObject]):
        self.objects = objects

    def update(self, dt: float):
        pass

    def draw(self, surface: Surface):
        pass
