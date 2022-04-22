from src.Platform import Platform
from src.Vector import Vector


class MovingPlatform(Platform):
    def __init__(self, position: Vector, size: Vector, texture_name: str, start_position: Vector, end_position: Vector, speed: Vector):
        super(MovingPlatform, self).__init__(position, size, texture_name)
        self.start_position = start_position
        self.end_position = end_position
        self.speed = speed
        self.forward = True

    def check_boundaries(self):
        if self.position.x <= self.start_position.x or self.position.y <= self.position.y:
            self.forward = True
        elif self.position.x >= self.end_position.x or self.position.y >= self.position.y:
            self.forward = False

    def update(self, dt):
        self.check_boundaries()
        if self.forward:
            self.position += self.speed * dt
        else:
            self.position -= self.speed * dt

