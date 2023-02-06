import numpy as np
import cv2

class Tracker:
    def __init__(self, api):
        self.api = api

    def match_survivor_state(self, state: dict, screenshot):
        result = cv2.matchTemplate(screenshot, state['template'], cv2.TM_CCOEFF_NORMED)
        return np.max(result)
    

    def read_picture_from_file(self, path):
        return cv2.imread(path)

    def read_template(self, path):
        return cv2.cvtColor(cv2.imread(path), cv2.COLOR_RGB2GRAY)

    def read_status_templates(self, statuses):
        def add_template_to_status(status):
            status['template'] = self.read_template(status['template'])
            return status

        return {status_name: add_template_to_status(status_props) for status_name, status_props in statuses.items()}
    
    def make_gray(self, picture):
        return cv2.cvtColor(picture, cv2.COLOR_RGB2GRAY)
    
    def match(self, picture, template):
        return cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED)

    def _match_statuses(self, picture, statuses):
        grey_image = self.make_gray(picture)
        return [(name, np.amax(self.match(grey_image, template))) for name, template in statuses]

    def take_zone_screenshot(self, screenshot_props, survivor_index, zone):
        x, y = screenshot_props.left_top

        w, h = zone.size
        offset_x, offset_y = zone.offset

        x += offset_x
        y += screenshot_props.next_offset * survivor_index + offset_y

        return self.api.get_screenshot(x, y, w, h)

    def _match_zone(self, zone):
        states = [(status.name, self.read_template(status.path)) for status in zone.states]

        def take_screenshot(screenshot_props, survivor_index):
            screenshot = self.take_zone_screenshot(screenshot_props, survivor_index, zone)
            matches = self._match_statuses(screenshot, states)
            return max(matches, key=lambda state: state[1])

        return take_screenshot

    def survivor_hud_tracker(self, zones, survivors_count=4):
        zone_matchers = [self._match_zone(zone) for zone in zones]

        def match_zones(screenshot_props, survivor_index):
            return [match(screenshot_props, survivor_index) for match in zone_matchers]

        def match_survivor_statuses(screenshot_props):
            return [match_zones(screenshot_props, i) for i in range(survivors_count)]

        return match_survivor_statuses
