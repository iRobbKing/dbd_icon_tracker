import numpy as np

import vision


def _read_template(path):
    return vision.make_grey(vision.read_picture_from_file(path))


def _match_statuses(picture, statuses):
    grey_image = vision.make_grey(picture)
    return [(name, np.amax(vision.match(grey_image, template))) for name, template in statuses]


def _take_zone_screenshot(screenshot_props, survivor_index, zone):
    x, y = screenshot_props.top_left

    w, h = zone.size
    offset_x, offset_y = zone.offset

    x += offset_x
    y += screenshot_props.next_offset * survivor_index + offset_y

    return vision.take_screenshot(x, y, w, h)


def _match_zone(zone):
    statuses = [(status.name, _read_template(status.path)) for status in zone.statuses]

    def take_screenshot(screenshot_props, survivor_index):
        screenshot = _take_zone_screenshot(screenshot_props, survivor_index, zone)
        matches = _match_statuses(screenshot, statuses)
        return max(matches, key=lambda status: status[1])

    return take_screenshot


def survivor_hud_tracker(zones, survivors_count=4):
    zone_matchers = [_match_zone(zone) for zone in zones]

    def match_zones(screenshot_props, survivor_index):
        return [match(screenshot_props, survivor_index) for match in zone_matchers]

    def match_survivor_statuses(screenshot_props):
        return [match_zones(screenshot_props, i) for i in range(survivors_count)]

    return match_survivor_statuses
