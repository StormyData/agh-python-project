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

    @staticmethod
    def from_tuple(tuple):
        return Vector(tuple[0], tuple[1])
