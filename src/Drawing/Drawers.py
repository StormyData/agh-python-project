import sys

import pygame
import pygame.gfxdraw
import pygame.transform

from src.Button import Button
from src.Level import Level
from src.LevelObjects.Checkpoint import Checkpoint
from src.LevelObjects.Entities import Monster
from src.LevelObjects.Entities import Player
from src.LevelObjects.LevelObject import LevelObject
from src.LevelObjects.Platforms import Platform, DisappearingPlatform, ChangingSizePlatform
from src.Systems.AssetLoader import AssetLoader
from src.Vector import Vector

draw_collisions = False
draw_speed = False
draw_checkpoints = True

pygame.font.init()
font = pygame.font.SysFont('Arial', 30)


def draw_fps(surface: pygame.Surface, fps: float):
    text_surface = font.render(f"fps={fps:0.2f}", False, (0, 0, 0))
    surface.blit(text_surface, (surface.get_width() - text_surface.get_width(), 0))


def draw_menu(surface: pygame.Surface):
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
    play_button = Button(button_texture, Vector(width / 2, 400),
                         "LEVEL 1", "assets/alien_font.ttf", 50, "#d7fcd4", "White")
    options_button = Button(button_texture, Vector(width / 2, 500),
                            "LEVEL 2", "assets/alien_font.ttf", 50, "#d7fcd4", "White")
    quit_button = Button(button_texture, Vector(width / 2, 600),
                         "QUIT", "assets/alien_font.ttf", 50, "#d7fcd4", "White")

    for button in [play_button, options_button, quit_button]:
        button.change_color(Vector.from_tuple(pygame.mouse.get_pos()))
        button.update(surface)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "levels/level01.xml"
            if options_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                return "levels/level_platform_test.xml"
            if quit_button.check_for_input(Vector.from_tuple(pygame.mouse.get_pos())):
                pygame.quit()
                sys.exit()


def draw_escape_panel(surface: pygame.Surface):
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


def draw_level(level: Level, surface: pygame.Surface, offset: Vector):
    background = AssetLoader.get_singleton().get_image(level.background_texture_name)
    width = surface.get_width()
    height = surface.get_height()
    pygame.gfxdraw.textured_polygon(surface, [(0, 0),
                                              (0, height),
                                              (width, height),
                                              (width, 0)], background, 0, 0)

    for game_object in level.objects:
        draw_level_object(game_object, surface, offset)


def draw_level_object(level_object: LevelObject, surface: pygame.Surface, offset: Vector):
    match level_object:
        case ChangingSizePlatform() as changing_size_platform:
            draw_changing_size_platform(changing_size_platform, surface, offset)
        case DisappearingPlatform() as disappearing_platform:
            if disappearing_platform.visible:
                draw_platform(disappearing_platform, surface, offset)
        case Platform() as platform:
            draw_platform(platform, surface, offset)
        case Player() as player:
            draw_player(player, surface, offset)
        case Monster() as monster:
            draw_monster(monster, surface, offset)
        case Checkpoint() as checkpoint:
            draw_checkpoint(checkpoint, surface, offset)


def draw_changing_size_platform(platform: ChangingSizePlatform, surface: pygame.Surface, offset: Vector):
    texture = AssetLoader.get_singleton().get_image(platform.texture_name)
    scaled_size = Vector.from_tuple(texture.get_size()) * platform.size
    scaled_texture = pygame.transform.scale(texture, scaled_size.as_tuple())
    bb = platform.get_bounding_box()
    offset_lu = bb[0] + offset
    offset_rd = bb[1] + offset
    width, height = surface.get_size()
    if offset_lu.x > width or offset_rd.x < 0 or \
            offset_lu.y > height or offset_rd.y < 0:
        return
    pygame.gfxdraw.textured_polygon(surface, [(v + offset).as_tuple() for v in platform.vertices],
                                    scaled_texture, int(offset_lu.x + platform.texture_pos.x * platform.size),
                                    int(-offset_lu.y + platform.texture_pos.y * platform.size))
    if draw_collisions:
        collider = platform.get_collider()
        pygame.draw.polygon(surface, (255, 0, 0), [(v + offset + collider.pos).as_tuple() for v in collider.vertices])


def draw_platform(platform: Platform, surface: pygame.Surface, offset: Vector):
    texture = AssetLoader.get_singleton().get_image(platform.texture_name)
    bb = platform.get_bounding_box()
    offset_lu = bb[0] + offset
    offset_rd = bb[1] + offset
    width, height = surface.get_size()
    if offset_lu.x > width or offset_rd.x < 0 or \
            offset_lu.y > height or offset_rd.y < 0:
        return
    pygame.gfxdraw.textured_polygon(surface, [(v + offset).as_tuple() for v in platform.vertices],
                                    texture, int(offset_lu.x + platform.texture_pos.x),
                                    int(-offset_lu.y + platform.texture_pos.y))
    if draw_collisions:
        collider = platform.get_collider()
        pygame.draw.polygon(surface, (255, 0, 0), [(v + offset + collider.pos).as_tuple() for v in collider.vertices])


def draw_monster(monster: Monster, surface: pygame.Surface, offset: Vector):
    texture = AssetLoader.get_singleton().get_image(monster.texture_name)
    offset_position = monster.position + offset
    width, height = surface.get_size()
    if offset_position.x > width or offset_position.x + monster.size.x < 0 or \
            offset_position.y > height or offset_position.y + monster.size.y < 0:
        return

    surface.blit(
        pygame.transform.flip(
            pygame.transform.scale(texture, monster.size.as_tuple()), monster.facing_left, False),
        offset_position.as_tuple())

    if draw_collisions:
        collider = monster.get_collider()
        pygame.draw.polygon(surface, (255, 0, 0), [(v + offset + collider.pos).as_tuple() for v in collider.vertices])


def draw_checkpoint(checkpoint: Checkpoint, surface: pygame.Surface, offset: Vector):
    if draw_checkpoints:
        pygame.draw.polygon(surface, (0, 255, 0), [(v + offset).as_tuple() for v in checkpoint.vertices])


def draw_player(player: Player, surface: pygame.Surface, offset: Vector):
    text_height = 0
    if draw_speed:
        text_surface = font.render(f"speed={player.physics.speed}", False, (0, 0, 0))
        surface.blit(text_surface, (0, text_height))
        text_height += text_surface.get_height()
    if draw_checkpoints:
        if player.last_checkpoint is not None:
            text_surface = font.render(f"last checkpoint id={player.last_checkpoint.id}", False, (0, 0, 0))
            surface.blit(text_surface, (0, text_height))
            text_height += text_surface.get_height()

    if player.curr_anim is not None:

        texture, texture_offset = player.curr_anim.get_frame()

        offset_position = player.position + offset
        width, height = surface.get_size()
        if offset_position.x > width or offset_position.x + player.size.x < 0 or \
                offset_position.y > height or offset_position.y + player.size.y < 0:
            return
        surface.blit(
            pygame.transform.flip(
                pygame.transform.scale(texture, player.size.as_tuple()), player.facing_left, False),
            (offset_position - texture_offset).as_tuple())

    if draw_collisions:
        collider = player.get_collider()
        pygame.draw.polygon(surface, (255, 0, 0), [(v + offset + collider.pos).as_tuple() for v in collider.vertices])
