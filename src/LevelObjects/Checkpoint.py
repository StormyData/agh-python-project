from typing import List

from src.LevelObjects.LevelObject import LevelObject
from src.Vector import Vector
from src.Physics import Collider


class Checkpoint(LevelObject):
    def __init__(self, vertices: List[Vector], checkpoint_id: str, tele_to: Vector):
        self.vertices = vertices
        self._recalc_bounding_box()
        super().__init__(self.bounding_box[0])
        self.id = checkpoint_id
        self.collider = Collider(self.vertices)
        self.tele_to = tele_to

    def check_collision(self, player):
        if self.collider.collides(player.get_collider()):
            player.set_last_checkpoint(self)

    def get_tele_to_pos(self):
        return self.tele_to

    def __str__(self):
        return f"Checkpoint({self.vertices}, {self.id}, {self.tele_to})"

    def get_bounding_box(self) -> (Vector, Vector):
        return self.bounding_box

    def _recalc_bounding_box(self):
        min_x = min(self.vertices, key=lambda v: v.x)
        max_x = max(self.vertices, key=lambda v: v.x)
        min_y = min(self.vertices, key=lambda v: v.y)
        max_y = max(self.vertices, key=lambda v: v.y)
        self.bounding_box = (Vector(min_x.x, min_y.y), Vector(max_x.x, max_y.y))
