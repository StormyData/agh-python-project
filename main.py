from src.Parser import parse_file


def main():
    level = parse_file("levels/level01.xml")
    return level


if __name__ == "__main__":
    main()
