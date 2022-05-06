import pygame

from src.Systems.Parser import parse_file
from src.Controller import Controller, MonsterAI
from src.Drawing.Drawers import draw_menu, draw_level, draw_escape_panel, draw_player, draw_fps
from src.LevelObjects.Entities import Player, Monster
from src.LevelObjects.Platforms import Platform
from src.Vector import Vector
from src.LevelObjects.Checkpoint import Checkpoint
pygame.init()


class Game:

    def __init__(self):
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.player = Player(Vector(10, -100), Vector(40, 40), {'idle': 'player_idle', 'walk': 'player_walk'})
        self.controller = Controller(self.player)
        self.main()

    def main(self):
        f = self.main_menu
        args = tuple()
        while f is not None:
            f, args = f(*args)

    def main_menu(self):
        run = True
        while run:
            self.window.fill((0, 0, 0))

            option = draw_menu(self.window)
            if option is not None:
                level = parse_file(option)
                return self.load_level, (level,)
            pygame.display.update()

        pygame.quit()

    def load_level(self, level, reset=True):
        if reset:
            self.player.set_position(level.initial_player_pos)
        clock = pygame.time.Clock()
        self.monster_AI = MonsterAI(level.entities)
        run = True
        while run:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return self.escape_panel ,(level, )
                elif event.type == pygame.QUIT:
                    exit(0)
            self.controller.update(dt)
            self.monster_AI.update(self.player.position, self.window.get_width(), self.window.get_height(), dt)
            level.update(dt)
            for game_object in level.objects:
                if isinstance(game_object, Platform):
                    self.player.calc_collision(game_object.get_collider())
                    for monster in level.entities:
                        monster.calc_collision(game_object.get_collider())
                elif isinstance(game_object, Monster):
                    self.player.calc_collision_monster(game_object.get_collider())
                elif isinstance(game_object, Checkpoint):
                    game_object.check_collision(self.player)

            self.player.update(dt)
            offset = -self.player.position + Vector.from_tuple(self.window.get_size()) * 0.5
            self.window.fill((0, 0, 0))
            draw_level(level, self.window, offset)
            draw_player(self.player, self.window, offset)
            fps = 1.0 / dt if dt != 0 else 0.0
            draw_fps(self.window, fps)

            pygame.display.update()

        pygame.quit()

    def escape_panel(self, curr_level):
        run = True
        while run:
            self.window.fill((0, 0, 0))

            option = draw_escape_panel(self.window)
            if option is not None:
                if option == "resume":
                    return self.load_level, (curr_level, False)
                if option == "retry":
                    level = parse_file(curr_level.level_name)
                    return self.load_level, (level,)
                if option == "menu":
                    return self.main_menu, tuple()


            pygame.display.update()

        return
