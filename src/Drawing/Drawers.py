import pygame
import pygame.gfxdraw
from src.LevelObject import LevelObject
from src.Platforms import Platform, DisappearingPlatform
from src.Entities import Entity, Player
from src.Vector import Vector
from src.AssetLoader import AssetLoader
from src.Level import Level


def draw_level(level: Level, surface: pygame.Surface, offset: Vector):
    background = AssetLoader.get_singleton().get_image(level.background_texture_name)
    width = surface.get_width()
    height = surface.get_height()
    pygame.gfxdraw.textured_polygon(surface, [(0, 0),
                                       (0, height),
                                       (width, height),
                                       (width, 0)], background, 0, 0)

    for game_object in level.objects:
        draw_level_object(game_object,surface, offset)


def draw_level_object(level_object: LevelObject, surface: pygame.Surface, offset: Vector):
    match level_object:
        case DisappearingPlatform() as disappearing_platform:
            if disappearing_platform.visible:
                draw_platform(disappearing_platform, surface, offset)
        case Platform() as platform:
            draw_platform(platform, surface, offset)
        case Player() as player:
            draw_player(player, surface, offset)
        case Entity() as entity:
            draw_entity(entity, surface, offset)


def draw_platform(platform: Platform, surface: pygame.Surface , offset: Vector):
    texture = AssetLoader.get_singleton().get_image(platform.texture_name)
    offset_position = platform.position + offset
    pygame.gfxdraw.textured_polygon(surface, [(offset_position.x, offset_position.y),
                                      (offset_position.x, offset_position.y + platform.size.y),
                                      (offset_position.x + platform.size.x,
                                       offset_position.y + platform.size.y),
                                      (offset_position.x + platform.size.x, offset_position.y)],
                             texture, 0, 0)


def draw_entity(entity: Entity, surface: pygame.Surface , offset: Vector):
    pass


def draw_player(player: Player, surface: pygame.Surface, offset:Vector):
    texture = AssetLoader.get_singleton().get_image(player.texture_name)
    offset_position = player.position + offset
    pygame.gfxdraw.textured_polygon(surface, [(offset_position.x, offset_position.y),
                                              (offset_position.x, offset_position.y + player.size.y),
                                              (offset_position.x + player.size.x,
                                               offset_position.y + player.size.y),
                                              (offset_position.x + player.size.x, offset_position.y)],
                                    texture, 0, 0)
