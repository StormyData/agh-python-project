from src.Game import Game
from src.Parser import parse_file
from src.AssetLoader import AssetLoader


def main():
    AssetLoader.get_singleton().load_paths("assets/descriptor.xml")
    print(AssetLoader.get_singleton().get_image("grass0"))
    level = parse_file("levels/level01.xml")

    game = Game()
    game.load_level(level)

    return level


if __name__ == "__main__":
    main()
