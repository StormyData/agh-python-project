import xml.etree.ElementTree as ETree

from pygame import Surface, image

from src.Drawing.Animation import AnimationBuffer, AnimationFrame
from src.Vector import Vector


def _parse_vector(val: str) -> Vector:
    if ',' not in val:
        raise ValueError(f"vector must be a pair of floats separated by a ',' not {val}")
    tab = val.split(",")
    if len(tab) != 2:
        raise ValueError(f"vector must be a pair of floats separated by a ',' not {val}")
    x, y = tab
    return Vector(x, y)


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
        self._animations = dict()
        self._animation_names_to_paths = dict()
        self._music_paths = dict()
        self._sound_names_to_paths = dict()
        self._sounds = dict()

    def load_paths(self, fp: str):
        tree = ETree.parse(fp)
        root = tree.getroot()
        if root.tag != "assets":
            raise ValueError("root must be named assets")
        for child in root:
            match child.tag:
                case "img":
                    self._read_img(child)
                case "anim":
                    self._read_anim(child)
                case "music":
                    self._read_music(child)
                case "sound":
                    self._read_sound(child)

    def _read_anim(self, child: ETree.Element):
        if 'name' not in child.attrib:
            raise ValueError("anim is missing attribute: name")
        content = []
        for c in child:
            if c.tag != "img":
                raise ValueError("unrecognized type of child in anim")
            if 'path' not in c.attrib:
                raise ValueError("frame doesn't have a path")
            offset = Vector(0, 0)
            if 'offset' in c.attrib:
                offset = _parse_vector(c.attrib['offset'])
            length = 1
            if 'len' in c.attrib:
                length = float(c.attrib['len'])
            content.append(AnimationFrame(c.attrib['path'], length, offset))
        self._animation_names_to_paths[child.attrib['name']] = AnimationBuffer(content)

    def _read_img(self, child: ETree.Element):
        if 'path' not in child.attrib:
            raise ValueError("img is missing attribute: path")
        if 'name' not in child.attrib:
            raise ValueError("img is missing attribute: name")
        self._image_names_to_paths[child.attrib['name']] = child.attrib['path']

    def _load_anim(self, name: str):
        frames = self._animation_names_to_paths[name].frames
        for i in range(len(frames)):
            frames[i].img = image.load(frames[i].img, "")
        self._animations[name] = self._animation_names_to_paths[name]

    def get_image(self, name: str) -> Surface:
        if name not in self._images:
            if name not in self._image_names_to_paths:
                raise ValueError(f"unknown image name: {name}")
            self._images[name] = image.load(self._image_names_to_paths[name], "")
        return self._images[name]

    def get_animation_buffer(self, name: str) -> AnimationBuffer:
        if name not in self._animations:
            if name not in self._animation_names_to_paths:
                raise ValueError(f"unknown animation name: {name}")
            self._load_anim(name)
        return self._animations[name]

    def get_sound_buffer(self, name: str) -> bytes:
        if name not in self._sounds:
            if name not in self._sound_names_to_paths:
                raise ValueError(f"unknown sound name: {name}")
            with open(self._sound_names_to_paths[name], "rb") as f:
                self._sounds[name] = f.read()
        return self._sounds[name]

    def get_music_path(self, name: str) -> str:
        if name not in self._music_paths:
            raise ValueError(f"unknown music name")
        return self._music_paths[name]

    def _read_music(self, child: ETree.Element):
        if 'path' not in child.attrib:
            raise ValueError("music is missing attribute: path")
        if 'name' not in child.attrib:
            raise ValueError("music is missing attribute: name")
        self._music_paths[child.attrib['name']] = child.attrib['path']

    def _read_sound(self, child: ETree.Element):
        if 'path' not in child.attrib:
            raise ValueError("sound is missing attribute: path")
        if 'name' not in child.attrib:
            raise ValueError("sound is missing attribute: name")
        self._sound_names_to_paths[child.attrib['name']] = child.attrib['path']
