from src.LevelObjects.LevelObject import LevelObject
from src.Vector import Vector
from src.Physics import Physics, Collider


class Entity(LevelObject):

    def __init__(self, position: Vector, size: Vector, texture_name: str, physics: Physics):
        super().__init__(position)
        self.size = size
        self.texture_name = texture_name
        self.speed = Vector(0, 0)
        self.physics = physics
        self.collider = Collider(position, size)
        self.collision_offset = Vector(0, 0)

    def move(self, distance: Vector, dt: float):
        # self.physics.acceleration += distance
        self.speed += distance

    def jump(self):
        self.physics.acceleration.y -= self.physics.jump_force

    def update(self, dt: float):
        self.position += self.collision_offset
        self.collider.move_by(self.collision_offset)
        self.physics.acceleration += self.physics.gravity

        # self.speed += self.physics.acceleration * dt
        self.position += self.speed * dt
        self.collider.move_by(self.speed * dt)
        self.physics.acceleration = Vector(0, 0)
        self.collision_offset = Vector(0, 0)

    def calc_collision(self, collider: Collider):
        delta_coll = self.collider.collide_offset(collider)
        self.collision_offset += delta_coll
        print(delta_coll)

    def get_collider(self) -> Collider:
        return self.collider


class Monster(Entity):
    pass


class Player(Entity):
    def __init__(self, position: Vector, size: Vector, texture_name: str):
        super().__init__(position, size, texture_name, Physics(Vector(0, 10), 100))
        self.facing_left = True

    def flip(self):
        self.facing_left = not self.facing_left

    # def move(self, distance: Vector):
    #     self.position += distance
