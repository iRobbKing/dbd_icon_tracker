import numpy as np
import vision


def _read_template(path):
    return vision.make_gray(vision.read_image(path))


def _match_statuses(picture, statuses):
    grey_image = vision.make_gray(picture)
    result = [(name, np.amax(vision.match(grey_image, template, mask))) for name, template, mask in statuses]
    return result


class Tracker:
    def __init__(self, api, config):
        self.api = api
        self.config = config
        self.zones = [self._match_zone(zone) for zone in config['zones']]

    def get_zone_screenshot(self, screenshot_props, survivor_index, zone):
        x, y = screenshot_props.left_top

        w, h = zone.size
        offset_x, offset_y = zone.offset

        x += offset_x
        y += screenshot_props.next_offset * survivor_index + offset_y

        return self.api.get_screenshot(x, y, w, h)

    def _match_zone(self, zone):
        states = tuple((status.name, _read_template(status.path), _read_template(status.mask))
                       for status in zone.states)

        def match_screenshot(screenshot_props, survivor_index):
            screenshot = self.get_zone_screenshot(screenshot_props, survivor_index, zone)
            matches = _match_statuses(screenshot, states)
            return max(matches, key=lambda state: state[1])

        return match_screenshot

    def survivor_hud_tracker(self, survivors_count=4):
        def match_zones(screenshot_props, survivor_index):
            return [match(screenshot_props, survivor_index) for match in self.zones]

        def match_survivor_statuses(screenshot_props):
            return [match_zones(screenshot_props, i) for i in range(survivors_count)]

        return match_survivor_statuses(self.config['screenshot_props'])

    def predict_survivor_status(self, survivor):
        return [{self.config['zones'][i].name: name}
                if value >= self.config['zones'][i].threshold else
                {self.config['zones'][i].name: None}
                for i, (name, value) in enumerate(survivor)]

    def get_survivor_screenshot(self, survivor_index):
        return self.get_zone_screenshot(self.config['screenshot_props'], survivor_index, self.config['zones'][1])
