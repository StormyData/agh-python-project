from src.Game import Game
from src.Parser import parse_file
from src.AssetLoader import AssetLoader


def main():
    AssetLoader.get_singleton().load_paths("assets/descriptor.xml")
    level = parse_file("levels/level01.xml")

    game = Game()
    game.load_level(level)

    return level


if __name__ == "__main__":
    main()
