import xml.etree.ElementTree as ETree

from src.Level import Level
from src.Platform import Platform
from src.Vector import Vector

vector_scale = 16

class ParseError(Exception):
    pass


def parse_file(filename: str) -> Level:
    tree = ETree.parse(filename)
    return _parse_level(tree)


def _parse_level(tree: ETree.ElementTree) -> Level:
    root = tree.getroot()
    if root.tag != "level":
        raise ParseError("root node is not level")
    # if 'name' not in root.attrib:
    #    raise ParseError("level doesn't have a name")
    # name = root.attrib['name']
    contents = set()
    for index, child in enumerate(root):
        match child.tag:
            case "platform":
                contents.add(_parse_platform(child))
            case _:
                raise ParseError("unknown level element")
    return Level(contents)


def _parse_platform(element: ETree.Element) -> Platform:
    if 'position' not in element.attrib:
        raise ParseError("platform requires a position")
    if 'size' not in element.attrib:
        raise ParseError("platform requires a size")
    if 'texture' not in element.attrib:
        raise ParseError("platform requires a texture name")
    position = _parse_vector(element.attrib['position'])
    size = _parse_vector(element.attrib['size'])
    texture = element.attrib['texture']
    return Platform(position, size, texture)


def _parse_vector(val: str) -> Vector:
    if ',' not in val:
        raise ParseError(f"vector must be a pair of floats separated by a ',' not {val}")
    tab = val.split(",")
    if len(tab) != 2:
        raise ParseError(f"vector must be a pair of floats separated by a ',' not {val}")
    x, y = tab
    x = vector_scale*float(x)
    y = vector_scale*float(y)
    return Vector(x, y)
