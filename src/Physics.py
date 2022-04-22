from src.Vector import Vector


class Physics:
    def __init__(self, acceleration: Vector, jump_speed: int):
        self.acceleration = acceleration
        self.jump_speed = jump_speed
