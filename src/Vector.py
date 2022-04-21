from dataclasses import dataclass


@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        if not isinstance(other, float):
            return NotImplemented
        return Vector(self.x * other, self.y * other)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
