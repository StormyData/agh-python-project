from LevelObject import LevelObject
from pygame import Surface
from Vector import Vector
from Collider import Collider


class Platform(LevelObject):
    def __init__(self, position: Vector, size: Vector, texture_name: str):
        super().__init__(position)
        self.size = size
        self.texture_name = texture_name

    def draw(self, surface: Surface):
        pass

    def get_collider(self) -> Collider:
        pass
