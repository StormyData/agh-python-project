import pygame

from src.LevelObjects.Entities import Player, Monster
from src.Vector import Vector


class Controller:
    player_speed = 512  # px/s/s

    def __init__(self, player: Player):
        self.player = player

    def update(self, dt: float):
        if not pygame.key.get_focused():
            return
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.jump()
            # self.player.move(Vector(0, self.player_speed))
            # self.player.move(Vector(0, -self.player_speed * dt))
        # if pressed[pygame.K_DOWN]:
        #     pass
        #     self.player.move(Vector(0, -self.player_speed))
        if pressed[pygame.K_LEFT]:
            if not self.player.facing_left:
                self.player.flip()
            self.player.move(Vector(self.player_speed, 0))
        if pressed[pygame.K_RIGHT]:
            if self.player.facing_left:
                self.player.flip()
            self.player.move(Vector(-self.player_speed, 0))
        if pressed[pygame.K_HOME]:
            self.player.teleport_to_last_checkpoint()
        # self.player.update(dt)


class MonsterAI:
    # monster_speed = 512  # px/s/s

    def __init__(self, monsters: [Monster]):
        self.monsters = monsters

    def update(self, player_position: Vector, screen_width: int, screen_height: int, dt: float):
        for monster in self.monsters:
            offset = -monster.position + Vector(screen_width, screen_height) * 0.5
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
