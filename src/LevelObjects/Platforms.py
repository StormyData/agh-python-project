from typing import List

from src.LevelObjects.LevelObject import LevelObject
from src.Physics import Collider
from src.Vector import Vector


class Platform(LevelObject):
    def __init__(self, vertices: List[Vector], texture_name: str, texture_pos: Vector = Vector(0, 0)):
        self.vertices = vertices
        self.texture_name = texture_name
        self.texture_pos = texture_pos
        self.collider = Collider(self.vertices)
        self._recalc_bounding_box()

        super().__init__(self.bounding_box[0])

    def get_collider(self) -> Collider:
        return self.collider

    def update(self, dt: float):
        pass

    def get_bounding_box(self) -> (Vector, Vector):
        return self.bounding_box

    def _recalc_bounding_box(self):
        min_x = min(self.vertices, key=lambda v: v.x)
        max_x = max(self.vertices, key=lambda v: v.x)
        min_y = min(self.vertices, key=lambda v: v.y)
        max_y = max(self.vertices, key=lambda v: v.y)
        self.bounding_box = (Vector(min_x.x, min_y.y), Vector(max_x.x, max_y.y))


class ChangingSizePlatform(Platform):
    def __init__(self, vertices: List[Vector], init_size: float, texture_name: str, max_size: float, min_size: float,
                 speed: float, texture_pos: Vector = Vector(0, 0)):
        super(ChangingSizePlatform, self).__init__(vertices, texture_name, texture_pos)
        self.center = sum(vertices, Vector(0, 0)) / len(vertices)
        self.base_vertices = [(v - self.center) / init_size for v in vertices]
        self.base_texture_pos = (texture_pos - self.center) / init_size
        self.size = init_size
        self.max_size = max_size
        self.min_size = min_size
        self.speed = speed
        self.shrink = False

    def check_size_limit(self):
        if self.size >= self.max_size:
            self.shrink = True
        elif self.size <= self.min_size:
            self.shrink = False

    def update(self, dt):
        self.check_size_limit()
        ds = self.speed * dt
        if self.shrink:
            ds *= -1
        self.size += ds
        self.vertices = [self.size * v + self.center for v in self.base_vertices]
        self.collider.re_setup(self.vertices)
        self._recalc_bounding_box()


class DisappearingPlatform(Platform):
    def __init__(self, vertices: List[Vector], texture_name: str, max_time: float,
                 texture_pos: Vector = Vector(0, 0)):
        super(DisappearingPlatform, self).__init__(vertices, texture_name, texture_pos)
        self.max_time = max_time
        self.timer = 0
        self.visible = True

    def update(self, dt):
        self.timer += dt
        if self.timer < self.max_time:
            return
        self.timer = 0
        self.visible = not self.visible

    def get_collider(self) -> Collider | None:
        if self.visible:
            return self.collider
        else:
            return None


class MovingPlatform(Platform):
    def __init__(self, vertices: List[Vector], texture_name: str, max_time: float,
                 speed: Vector, texture_pos: Vector = Vector(0, 0)):
        super(MovingPlatform, self).__init__(vertices, texture_name, texture_pos)
        self.speed = speed
        self.max_time = max_time
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer < self.max_time:
            self.vertices = [v + self.speed * dt for v in self.vertices]
            self.collider.move_by(self.speed * dt)
            self._recalc_bounding_box()
            return
        self.timer = 0
        self.speed = -self.speed
