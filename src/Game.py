import pygame

from src.Controller import Controller
from src.Drawing.Drawers import draw_level, draw_player
from src.LevelObjects.Entities import Player
from src.LevelObjects.Platforms import Platform
from src.Vector import Vector

pygame.init()


class Game:
    screen_width = 1600
    screen_height = 900

    def __init__(self):
        self.player = Player(Vector(0, 0), Vector(20, 20), "wall0")
        self.controller = Controller(self.player)

    def load_level(self, level):
        window = pygame.display.set_mode((self.screen_width, self.screen_height))
        last_time = pygame.time.get_ticks()
        run = True
        while run:
            curr_time = pygame.time.get_ticks()
            dt = (curr_time - last_time) / 1000
            last_time = curr_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.controller.update(dt)
            # level.update(dt)
            for game_object in level.objects:
                if not isinstance(game_object, Platform):
                    continue
                self.player.calc_collision(game_object.get_collider())
            self.player.update(dt)
            offset = -self.player.position + Vector(Game.screen_width, Game.screen_height) * 0.5
            window.fill((0, 0, 0))
            draw_level(level, window, offset)
            draw_player(self.player, window, offset)
            pygame.display.update()

        pygame.quit()
