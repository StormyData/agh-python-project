import sys

import pygame
import pygame.gfxdraw
import pygame.transform

from ..Systems.AssetLoader import AssetLoader
from ..Button import Button
from ..Vector import Vector


def draw_menu(surface: pygame.Surface):
    surface.fill((0, 0, 0))
    background = AssetLoader.get_singleton().get_image("alien3")
    width = surface.get_width()
    height = surface.get_height()
    pygame.gfxdraw.textured_polygon(surface, [(0, 0),
                                              (0, height),
                                              (width, height),
                                              (width, 0)], background, 0, 0)

    menu_name = pygame.font.Font("assets/alien_font.ttf", 100).render("MAIN MENU", True, "#ACF5B3")
    menu_rect = menu_name.get_rect(center=(width / 2, 300))
    surface.blit(menu_name, menu_rect)

    button_texture = AssetLoader.get_singleton().get_image("alien1")
    level1_button = Button(button_texture, Vector(width / 2, 400),
                         "LEVEL 1", "assets/alien_font.ttf", 50, "#d7fcd4", "White")
    level2_button = Button(button_texture, Vector(width / 2, 500),
                            "LEVEL 2", "assets/alien_font.ttf", 50, "#d7fcd4", "White")
    level3_button = Button(button_texture, Vector(width / 2, 600),
                          "LEVEL 3", "assets/alien_font.ttf", 50, "#d7fcd4", "White")
    quit_button = Button(button_texture, Vector(width / 2, 700),
                         "QUIT", "assets/alien_font.ttf", 50, "#d7fcd4", "White")

    for button in [level1_button, level2_button, level3_button, quit_button]:
        button.change_color(Vector.from_tuple(pygame.mouse.get_pos()))
        button.update(surface)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if level1_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "levels/level01.xml"
            if level2_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "levels/level02.xml"
            if level3_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "levels/level03.xml"
            if quit_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                pygame.quit()
                sys.exit()


def draw_escape_panel(surface: pygame.Surface):
    surface.fill((0, 0, 0))
    background = AssetLoader.get_singleton().get_image("alien3")
    width = surface.get_width()
    height = surface.get_height()
    pygame.gfxdraw.textured_polygon(surface, [(0, 0),
                                              (0, height),
                                              (width, height),
                                              (width, 0)], background, 0, 0)

    button_texture = AssetLoader.get_singleton().get_image("alien1")
    resume_button = Button(button_texture, Vector(width / 2, 300),
                           "RESUME", "assets/alien_font.ttf", 50, "#d7fcd4", "White")
    retry_button = Button(button_texture, Vector(width / 2, 400),
                          "RETRY", "assets/alien_font.ttf", 50, "#d7fcd4", "White")
    menu_button = Button(button_texture, Vector(width / 2, 500),
                         "MAIN MENU", "assets/alien_font.ttf", 50, "#d7fcd4", "White")

    for button in [resume_button, retry_button, menu_button]:
        button.change_color(Vector.from_tuple(pygame.mouse.get_pos()))
        button.update(surface)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if resume_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "resume"
            if retry_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "retry"
            if menu_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "menu"


def draw_winning_panel(surface: pygame.Surface, score, time_taken):
    surface.fill((0, 0, 0))
    background = AssetLoader.get_singleton().get_image("alien2")
    width = surface.get_width()
    height = surface.get_height()
    pygame.gfxdraw.textured_polygon(surface, [(0, 0),
                                              (0, height),
                                              (width, height),
                                              (width, 0)], background, 0, 0)

    win_name = pygame.font.Font("assets/alien_font.ttf", 100).render("YOU WIN", True, "#ACF5B3")
    win_rect = win_name.get_rect(center=(width / 2, 300))
    surface.blit(win_name, win_rect)

    win_name = pygame.font.Font("assets/alien_font.ttf", 50).render(f"YOUR SCORE:\t\t {score}", True, "#ACF5B3")
    win_rect = win_name.get_rect(center=(width / 2, 400))
    surface.blit(win_name, win_rect)

    win_name = pygame.font.Font("assets/alien_font.ttf", 50).render(f"YOUR TIME:\t\t {float(time_taken)/1000:.2f}", True, "#ACF5B3")
    win_rect = win_name.get_rect(center=(width / 2, 600))
    surface.blit(win_name, win_rect)

    button_texture = AssetLoader.get_singleton().get_image("alien1")

    retry_button = Button(button_texture, Vector(width / 2, 800),
                          "PLAY AGAIN", "assets/alien_font.ttf", 50, "#d7fcd4", "White")
    menu_button = Button(button_texture, Vector(width / 2, 900),
                         "MAIN MENU", "assets/alien_font.ttf", 50, "#d7fcd4", "White")

    for button in [retry_button, menu_button]:
        button.change_color(Vector.from_tuple(pygame.mouse.get_pos()))
        button.update(surface)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if retry_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "retry"
            if menu_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "menu"
