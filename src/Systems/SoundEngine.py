from enum import Enum, auto, unique


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

    def send_event(self, event: SOUND_EVENT):
        match event:
            case SOUND_EVENT.PLAYER_CHECKPOINT_SET:
                print("playing checkpoint set sound")
            case SOUND_EVENT.PLAYER_DIED:
                print("playing player died sound")
            case SOUND_EVENT.PLAYER_JUMPED:
                print("playing player jumped sound")
            case SOUND_EVENT.PLAYER_STARTED_MOVING:
                print("starting playing player moving")
            case SOUND_EVENT.PLAYER_STOPPED_MOVING:
                print("stopping playing player moving")
            case SOUND_EVENT.PLAYER_GONE_HOME:
                print("playing player gone home sound")

            case SOUND_EVENT.SCREEN_ENTERED_MENU:
                print("starting menu music")
            case SOUND_EVENT.SCREEN_RESUMED_LEVEL:
                print("resuming level music")
            case SOUND_EVENT.SCREEN_ENTERED_LEVEL:
                print("starting level music")
            case SOUND_EVENT.SCREEN_ENTERED_ESCAPE_PANEL:
                print("pausing level music")