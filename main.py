from src.Game import Game
from src.Systems.Parser import parse_file
from src.Systems.AssetLoader import AssetLoader


def main():
    AssetLoader.get_singleton().load_paths("assets/descriptor.xml")
    Game()


if __name__ == "__main__":
    main()
