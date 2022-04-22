from src.LevelObjects.LevelObject import LevelObject


class Level:
    def __init__(self, objects: [LevelObject], background_texture_name: str):
        self.objects = objects
        self.background_texture_name = background_texture_name

    def update(self, dt: float):
        for game_object in self.objects:
            game_object.update(dt)
