from src.LevelObjects.LevelObject import LevelObject
from src.Physics import Collider
from src.Vector import Vector, get_sized_box


class Platform(LevelObject):
    def __init__(self, position: Vector, size: Vector, texture_name: str, texture_pos: Vector = Vector(0, 0)):
        super().__init__(position)
        self.vertices = [v + position for v in get_sized_box(size)]
        self.texture_name = texture_name
        self.texture_pos = texture_pos
        self.collider = Collider(self.vertices)
        self.bounding_box = (position, position + size)

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
        self.bounding_box = (Vector(min_x, min_y), Vector(max_x, max_y))


class ChangingSizePlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, max_size: Vector, min_size: Vector,
                 speed: Vector, texture_pos: Vector = Vector(0, 0)):
        super(ChangingSizePlatform, self).__init__(position, size, texture_name, texture_pos)
        self.size = size
        self.max_size = max_size
        self.min_size = min_size
        self.speed = speed
        self.enlarge = True
        self.forward = False

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
        self.collider.resetup([self.position + v for v in get_sized_box(self.size)])
        self._recalc_bounding_box()


class DisappearingPlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, max_time: float,
                 texture_pos: Vector = Vector(0, 0)):
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

    def get_collider(self) -> Collider | None:
        if self.visible:
            return self.collider
        else:
            return None

#   <moving_platform position="-3,-3" size="2,2" texture="grass0" start_position="-5,-5" end_position="0,0" speed="-2,-2"/>


class MovingPlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, start_position: Vector, end_position: Vector,
                 speed: Vector, texture_pos: Vector = Vector(0, 0)):
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
        #print(self.position)
        self.check_boundaries()
        if self.forward:
            self.position += self.speed * dt
            self.collider.move_by(self.speed * dt)
        else:
            self.position -= self.speed * dt
            self.collider.move_by(-self.speed * dt)
        self._recalc_bounding_box()
