from src.Vector import Vector


class Physics:
    def __init__(self, gravity: Vector, jump_speed: float):
        self.gravity = gravity
        self.acceleration = Vector(0, 0)
        self.jump_force = jump_speed


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

    def __repr__(self):
        return f"Collider({self.pos}, {self.size})"