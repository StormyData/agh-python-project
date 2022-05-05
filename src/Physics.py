from typing import List

from src.Vector import Vector


class Physics:
    drag_coefficient = 0.025

    def __init__(self):
        self.speed = Vector(0, 0)
        self._reset()

    def reset(self):
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
    def __init__(self, vertices: List[Vector]):
        self.pos = Vector(0, 0)
        self.vertices = vertices.copy()
        self.min_max_arr = None
        self.min_max_arr_dirty = True

    def collides(self, other) -> bool:
        if other is None:
            return False
        other: Collider
        self._update_pos()
        other._update_pos()
        return self._sat(other, False).collides and other._sat(self, True).collides

    def collide_offset(self, other) -> Vector:
        if other is None:
            return Vector(0, 0)
        other: Collider
        self._update_pos()
        other._update_pos()
        res2 = other._sat(self, True)
        res1 = self._sat(other, False)
        if (not res1.collides) or (not res2.collides):
            return Vector(0, 0)
        if abs(res1.distance) < abs(res2.distance):
            return res1.vector * -res1.distance
        else:
            return res2.vector * -res2.distance

    def move_by(self, distance: Vector) -> None:
        self.pos += distance

    def resetup(self, verices: List[Vector]):
        self.pos = Vector(0, 0)
        self.vertices = verices.copy()
        self.min_max_arr_dirty = True

    def _update_pos(self):
        if self.pos != Vector(0, 0):
            for i in range(len(self.vertices)):
                self.vertices[i] += self.pos
            self.pos = Vector(0, 0)
            self.min_max_arr_dirty = True

    def _calc_min_max_arr(self):
        self.min_max_arr_dirty = False
        self.min_max_arr = [None] * len(self.vertices)
        for i in range(len(self.vertices)):
            axis = (self.vertices[i - 1] - self.vertices[i]).rotate_90_deg_clockwise().normalized()
            min1 = min(axis.dot(vertex) for vertex in self.vertices)
            max1 = max(axis.dot(vertex) for vertex in self.vertices)
            self.min_max_arr[i] = (min1, max1)

    def _sat(self, other, flip: bool):
        other: Collider
        if self.min_max_arr_dirty:
            self._calc_min_max_arr()
        result = CollisionResult()
        shortest_dist = float('inf')
        for i in range(len(self.vertices)):
            axis = (self.vertices[i - 1] - self.vertices[i]).rotate_90_deg_clockwise().normalized()
            min1 = min(axis.dot(vertex) for vertex in other.vertices)
            max1 = max(axis.dot(vertex) for vertex in other.vertices)
            if self.min_max_arr[i][0] > max1 or min1 > self.min_max_arr[i][1]:
                result.collides = False
                return result
            dist = self.min_max_arr[i][0] - max1
            if flip:
                dist *= -1
            if abs(dist) < shortest_dist:
                shortest_dist = abs(dist)
                result.distance = dist
                result.vector = axis
        result.collides = True
        return result

    def __repr__(self):
        self._update_pos()
        return f"Collider({self.vertices})"


class CollisionResult:
    def __init__(self):
        self.collides = False
        self.vector = Vector(0, 0)
        self.distance = 0
