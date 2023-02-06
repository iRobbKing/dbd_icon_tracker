from dataclasses import dataclass
import os
import tomllib


@dataclass
class ScreenshotProps:
    left_top: tuple[int, int]
    next_offset: int


@dataclass
class State:
    name: str
    path: str


@dataclass
class Zone:
    name: str
    offset: tuple[int, int]
    size: tuple[int, int]
    threshold: float
    states: tuple[State, ...]


def _map_lists_to_tuples(table):
    def inner_map(value):
        if isinstance(value, dict):
            return _map_lists_to_tuples(value)

        return tuple(value) if isinstance(value, list) else value

    return {key: inner_map(value) for key, value in table.items()}


def _read_config():
    with open('config.toml', 'rb') as file:
        config = tomllib.load(file)

    return _map_lists_to_tuples(config)


def _read_zones(screenshot_zones):
    files = list(os.walk('icons'))[1:]

    for dirs in files:
        zone_name = dirs[0].split('\\')[-1]
        zone_offset = screenshot_zones[zone_name]['offset']
        zone_size = screenshot_zones[zone_name]['size']
        zone_threshold = screenshot_zones[zone_name]['threshold']

        states = (State(status_path.split('.')[0], os.path.join(dirs[0], status_path)) for status_path in dirs[2])

        yield Zone(zone_name, zone_offset, zone_size, zone_threshold, tuple(states))


_CONFIG = _read_config()

SCREENSHOT_PROPS = ScreenshotProps(**_CONFIG['screenshot_props'])
ZONES = tuple(_read_zones(_CONFIG['screenshot_zones']))
