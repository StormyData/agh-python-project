import pygame

from src.LevelObjects.Entities import Player
from src.Vector import Vector


class Controller:
    player_speed = 64  # px/s

    def __init__(self, player: Player):
        self.player = player

    def update(self, dt: float):
        if not pygame.key.get_focused():
            return
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            # self.player.jump()
            self.player.move(Vector(0, -self.player_speed * dt), dt)
            # self.player.move(Vector(0, -self.player_speed * dt))
        if pressed[pygame.K_DOWN]:
            pass
            self.player.move(Vector(0, self.player_speed * dt), dt)
        if pressed[pygame.K_LEFT]:
            if not self.player.facing_left:
                self.player.flip()
            self.player.move(Vector(-self.player_speed * dt, 0), dt)
        if pressed[pygame.K_RIGHT]:
            if self.player.facing_left:
                self.player.flip()
            self.player.move(Vector(self.player_speed * dt, 0), dt)
        # self.player.update(dt)
