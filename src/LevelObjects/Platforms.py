from src.LevelObjects.LevelObject import LevelObject
from src.Physics import Collider
from src.Vector import Vector


class Platform(LevelObject):
    def __init__(self, position: Vector, size: Vector, texture_name: str, texture_pos: Vector = Vector(0, 0)):
        super().__init__(position)
        self.size = size
        self.texture_name = texture_name
        self.texture_pos = texture_pos
        self.collider = Collider(position, size)

    def get_collider(self) -> Collider:
        return self.collider

    def update(self, dt: float):
        pass


class ChangingSizePlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, max_size: Vector, min_size: Vector,
                 speed: float, texture_pos: Vector = Vector(0, 0)):
        super(ChangingSizePlatform, self).__init__(position, size, texture_name, texture_pos)
        if min_size.x > max_size.x:
            min_size, max_size = max_size, min_size
        self.max_size = max_size
        self.min_size = min_size
        self.speed_vector = (self.max_size - self.min_size).normalized() * speed * 15
        self.enlarge = True

    def check_size_limit(self):
        if self.min_size.y < self.max_size.y:
            if self.size.x < self.min_size.x or self.size.y < self.min_size.y:
                self.enlarge = True
            elif self.max_size.x < self.size.x or self.max_size.y < self.size.y:
                self.enlarge = False
        else:
            if self.size.x < self.min_size.x or self.size.y > self.min_size.y:
                self.enlarge = True
            elif self.max_size.x < self.size.x or self.max_size.y > self.size.y:
                self.enlarge = False


    def update(self, dt):
        self.check_size_limit()
        if self.enlarge:
            self.size += self.speed_vector * dt
            self.position -= self.speed_vector * dt / 2
        else:
            self.size -= self.speed_vector * dt
            self.position += self.speed_vector * dt / 2
        self.collider.resetup(self.position, self.size)


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


class MovingPlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, start_position: Vector, end_position: Vector,
                 speed: float, texture_pos: Vector = Vector(0, 0)):
        super(MovingPlatform, self).__init__(position, size, texture_name, texture_pos)
        if start_position.x > end_position.x:
            start_position, end_position = end_position, start_position
        self.start_position = start_position
        self.end_position = end_position
        self.speed_vector = (self.end_position - self.start_position).normalized() * speed * 15
        self.forward = True

    def check_boundaries(self):
        if self.start_position.y < self.end_position.y:
            if self.position.x < self.start_position.x or self.position.y < self.start_position.y:
                self.forward = True
            elif self.end_position.x < self.position.x or self.end_position.y < self.position.y:
                self.forward = False
        else:
            if self.position.x < self.start_position.x or self.position.y > self.start_position.y:
                self.forward = True
            elif self.end_position.x < self.position.x or self.end_position.y > self.position.y:
                self.forward = False


    def update(self, dt):
        self.check_boundaries()
        if self.forward:
            self.position += self.speed_vector * dt
            self.collider.move_by(self.speed_vector * dt)
        else:
            self.position -= self.speed_vector * dt
            self.collider.move_by(-self.speed_vector * dt)
