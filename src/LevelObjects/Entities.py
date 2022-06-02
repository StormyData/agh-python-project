from src.Drawing.Animation import Animation
from src.LevelObjects.LevelObject import LevelObject
from src.Physics import Physics, Collider
from src.Systems.AssetLoader import AssetLoader
from src.Vector import Vector, get_sized_box
from src.LevelObjects.Checkpoint import Checkpoint
from src.Systems.SoundEngine import SoundEvent, SoundEngine


class Entity(LevelObject):
    jump_force = Vector(0, 20000)
    gravity = Vector(0, -500)

    def __init__(self, position: Vector, size: Vector, texture_name: str):
        super().__init__(position)
        self.size = size
        self.texture_name = texture_name
        self.physics = Physics()
        self.collider = Collider([position + v for v in get_sized_box(size)])
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

    def get_collider(self) -> Collider:
        return self.collider

    def get_bounding_box(self) -> (Vector, Vector):
        return self.position, self.position + self.size

    def set_position(self, new_pos: Vector):
        dp = new_pos - self.position
        self.position += dp
        self.collider.move_by(dp)
        self.physics.reset()


class Monster(Entity):
    def __init__(self, position: Vector, size: Vector, texture_name: str, speed: float):
        super().__init__(position, size, texture_name)
        self.speed = speed * 15
        self.facing_left = True

    def flip(self):
        self.facing_left = not self.facing_left


class Player(Entity):
    def __init__(self, position: Vector, size: Vector, animations: dict[str, str]):
        super().__init__(position, size, "")
        self.facing_left = True
        self.last_checkpoint: Checkpoint | None = None
        self.animations = dict()
        for anim in animations:
            self.animations[anim] = Animation(AssetLoader.get_singleton().get_animation_buffer(animations[anim]))
        self.curr_anim = self.animations['idle']
        self.curr_anim: Animation | None
        self.last_last_on_ground = False
        self.score = 0

    def flip(self):
        self.facing_left = not self.facing_left

    def update(self, dt: float):
        self.last_last_on_ground = self.last_on_ground
        super().update(dt)
        if self.last_on_ground != self.last_last_on_ground:
            if self.last_on_ground:
                SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_ON_GROUND)
            else:
                SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_OFF_GROUND)
        if abs(self.physics.speed.x) > 0.1:
            if self.curr_anim != self.animations['walk']:
                self.curr_anim = self.animations['walk']
                SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_STARTED_MOVING)
                self.curr_anim.reset()
        else:
            if self.curr_anim != self.animations['idle']:
                SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_STOPPED_MOVING)
                self.curr_anim = self.animations['idle']
                self.curr_anim.reset()
        self.curr_anim.update(dt)

    def set_last_checkpoint(self, checkpoint):
        if self.last_checkpoint != checkpoint:
            self.last_checkpoint = checkpoint
            SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_CHECKPOINT_SET)

    def teleport_to_last_checkpoint(self):
        if self.last_checkpoint is None:
            return
        self.set_position(self.last_checkpoint.get_tele_to_pos())

    def calc_collision_monster(self, collider: Collider):
        if self.collider.collides(collider):
            SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_DIED)
            self.teleport_to_last_checkpoint()

    def jump(self):
        super().jump()
        if self.last_on_ground:
            SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_JUMPED)

    def score_reset(self):
        self.score = 0
