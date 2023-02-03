from dataclasses import dataclass
import os
import tomllib
from typing import Any


@dataclass
class ScreenshotProps:
    top_left: tuple[int, int]
    next_offset: int


def _map_lists_to_tuples(table: dict[str, Any]) -> dict[str, Any]:
    def inner_map(value: Any) -> Any:
        if isinstance(value, dict):
            return _map_lists_to_tuples(value)

        return tuple(value) if isinstance(value, list) else value

    return {key: inner_map(value) for key, value in table.items()}


def _read_config():
    with open('config.toml', 'rb') as file:
        config = tomllib.load(file)

    return _map_lists_to_tuples(config)


def _map_status_templates(statuses: dict) -> dict:
    def map_template(status: dict[str, str]) -> dict[str, str]:
        status['template'] = os.path.join('icons', status['template'])
        return status

    return {status_name: map_template(status_props) for status_name, status_props in statuses.items()}


_CONFIG = _read_config()

SCREENSHOT_PROPS = ScreenshotProps(**_CONFIG['screenshot_props'])
SCREENSHOT_ZONES = _CONFIG['screenshot_zones']
STATUSES = _map_status_templates(_CONFIG['statuses'])
