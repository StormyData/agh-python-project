from enum import Enum, auto, unique
import pygame.mixer
import logging
from src.Systems.AssetLoader import AssetLoader
from io import BytesIO
@unique
class SOUND_EVENT(Enum):
    PLAYER_STARTED_MOVING = auto()
    PLAYER_STOPPED_MOVING = auto()
    PLAYER_JUMPED = auto()
    PLAYER_DIED = auto()
    PLAYER_CHECKPOINT_SET = auto()
    PLAYER_GONE_HOME = auto()
    SCREEN_ENTERED_MENU = auto()
    SCREEN_ENTERED_ESCAPE_PANEL = auto()
    SCREEN_ENTERED_LEVEL = auto()
    SCREEN_RESUMED_LEVEL = auto()


class SoundEngine:
    _instance = None

    @staticmethod
    def get_singleton():
        if SoundEngine._instance is None:
            SoundEngine._instance = SoundEngine()
        return SoundEngine._instance

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        pass

    def send_event(self, event: SOUND_EVENT):
        match event:
            case SOUND_EVENT.PLAYER_CHECKPOINT_SET:
                SoundEngine._get_sound("checkpoint_set").play()
            case SOUND_EVENT.PLAYER_DIED:
                SoundEngine._get_sound("player_died").play()
            case SOUND_EVENT.PLAYER_JUMPED:
                SoundEngine._get_sound("player_jumped").play()
            case SOUND_EVENT.PLAYER_STARTED_MOVING:
                logging.getLogger().debug("starting playing player moving")
            case SOUND_EVENT.PLAYER_STOPPED_MOVING:
                logging.getLogger().debug("stopping playing player moving")
            case SOUND_EVENT.PLAYER_GONE_HOME:
                SoundEngine._get_sound("player_gone_home").play()

            case SOUND_EVENT.SCREEN_ENTERED_MENU:
                pygame.mixer.music.load(AssetLoader.get_singleton().get_music_path("main_menu"))
                pygame.mixer.music.play(loops=-1)
            case SOUND_EVENT.SCREEN_RESUMED_LEVEL:
                pygame.mixer.music.unpause()
            case SOUND_EVENT.SCREEN_ENTERED_LEVEL:
                pygame.mixer.music.load(AssetLoader.get_singleton().get_music_path("level"))
                pygame.mixer.music.play(loops=-1)
            case SOUND_EVENT.SCREEN_ENTERED_ESCAPE_PANEL:
                pygame.mixer.music.pause()
    @staticmethod
    def _get_sound(name: str) -> pygame.mixer.Sound:
        with BytesIO(AssetLoader.get_singleton().get_sound_buffer(name)) as f:
            return pygame.mixer.Sound(f)