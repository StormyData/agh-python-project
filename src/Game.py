import pygame

from src.Systems.Parser import parse_file
from src.Controller import Controller, MonsterAI
from src.Drawing.Drawers import draw_menu, draw_level, draw_escape_panel, draw_player
from src.LevelObjects.Entities import Player, Monster
from src.LevelObjects.Platforms import Platform
from src.Vector import Vector
from src.LevelObjects.Checkpoint import Checkpoint
pygame.init()


class Game:
    screen_width = 1600
    screen_height = 900

    def __init__(self):
        self.player = Player(Vector(10, -100), Vector(40, 40), {'idle': 'player_idle', 'walk': 'player_walk'})
        self.controller = Controller(self.player)
        self.main_menu()

    def main_menu(self):
        window = pygame.display.set_mode((self.screen_width, self.screen_height))
        run = True
        while run:
            window.fill((0, 0, 0))

            option = draw_menu(window)
            if option is not None:
                level = parse_file(option)
                return self.load_level(level)
            pygame.display.update()

        pygame.quit()

    def load_level(self, level):
        window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.player.set_position(level.initial_player_pos)
        last_time = pygame.time.get_ticks()
        self.monster_AI = MonsterAI(level.entities)
        run = True
        while run:
            curr_time = pygame.time.get_ticks()
            dt = (curr_time - last_time) / 1000
            last_time = curr_time
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.escape_panel(level)
            self.controller.update(dt)
            self.monster_AI.update(self.player.position, Game.screen_width, Game.screen_height, dt)
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
            offset = -self.player.position + Vector(Game.screen_width, Game.screen_height) * 0.5
            window.fill((0, 0, 0))
            draw_level(level, window, offset)
            draw_player(self.player, window, offset)
            pygame.display.update()

        pygame.quit()

    def escape_panel(self, curr_level):
        window = pygame.display.set_mode((self.screen_width, self.screen_height))
        run = True
        while run:
            window.fill((0, 0, 0))

            option = draw_escape_panel(window)
            if option is not None:
                if option == "resume":
                    return self.load_level(curr_level)
                if option == "retry":
                    level = parse_file(curr_level.level_name)
                    return self.load_level(level)
                if option == "menu":
                    return self.main_menu()


            pygame.display.update()

        return
