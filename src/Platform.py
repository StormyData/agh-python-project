from pygame import Surface

from src.Collider import Collider
from src.LevelObject import LevelObject
from src.Vector import Vector


class Platform(LevelObject):
    def __init__(self, position: Vector, size: Vector, texture_name: str):
        super().__init__(position)
        self.size = size
        self.texture_name = texture_name

    def draw(self, surface: Surface):
        pass

    def get_collider(self) -> Collider:
        pass
