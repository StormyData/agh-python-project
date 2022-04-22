from src.Platform import Platform
from src.Vector import Vector


class ChangingSizePlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, max_size: Vector, min_size: Vector, speed: Vector):
        super(ChangingSizePlatform, self).__init__(position, size, texture_name)
        self.max_size = max_size
        self.min_size = min_size
        self.speed = speed
        self.enlarge = True

    def check_size_limit(self):
        if self.size.x >= self.max_size.x or self.size.y >= self.max_size.y:
            self.forward = True
        elif self.size.x <= self.min_size.x or self.size.y <= self.min_size.y:
            self.forward = False

    def update(self, dt):
        self.check_size_limit()
        if self.enlarge:
            self.size += self.speed * dt
            self.position += self.speed * dt / 2
        else:
            self.size -= self.speed * dt
            self.position -= self.speed * dt / 2
