from dataclasses import dataclass


@dataclass
class Vector:
    x: float
    y: float
    eps = 0.001

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        if not (isinstance(other, float) or isinstance(other, int)):
            return NotImplemented
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        if not (isinstance(other, float) or isinstance(other, int)):
            return NotImplemented
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        if not (isinstance(other, float) or isinstance(other, int)):
            return NotImplemented
        return Vector(self.x / other, self.y / other)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def dot(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.y - self.y * other.x

    def normalized(self):
        len = self.__abs__()
        if len < self.eps:
            return Vector(0, 0)
        return self / len

    def as_tuple(self):
        return self.x, self.y

    def rotate_90_deg_clockwise(self):
        return Vector(self.y, -self.x)

    def rotate_90_deg_anticlockwise(self):
        return Vector(-self.y, self.x)

    @staticmethod
    def from_tuple(tuple):
        return Vector(tuple[0], tuple[1])

     def is_between(self, other1, other2):
        if not isinstance(other1, Vector) and not isinstance(other2, Vector):
            return NotImplemented
        if other1.x > other2.x:
            other1, other2 = other2, other1
        if other1.y <= other2.y:
            return other1.x <= self.x <= other2.x and other1.y <= self.y <= other2.y
        else:
            return other1.x <= self.x <= other2.x and other1.y >= self.y >= other2.y


def get_sized_box(size: Vector):
    return [Vector(0, 0), Vector(0, size.y), Vector(size.x, size.y), Vector(size.x, 0)]