import pygame
from src.Player import Player
from src.Vector import Vector


class Controller:
    player_speed = 64 # px/s
    def __init__(self, player: Player):
        self.player = player

    def update(self, dt: float):
        if not pygame.key.get_focused():
            return
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move(Vector(0, -self.player_speed * dt))
        if pressed[pygame.K_DOWN]:
            self.player.move(Vector(0, self.player_speed * dt))
        if pressed[pygame.K_LEFT]:
            if not self.player.facing_left:
                self.player.flip()
            self.player.move(Vector(-self.player_speed * dt, 0))
        if pressed[pygame.K_RIGHT]:
            if self.player.facing_left:
                self.player.flip()
            self.player.move(Vector(self.player_speed * dt, 0))