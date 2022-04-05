from src.Vector import Vector


class Collider:
    def collides(self, other) -> bool:
        pass

    def collide_offset(self, other) -> Vector:
        pass

    def move_by(self, distance: Vector) -> None:
        pass
