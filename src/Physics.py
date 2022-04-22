from src.Vector import Vector


class Physics:

    drag_coefficient = 0.025

    def __init__(self):
        self.speed = Vector(0, 0)
        self._reset()

    def _reset(self):
        self._delta_pos = Vector(0, 0)
        self._collision_vector = Vector(0, 0)
        self.acceleration = Vector(0, 0)

    def apply_force(self, force):
        self.acceleration += force

    def move(self, delta):
        self._delta_pos += delta

    def update(self, dt):
        # drag
        self.acceleration += self.speed.normalized() * self.drag_coefficient * abs(self.speed) ** 2

        # acceleration
        self.speed -= self.acceleration * dt
        # collision
        if self._collision_vector != Vector(0, 0):
            if self._collision_vector.dot(self.speed) < 0:
                if self._collision_vector.x * self.speed.x < 0:
                    self.speed.x = 0
                if self._collision_vector.y * self.speed.y < 0:
                    self.speed.y = 0
            self._delta_pos += self._collision_vector - self._collision_vector.normalized() * 0.1

        # position
        self._delta_pos += self.speed * dt
        delta_pos = self._delta_pos
        self._reset()
        return delta_pos

    def add_collision_vector(self, delta_coll: Vector):
        self._collision_vector += delta_coll


class Collider:
    def __init__(self, pos: Vector, size: Vector):
        self.pos = pos
        self.size = size

    def collides(self, other) -> bool:
        return not (self.pos.x + self.size.x <= other.pos.x or self.pos.x >= other.pos.x + other.size.x or
                    self.pos.y + self.size.y <= other.pos.y or self.pos.y >= other.pos.y + other.size.y)

    def collide_offset(self, other) -> Vector:
        if not self.collides(other):
            return Vector(0, 0)
        min_dx = None
        min_dy = None
        if self.pos.x + self.size.x >= other.pos.x:
            min_dx = other.pos.x - self.pos.x - self.size.x
        if self.pos.x <= other.pos.x + other.size.x:
            dx = other.pos.x + other.size.x - self.pos.x
            if min_dx is None or abs(dx) < abs(min_dx):
                min_dx = dx

        if self.pos.y + self.size.y >= other.pos.y:
            min_dy = other.pos.y - self.pos.y - self.size.y
        if self.pos.y <= other.pos.y + other.size.y:
            dy = other.pos.y + other.size.y - self.pos.y
            if min_dy is None or abs(dy) < abs(min_dy):
                min_dy = dy

        if min_dx is None or min_dy is None:
            return Vector(0, 0)
        if abs(min_dx) < abs(min_dy):
            return Vector(min_dx, 0)
        else:
            return Vector(0, min_dy)

    def move_by(self, distance: Vector) -> None:
        self.pos += distance

    def resetup(self, pos: Vector, size: Vector):
        self.pos = pos
        self.size = size

    # def resetup(self, points: [Vector]):
    #     pass
    #     min_x = min(point.x for point in points)
    #     min_y = min(point.y for point in points)
    #     max_x = min(point.x for point in points)
    #     max_y = min(point.y for point in points)
    #     self.pos = Vector(min_x, min_y)
    #     self.size = Vector(max_x - min_x, max_y - min_y)

    def __repr__(self):
        return f"Collider({self.pos}, {self.size})"
