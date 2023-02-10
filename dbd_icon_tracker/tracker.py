import numpy as np

from . import vision


def _read_template(path):
    return vision.make_gray(vision.read_image(path))


def _match_statuses(picture, statuses):
    grey_image = vision.make_gray(picture)
    return [(name, np.amax(np.nan_to_num(vision.match(grey_image, template, mask), False, nan=0.0, posinf=0.0, neginf=0.0))) for name, template, mask in statuses]


def _match_zone(zone):
    states = tuple((status.name, _read_template(status.path), _read_template(status.mask))
                   for status in zone.states)

    def match_screenshot(screenshot):
        matches = _match_statuses(screenshot, states)
        return max(matches, key=lambda state: state[1])

    return match_screenshot


def get_zone_box(screenshot_props, survivor_index, zone):
    x, y = screenshot_props.left_top

    w, h = zone.size
    offset_x, offset_y = zone.offset

    x += offset_x
    y += screenshot_props.next_offset * survivor_index + offset_y

    return x, y, w, h


def survivor_hud_tracker(take_screenshot, screenshot_props, zones, survivors_count=4):
    matches = [_match_zone(zone) for zone in zones]

    def match_zones(survivor_index):
        return [match(take_screenshot(*get_zone_box(screenshot_props, survivor_index, zones[i])))
                for i, match in enumerate(matches)]

    return [match_zones(i) for i in range(survivors_count)]


