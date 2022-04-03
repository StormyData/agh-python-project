from Vector import Vector


class LevelObject:
    def __init__(self, position: Vector):
        self.position = position

    def save(self) -> dict:
        pass

    def load(self, data: dict):
        pass
