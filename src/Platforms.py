from pygame import Surface, gfxdraw
from src.Physics import Collider
from src.LevelObject import LevelObject
from src.Vector import Vector
from src.AssetLoader import AssetLoader

class Platform(LevelObject):
    def __init__(self, position: Vector, size: Vector, texture_name: str, texture_pos: Vector = Vector(0, 0)):
        super().__init__(position)
        self.size = size
        self.texture_name = texture_name
        self.texture_pos = texture_pos
        self.collider = Collider(position, size)


    def get_collider(self) -> Collider:
        return self.collider


class ChangingSizePlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, max_size: Vector, min_size: Vector, speed: Vector, texture_pos: Vector = Vector(0, 0)):
        super(ChangingSizePlatform, self).__init__(position, size, texture_name, texture_pos)
        self.max_size = max_size
        self.min_size = min_size
        self.speed = speed
        self.enlarge = True

    def check_size_limit(self):
        if self.size.x >= self.max_size.x or self.size.y >= self.max_size.y:
            self.forward = True
        elif self.size.x <= self.min_size.x or self.size.y <= self.min_size.y:
            self.forward = False

    def update(self, dt):
        self.check_size_limit()
        if self.enlarge:
            self.size += self.speed * dt
            self.position += self.speed * dt / 2
        else:
            self.size -= self.speed * dt
            self.position -= self.speed * dt / 2


class DisappearingPlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, max_time: float, texture_pos: Vector = Vector(0, 0)):
        super(DisappearingPlatform, self).__init__(position, size, texture_name, texture_pos)
        self.max_time = max_time
        self.timer = 0
        self.visible = True

    def update(self, dt):
        self.timer += dt
        if self.timer < self.max_time:
            return
        self.timer = 0
        self.visible = not self.visible


class MovingPlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, start_position: Vector, end_position: Vector, speed: Vector, texture_pos: Vector = Vector(0, 0)):
        super(MovingPlatform, self).__init__(position, size, texture_name, texture_pos)
        self.start_position = start_position
        self.end_position = end_position
        self.speed = speed
        self.forward = True

    def check_boundaries(self):
        if self.position.x <= self.start_position.x or self.position.y <= self.position.y:
            self.forward = True
        elif self.position.x >= self.end_position.x or self.position.y >= self.position.y:
            self.forward = False

    def update(self, dt):
        self.check_boundaries()
        if self.forward:
            self.position += self.speed * dt
        else:
            self.position -= self.speed * dt