import xml.etree.ElementTree as ETree

from src.Level import Level
from src.LevelObjects.Platforms import Platform, MovingPlatform, DisappearingPlatform, ChangingSizePlatform
from src.LevelObjects.Checkpoint import Checkpoint
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
            case "checkpoint":
                contents.add(_parse_checkpoint(child))
            case _:
                raise ParseError("unknown level element")
    return Level(contents, bg)


def _parse_checkpoint(element: ETree.Element) -> Checkpoint:
    fields = {'id': str, 'tele_to': _parse_vector}
    child_nodes = {'v': _parse_platform_vertex}
    field_renames = {'v': 'vertices'}
    return _parse(element, Checkpoint, fields, field_renames, child_nodes=child_nodes)


def _parse_changing_size_platform(element: ETree.Element) -> ChangingSizePlatform:
    fields = {'init_size': float, 'texture': str, 'texture_pos': _parse_vector,
              'max_size': float, 'min_size': float, 'speed': float}
    field_renames = {'texture': 'texture_name', 'v': 'vertices'}

    child_nodes = {'v': _parse_platform_vertex}
    defaults = {'texture_pos': Vector(0, 0), 'init_size': 1}
    return _parse(element, ChangingSizePlatform, fields, field_renames, defaults,child_nodes)


def _parse_disappearing_platform(element: ETree.Element) -> DisappearingPlatform:
    fields = {'texture': str, 'texture_pos': _parse_vector,
              'time': float}
    field_renames = {'texture': 'texture_name', 'time': 'max_time', 'v': 'vertices'}
    defaults = {'texture_pos': Vector(0, 0)}
    child_nodes = {'v': _parse_platform_vertex}
    return _parse(element, DisappearingPlatform, fields, field_renames, defaults, child_nodes)


def _parse_moving_platform(element: ETree.Element) -> MovingPlatform:
    fields = {'texture': str, 'texture_pos': _parse_vector,
              'start_position': _parse_vector, 'end_position': _parse_vector, 'speed': _parse_vector}
    field_renames = {'texture': 'texture_name', 'v': 'vertices'}
    defaults = {'texture_pos': Vector(0, 0)}
    child_nodes = {'v': _parse_platform_vertex}
    return _parse(element, MovingPlatform, fields, field_renames, defaults, child_nodes)


def _parse_platform(element: ETree.Element) -> Platform:
    fields = {'texture': str, 'texture_pos': _parse_vector}
    field_renames = {'texture': 'texture_name', 'v': 'vertices'}
    defaults = {'texture_pos': Vector(0, 0)}
    child_nodes = {'v': _parse_platform_vertex}
    return _parse(element, Platform, fields, field_renames, defaults, child_nodes)


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


def _parse_platform_vertex(element: ETree.Element) -> Vector:
    return _parse_vector(element.attrib['pos'])


def _parse(element: ETree.Element, constructor, fields, field_renames=None, defaults=None, child_nodes=None):
    if child_nodes is None:
        child_nodes = dict()
    if defaults is None:
        defaults = dict()
    if field_renames is None:
        field_renames = dict()

    constructor_dict = dict()
    for child_node in child_nodes:
        field_name = field_renames.get(child_node, child_node)
        constructor_dict[field_name] = []

    for field in fields:
        value = None
        if field not in element.attrib:
            if field not in defaults:
                raise ParseError(f"{constructor.__name__} requires a {field}")
            value = defaults[field]
        else:
            value = fields[field](element.attrib[field])
        constructor_dict[field_renames.get(field, field)] = value

    for child in element:
        if child.tag not in child_nodes:
            raise ParseError(f"{child.tag} not specified in a list of allowed children for {constructor.__name__}")
        field_name = field_renames.get(child.tag, child.tag)
        constructor_dict[field_name].append(child_nodes[child.tag](child))
    return constructor(**constructor_dict)
