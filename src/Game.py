import pygame

from src.Vector import Vector
from src.Player import Player
from src.Controller import Controller
pygame.init()


class Game:
    screen_width = 500
    screen_height = 500

    def __init__(self):
        self.player = Player(Vector(0, 0), Vector(20, 20), "wall0")
        self.controller = Controller(self.player)

    def load_level(self, level):
        window = pygame.display.set_mode((self.screen_width, self.screen_height))
        last_time = pygame.time.get_ticks()
        offset = Vector(200, 200)
        run = True
        while run:
            curr_time = pygame.time.get_ticks()
            dt = (curr_time - last_time)/1000
            last_time = curr_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.controller.update(dt)
            window.fill((0, 0, 0))
            level.draw(window, offset)
            self.player.draw(window, offset)
            pygame.display.update()

        pygame.quit()
