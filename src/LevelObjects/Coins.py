from .LevelObject import LevelObject
from ..Systems.SoundEngine import SoundEvent, SoundEngine
from ..Physics import Collider
from ..Vector import Vector, get_sized_box


class Coins(LevelObject):
    def __init__(self, position: Vector, texture_name: str, size: Vector):
        super().__init__(position)
        self.size = size
        self.collider = Collider([position + v for v in get_sized_box(self.size)])
        self.texture_name = texture_name
        self.collected = False

    def check_collision(self, player):
        if self.collider.collides(player.get_collider()):
            if not self.collected:
                player.score += 1
                SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_PICKED_UP_COIN)
                self.collected = True

    def get_collider(self):
        return self.collider
