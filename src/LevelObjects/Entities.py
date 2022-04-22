from src.LevelObjects.LevelObject import LevelObject
from src.Physics import Physics, Collider
from src.Vector import Vector


class Entity(LevelObject):

    jump_force = Vector(0, 20000)
    gravity = Vector(0, -500)

    def __init__(self, position: Vector, size: Vector, texture_name: str):
        super().__init__(position)
        self.size = size
        self.texture_name = texture_name
        self.physics = Physics()
        self.collider = Collider(position, size)
        self.on_ground = False
        self.last_on_ground = False

    def move(self, distance: Vector):
        self.physics.apply_force(distance)

    def jump(self):
        if self.last_on_ground:
            self.physics.apply_force(self.jump_force)

    def update(self, dt: float):
        self.physics.apply_force(self.gravity)
        # acc = self.physics.acceleration
        delta_pos = self.physics.update(dt)
        # print(f"{acc}, {self.physics.speed}")
        self.position += delta_pos
        self.collider.move_by(delta_pos)

        self.last_on_ground = self.on_ground
        self.on_ground = False

    def calc_collision(self, collider: Collider):
        delta_coll = self.collider.collide_offset(collider)
        if delta_coll.y < 0:
            self.on_ground = True
        self.physics.add_collision_vector(delta_coll)
        # print(delta_coll)

    def get_collider(self) -> Collider:
        return self.collider


class Monster(Entity):
    pass


class Player(Entity):
    def __init__(self, position: Vector, size: Vector, texture_name: str):
        super().__init__(position, size, texture_name)
        self.facing_left = True

    def flip(self):
        self.facing_left = not self.facing_left

    # def move(self, distance: Vector):
    #     self.position += distance
