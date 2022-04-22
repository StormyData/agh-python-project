import xml.etree.ElementTree as ETree

from src.Level import Level
from src.LevelObjects.Platforms import Platform, MovingPlatform, DisappearingPlatform, ChangingSizePlatform
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
    bg = None
    if 'background' in root.attrib:
        bg = root.attrib['background']
    # if 'name' not in root.attrib:
    #    raise ParseError("level doesn't have a name")
    # name = root.attrib['name']
    contents = set()
    for index, child in enumerate(root):
        match child.tag:
            case "platform":
                contents.add(_parse_platform(child))
            case "moving_platform":
                contents.add(_parse_moving_platform(child))
            case "disappearing_platform":
                contents.add(_parse_disappearing_platform(child))
            case "changing_size_platform":
                contents.add(_parse_changing_size_platform(child))
            case _:
                raise ParseError("unknown level element")
    return Level(contents, bg)


def _parse_changing_size_platform(element: ETree.Element) -> ChangingSizePlatform:
    fields = {'position': _parse_vector, 'size': _parse_vector, 'texture': str, 'texture_pos': _parse_vector,
              'max_size': _parse_vector, 'min_size': _parse_vector, 'speed': _parse_vector}
    field_renames = {'texture': 'texture_name', 'time': 'max_time'}
    defaults = {'texture_pos': Vector(0, 0)}
    return _parse(element, ChangingSizePlatform, fields, field_renames, defaults)


def _parse_disappearing_platform(element: ETree.Element) -> DisappearingPlatform:
    fields = {'position': _parse_vector, 'size': _parse_vector, 'texture': str, 'texture_pos': _parse_vector,
              'time': _parse_vector}
    field_renames = {'texture': 'texture_name', 'time': 'max_time'}
    defaults = {'texture_pos': Vector(0, 0)}
    return _parse(element, DisappearingPlatform, fields, field_renames, defaults)


def _parse_moving_platform(element: ETree.Element) -> MovingPlatform:
    fields = {'position': _parse_vector, 'size': _parse_vector, 'texture': str, 'texture_pos': _parse_vector,
              'start_position': _parse_vector, 'end_position': _parse_vector, 'speed': _parse_vector}
    field_renames = {'texture': 'texture_name'}
    defaults = {'texture_pos': Vector(0, 0)}
    return _parse(element, MovingPlatform, fields, field_renames, defaults)


def _parse_platform(element: ETree.Element) -> Platform:
    fields = {'position': _parse_vector, 'size': _parse_vector, 'texture': str, 'texture_pos': _parse_vector}
    field_renames = {'texture': 'texture_name'}
    defaults = {'texture_pos': Vector(0, 0)}
    return _parse(element, Platform, fields, field_renames, defaults)


def _parse_vector(val: str) -> Vector:
    if ',' not in val:
        raise ParseError(f"vector must be a pair of floats separated by a ',' not {val}")
    tab = val.split(",")
    if len(tab) != 2:
        raise ParseError(f"vector must be a pair of floats separated by a ',' not {val}")
    x, y = tab
    x = vector_scale * float(x)
    y = vector_scale * float(y)
    return Vector(x, y)


def _parse(element: ETree.Element, constructor, fields, field_renames=None, defaults=None):
    if defaults is None:
        defaults = dict()
    if field_renames is None:
        field_renames = dict()

    constructor_dict = dict()
    for field in fields:
        value = None
        if field not in element.attrib:
            if field not in defaults:
                raise ParseError(f"{constructor.__name__} requires a {field}")
            value = defaults[field]
        else:
            value = fields[field](element.attrib[field])
        constructor_dict[field_renames.get(field, field)] = value
    return constructor(**constructor_dict)
