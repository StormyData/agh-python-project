import pygame
import pygame.gfxdraw

from src.Level import Level
from src.LevelObjects.Entities import Entity, Player
from src.LevelObjects.LevelObject import LevelObject
from src.LevelObjects.Platforms import Platform, DisappearingPlatform
from src.Systems.AssetLoader import AssetLoader
from src.Vector import Vector
from src.LevelObjects.Checkpoint import Checkpoint

draw_collisions = False
draw_speed = True
draw_checkpoints = True

pygame.font.init()
font = pygame.font.SysFont('Arial', 30)


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
        case DisappearingPlatform() as disappearing_platform:
            if disappearing_platform.visible:
                draw_platform(disappearing_platform, surface, offset)
        case Platform() as platform:
            draw_platform(platform, surface, offset)
        case Player() as player:
            draw_player(player, surface, offset)
        case Entity() as entity:
            draw_entity(entity, surface, offset)
        case Checkpoint() as chheckpoint:
            draw_checkpoint(chheckpoint, surface, offset)


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


def draw_checkpoint(checkpoint: Checkpoint, surface: pygame.Surface, offset: Vector):
    if draw_checkpoints:
        pygame.draw.polygon(surface, (0, 255, 0), [(v + offset).as_tuple() for v in checkpoint.vertices])

def draw_entity(entity: Entity, surface: pygame.Surface, offset: Vector):
    pass


def draw_player(player: Player, surface: pygame.Surface, offset: Vector):
    text_height = 0
    if draw_speed:
        textsurface = font.render(f"speed={player.physics.speed}", False, (0, 0, 0))
        surface.blit(textsurface,(0, text_height))
        text_height += textsurface.get_height()
    if draw_checkpoints:
        if player.last_checkpoint is not None:
            textsurface = font.render(f"last checkpoint id={player.last_checkpoint.id}", False, (0, 0, 0))
            surface.blit(textsurface, (0, text_height))
            text_height += textsurface.get_height()

    texture = AssetLoader.get_singleton().get_image(player.texture_name)
    offset_position = player.position + offset
    width, height = surface.get_size()
    if offset_position.x > width or offset_position.x + player.size.x < 0 or \
            offset_position.y > height or offset_position.y + player.size.y < 0:
        return
    pygame.draw.rect(surface, (0, 0, 255),
                     (player.position.x + offset.x, player.position.y + offset.y, player.size.x, player.size.y))

        # pygame.gfxdraw.textured_polygon(surface, [(offset_position.x, offset_position.y),
    #                                           (offset_position.x, offset_position.y + player.size.y),
    #                                           (offset_position.x + player.size.x,
    #                                            offset_position.y + player.size.y),
    #                                           (offset_position.x + player.size.x, offset_position.y)],
    #                                 texture, 0, 0)
    if draw_collisions:
        collider = player.get_collider()
        pygame.draw.polygon(surface, (0, 255, 0), [(v + offset + collider.pos).as_tuple() for v in collider.vertices])
