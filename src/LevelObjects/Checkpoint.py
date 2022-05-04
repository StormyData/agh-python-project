from src.LevelObjects.Entities import Player
from src.LevelObjects.LevelObject import LevelObject
from src.Vector import Vector
from src.Physics import Collider


class Checkpoint(LevelObject):
    def __init__(self, position: Vector, size: Vector):
        super().__init__(position)
        self.size = size
        self.collider = Collider(position, size)

    def check_collision(self, player: Player):
        if self.collider.collides(player.get_collider()):
            player.set_last_checkpoint(self)

    def get_tele_to_pos(self):
        return self.position + self.size / 2

    def __str__(self):
        return f"Checkpoint({self.position}, {self.size})"
