from src.Platform import Platform
from src.Vector import Vector
from pygame import Surface


class DisappearingPlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name, max_time: float):
        super(DisappearingPlatform, self).__init__(position, size, texture_name)
        self.max_time = max_time
        self.timer = 0
        self.visible = True


    def update(self, dt):
        self.timer += dt
        if self.timer < self.max_time:
            return
        self.timer = 0
        self.visible = not self.visible

    def draw(self, window: Surface, offset: Vector):
        if not self.visible:
            return
        super(DisappearingPlatform, self).draw(self, window, offset)
