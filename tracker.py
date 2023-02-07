import numpy as np
import vision

class Tracker:
    def __init__(self, api, config):
        self.api = api
        self.config = config
        self.zones = [self._match_zone(zone) for zone in config['zones']]

    def _match_statuses(self, picture, statuses):
        grey_image = vision.make_gray(picture)
        result = [(name, np.amax(vision.match(grey_image, template, mask))) for name, template, mask in statuses]
        return result

    def get_zone_screenshot(self, screenshot_props, survivor_index, zone):
        x, y = screenshot_props.left_top

        w, h = zone.size
        offset_x, offset_y = zone.offset

        x += offset_x
        y += screenshot_props.next_offset * survivor_index + offset_y

        return self.api.get_screenshot(x, y, w, h)

    def _match_zone(self, zone):

        names = []
        templates = []
        masks = []
        for status in zone.states:
            if 'png' in status.path:
                names.append(status.name)
                templates.append(vision.read_template(status.path))
            elif 'bmp' in status.path:
                masks.append(vision.read_mask(status.path))

        states = list(zip(names, templates, masks))

        def match_screenshot(screenshot_props, survivor_index):
            screenshot = self.get_zone_screenshot(
                screenshot_props, survivor_index, zone)
            matches = self._match_statuses(screenshot, states)
            return max(matches, key=lambda state: state[1])

        return match_screenshot

    def survivor_hud_tracker(self, survivors_count=4):
        def match_zones(screenshot_props, survivor_index):
            return [match(screenshot_props, survivor_index) for match in self.zones]

        def match_survivor_statuses(screenshot_props):
            return [match_zones(screenshot_props, i) for i in range(survivors_count)]

        return match_survivor_statuses(self.config['screenshot_props'])
    
    def predict_survivor_status(self, survivor):
        return [{ self.config['zones'][i].name: name } if value >= self.config['zones'][i].threshold else { self.config['zones'][i].name: 'unknown' }
            for i, (name, value) in enumerate(survivor)]
    
    def get_survivor_screenshot(self, survivor_index):
        screenshot = self.get_zone_screenshot(self.config['screenshot_props'], survivor_index, self.config['zones'][1])
        return screenshot
