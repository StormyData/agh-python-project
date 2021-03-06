from typing import Callable

import pygame

from .Drawing.Drawers import draw_level, draw_player, draw_fps, draw_overlay
from .Drawing.GUI import draw_menu, draw_escape_panel, draw_winning_panel
from .LevelObjects.Checkpoint import WalkInArea, Checkpoint, FinalCheckpoint
from .LevelObjects.Coins import Coins
from .LevelObjects.Entities import Player, Monster
from .LevelObjects.Platforms import Platform
from .Systems.Parser import parse_file
from .Systems.SoundEngine import SoundEvent, SoundEngine
from .Controller import Controller, MonsterAI
from .Vector import Vector

pygame.init()


class Game:

    def __init__(self):
        self.monster_AI = None
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.player = Player(Vector(10, -100), Vector(40, 40), {'idle': 'player_idle', 'walk': 'player_walk'})
        self.controller = Controller(self.player)
        self.time = 0
        self.main()

    def main(self):
        f = self.main_menu
        args = tuple()
        f: Callable

        while f is not None:
            f, args = f(*args)

    def main_menu(self):
        SoundEngine.get_singleton().send_event(SoundEvent.SCREEN_ENTERED_MENU)
        run = True
        while run:
            option = draw_menu(self.window)
            if option is not None:
                level = parse_file(option)
                return self.load_level, (level,)
            pygame.display.update()

        pygame.quit()

    def load_level(self, level, reset=True):
        if reset:
            self.time = 0
            SoundEngine.get_singleton().send_event(SoundEvent.SCREEN_ENTERED_LEVEL)
            self.player.set_position(level.initial_player_pos)
            self.player.score_reset()
        else:
            SoundEngine.get_singleton().send_event(SoundEvent.SCREEN_RESUMED_LEVEL)
        clock = pygame.time.Clock()
        game_timer = pygame.time.Clock()
        self.monster_AI = MonsterAI(level.entities)
        run = True
        while run:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.time += game_timer.tick()
                    return self.escape_panel, (level,)
                elif event.type == pygame.QUIT:
                    exit(0)
            self.controller.update()
            self.monster_AI.update(self.player.position, self.window.get_width(), self.window.get_height())
            level.update(dt)
            for game_object in level.objects:
                if isinstance(game_object, Platform):
                    self.player.calc_collision(game_object.get_collider())
                    for monster in level.entities:
                        monster.calc_collision(game_object.get_collider())
                elif isinstance(game_object, Monster):
                    self.player.calc_collision_monster(game_object.get_collider())
                elif isinstance(game_object, Coins):
                    game_object.check_collision(self.player)
                elif isinstance(game_object, WalkInArea):
                    res = game_object.check_collision(self.player)
                    if isinstance(game_object, Checkpoint):
                        for monster in level.entities:
                            monster.calc_collision(game_object.get_collider())
                    elif isinstance(game_object, FinalCheckpoint) and res:
                        return self.winning_panel, (self.player.score, level, self.time + game_timer.tick())
            self.time += game_timer.tick()
            self.player.update(dt)
            offset = -self.player.position + Vector.from_tuple(self.window.get_size()) * 0.5
            self.window.fill((0, 0, 0))
            draw_level(level, self.window, offset)
            draw_player(self.player, self.window, offset)
            fps = 1.0 / dt if dt != 0 else 0.0
            draw_fps(self.window, fps)
            draw_overlay(self.window, self.player.score, self.time, self.player.physics.speed)

            pygame.display.update()

        pygame.quit()

    def escape_panel(self, curr_level):
        SoundEngine.get_singleton().send_event(SoundEvent.SCREEN_ENTERED_ESCAPE_PANEL)
        run = True
        while run:
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

    def winning_panel(self, score, curr_level, time_taken):
        SoundEngine.get_singleton().send_event(SoundEvent.SCREEN_ENTERED_ESCAPE_PANEL)
        run = True
        while run:
            option = draw_winning_panel(self.window, score, time_taken)
            if option is not None:
                if option == "retry":
                    level = parse_file(curr_level.level_name)
                    return self.load_level, (level,)
                if option == "menu":
                    return self.main_menu, tuple()

            pygame.display.update()

        return
