import pygame

from .LevelObjects.Entities import Player, Monster
from .Systems.SoundEngine import SoundEvent, SoundEngine
from .Vector import Vector


class Controller:
    player_speed = 512  # px/s/s

    def __init__(self, player: Player):
        self.player = player

    def update(self):
        if not pygame.key.get_focused():
            return
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.player.jump()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            if not self.player.facing_left:
                self.player.flip()
            self.player.move(Vector(self.player_speed, 0))
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            if self.player.facing_left:
                self.player.flip()
            self.player.move(Vector(-self.player_speed, 0))
        if pressed[pygame.K_HOME]:
            SoundEngine.get_singleton().send_event(SoundEvent.PLAYER_GONE_HOME)
            self.player.teleport_to_last_checkpoint()


class MonsterAI:
    def __init__(self, monsters: [Monster]):
        self.monsters = monsters

    def update(self, player_position: Vector, screen_width: int, screen_height: int):
        for monster in self.monsters:
            offset = monster.position - player_position + Vector(screen_width, screen_height) * 0.5
            if offset.x > screen_width or offset.x + monster.size.x < 0 or \
                    offset.y > screen_height or offset.y + monster.size.y < 0:
                continue

            if player_position.x < monster.position.x:
                if not monster.facing_left:
                    monster.flip()
                monster.move(Vector(monster.speed, 0))
            elif player_position.x > monster.position.x:
                if monster.facing_left:
                    monster.flip()
                monster.move(Vector(-monster.speed, 0))
