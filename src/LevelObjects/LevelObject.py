from ..Vector import Vector


class LevelObject:
    def __init__(self, position: Vector):
        self.position = position

    def get_bounding_box(self) -> (Vector, Vector):
        return NotImplemented
