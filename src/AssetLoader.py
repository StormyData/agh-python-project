import xml.etree.ElementTree as ETree
from pygame import Surface,image

from src.Parser import ParseError

class AssetLoader:
    _instance = None

    @staticmethod
    def get_singleton():
        if AssetLoader._instance is None:
            AssetLoader._instance = AssetLoader()
        return AssetLoader._instance

    def __init__(self):
        self._images = dict()
        self._image_names_to_paths = dict()

    def load_paths(self, fp: str):
        tree = ETree.parse(fp)
        root = tree.getroot()
        if root.tag != "assets":
            raise ParseError("root must be named assets")
        for child in root:
            match child.tag:
                case "img":
                    if 'path' not in child.attrib:
                        raise ParseError("img is missing attribute: path")
                    if 'name' not in child.attrib:
                        raise ParseError("img is missing attribute: name")
                    self._image_names_to_paths[child.attrib['name']] = child.attrib['path']
                case _:
                    pass  # ignore

    def get_image(self, name: str) -> Surface:
        if name not in self._images:
            if name not in self._image_names_to_paths:
                raise ValueError(f"unknown image name: {name}")
            self._images[name] = image.load(self._image_names_to_paths[name], "")
        return self._images[name]

    def get_sound_buffer(self, name: str) -> bytes:
        pass
