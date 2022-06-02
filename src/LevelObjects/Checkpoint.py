from .LevelObject import LevelObject
from ..Physics import Collider
from ..Vector import Vector


class WalkInArea(LevelObject):
    def __init__(self, vertices: list[Vector]):
        self.vertices = vertices
        self._recalc_bounding_box()
        super().__init__(self.bounding_box[0])
        self.collider = Collider(self.vertices)

    def check_collision(self, player) -> bool:
        if self.collider.collides(player.get_collider()):
            self._on_enter(player)
            return True
        return False

    def get_collider(self):
        return self.collider

    def __str__(self):
        return f"WalkInArea({self.vertices})"

    def get_bounding_box(self) -> (Vector, Vector):
        return self.bounding_box

    def _recalc_bounding_box(self):
        min_x = min(self.vertices, key=lambda v: v.x)
        max_x = max(self.vertices, key=lambda v: v.x)
        min_y = min(self.vertices, key=lambda v: v.y)
        max_y = max(self.vertices, key=lambda v: v.y)
        self.bounding_box = (Vector(min_x.x, min_y.y), Vector(max_x.x, max_y.y))

    def _on_enter(self, player):
        pass


class Checkpoint(WalkInArea):
    def __init__(self, vertices: list[Vector], checkpoint_id: str, tele_to: Vector):
        super().__init__(vertices)
        self.id = checkpoint_id
        self.tele_to = tele_to

    def _on_enter(self, player):
        player.set_last_checkpoint(self)

    def get_tele_to_pos(self):
        return self.tele_to

    def __str__(self):
        return f"Checkpoint({self.vertices}, {self.id}, {self.tele_to})"


class KillingArea(WalkInArea):
    def __init__(self, vertices: list[Vector]):
        super().__init__(vertices)

    def _on_enter(self, player):
        player.kill()

    def __str__(self):
        return f"KillingArea({self.vertices})"


class FinalCheckpoint(WalkInArea):
    def __init__(self, vertices: list[Vector]):
        super().__init__(vertices)

    def _on_enter(self, player):
        print("yey")

    def __str__(self):
        return f"FinalCheckpoint({self.vertices})"
