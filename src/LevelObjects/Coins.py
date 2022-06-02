from src.LevelObjects.LevelObject import LevelObject
from src.Vector import Vector, get_sized_box
from src.Physics import Collider
from src.Systems.SoundEngine import SoundEvent, SoundEngine


class Coins(LevelObject):
    def __init__(self, position: Vector, texture_name: str, size: Vector):
        super().__init__(position)
        self.size = size
        self.collider = Collider([position + v for v in get_sized_box(self.size)])
        self.texture_name = texture_name
        self.collected = False

    def check_collision(self, player):
        if self.collider.collides(player.get_collider()):
            player.score += 1
            if not self.collected:
                SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_PICKED_UP_COIN)
            self.collected = True

    def get_collider(self):
        return self.collider
