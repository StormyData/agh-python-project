from dataclasses import dataclass


@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Vector can only be added to other vector")
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float):
        if not isinstance(other, float):
            raise TypeError("Vector can only be multiplied by a float")
        return Vector(self.x * other, self.y * other)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
