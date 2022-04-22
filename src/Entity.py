from pygame import Surface

from src.Collider import Collider
from src.LevelObject import LevelObject
from src.Vector import Vector
from src.Physics import Physics


class Entity(LevelObject):

    def __init__(self, position: Vector, size: Vector, texture_name: str, physics: Physics):
        super().__init__(position)
        self.size = size
        self.texture_name = texture_name
        self.speed = Vector(0, 0)
        self.physics = physics

    def move(self, distance: Vector, dt: float):
        self.position += distance
        self.speed += self.physics.acceleration * dt

    def jump(self):
        self.speed.y = self.physics.jump_speed

    def update(self, dt: float):
        self.speed.x -= self.physics.acceleration.x * dt
        self.speed.y += self.physics.acceleration.y * dt

        self.position += self.speed * dt

    def draw(self, surface: Surface, offset: Vector):
        pass

    def calc_collision(self, collider: Collider):
        pass

    def get_collider(self) -> Collider:
        pass
