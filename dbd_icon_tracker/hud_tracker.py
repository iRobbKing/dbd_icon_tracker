from . import config
from . import tracker
from . import vision
import os

def _get_survivor_screenshot(take_screenshot, survivor_index, zone):
    return take_screenshot(*tracker.get_zone_box(config.SCREENSHOT_PROPS, survivor_index, zone))


def show_survivor_portraits(take_screenshot):
    for i in range(4):
        vision.show_image_in_window(f'survivor {i}', _get_survivor_screenshot(take_screenshot, i, config.ZONES[1]))

    vision.wait(1)


def _clamp_survivor_status(survivor):
    return [{config.ZONES[i].name: name}
            if value >= config.ZONES[i].threshold else
            {config.ZONES[i].name: None}
            for i, (name, value) in enumerate(survivor)]


def get_survivor_statuses(take_screenshot):
    survivors_statuses = tracker.survivor_hud_tracker(take_screenshot, config.SCREENSHOT_PROPS, config.ZONES)
    return [_clamp_survivor_status(survivor_status)
            for survivor_status in survivors_statuses]

def get_game_status(take_screenshot):
    zone = tracker._match_zone(config.ZONES[1])
    x, y = config.ZONES[1].offset
    w, h = config.ZONES[1].size
    name, value = zone(take_screenshot(x, y, w, h))
    return 'unknown' if value < config.ZONES[1].threshold else name


