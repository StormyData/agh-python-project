import pygame

from src.Vector import Vector

pygame.init()


class Game:
    screen_width = 500
    screen_height = 500

    def load_level(self, level):
        window = pygame.display.set_mode((self.screen_width, self.screen_height))

        offset = Vector(100, 100)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            window.fill((0, 0, 0))
            level.draw(window, offset)
            pygame.display.update()

        pygame.quit()
