from enum import Enum, auto, unique
import pygame.mixer
from src.Systems.AssetLoader import AssetLoader
from io import BytesIO
@unique
class SoundEvent(Enum):
    PLAYER_STARTED_MOVING = auto()
    PLAYER_STOPPED_MOVING = auto()
    PLAYER_OFF_GROUND = auto()
    PLAYER_ON_GROUND = auto()
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
        self._walking_sound = SoundEngine._get_sound("player_walk")
        self._player_moving = False
        self._player_on_ground = False

    def send_event(self, event: SoundEvent):
        match event:
            case SoundEvent.PLAYER_CHECKPOINT_SET:
                SoundEngine._get_sound("checkpoint_set").play()
            case SoundEvent.PLAYER_DIED:
                SoundEngine._get_sound("player_died").play()
            case SoundEvent.PLAYER_JUMPED:
                SoundEngine._get_sound("player_jumped").play()
            case SoundEvent.PLAYER_STARTED_MOVING:
                self._player_moving = True
                if self._player_on_ground:
                    self._walking_sound.play(-1)
            case SoundEvent.PLAYER_STOPPED_MOVING:
                if self._player_on_ground and self._player_moving:
                    self._walking_sound.stop()
                self._player_moving = False
            case SoundEvent.PLAYER_GONE_HOME:
                SoundEngine._get_sound("player_gone_home").play()

            case SoundEvent.SCREEN_ENTERED_MENU:
                pygame.mixer.music.load(AssetLoader.get_singleton().get_music_path("main_menu"))
                pygame.mixer.music.play(loops=-1)
                if self._player_on_ground and self._player_moving:
                    self._walking_sound.stop()
                self._player_moving = False
                self._player_on_ground = False
            case SoundEvent.SCREEN_RESUMED_LEVEL:
                pygame.mixer.music.unpause()
                if self._player_on_ground and self._player_moving:
                    self._walking_sound.play()

            case SoundEvent.SCREEN_ENTERED_LEVEL:
                pygame.mixer.music.load(AssetLoader.get_singleton().get_music_path("level"))
                pygame.mixer.music.play(loops=-1)

            case SoundEvent.SCREEN_ENTERED_ESCAPE_PANEL:
                pygame.mixer.music.pause()
                if self._player_on_ground and self._player_moving:
                    self._walking_sound.stop()

            case SoundEvent.PLAYER_OFF_GROUND:
                self._player_on_ground = False
                if self._player_moving:
                    self._walking_sound.stop()
            case SoundEvent.PLAYER_ON_GROUND:
                self._player_on_ground = True
                if self._player_moving:
                    self._walking_sound.play(-1)
    @staticmethod
    def _get_sound(name: str) -> pygame.mixer.Sound:
        with BytesIO(AssetLoader.get_singleton().get_sound_buffer(name)) as f:
            return pygame.mixer.Sound(f)