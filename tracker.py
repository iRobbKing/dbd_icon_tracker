import numpy as np
import cv2

class Tracker:
    def __init__(self, api):
        self.api = api

    def match_survivor_state(self, state: dict, screenshot):
        result = cv2.matchTemplate(screenshot, state['template'], cv2.TM_CCOEFF_NORMED)
        return np.max(result)
    
    def take_zone_screenshot(self, survivor_index, screenshot_props, zone):
        x, y = screenshot_props.top_left

        w, h = zone['size']
        offset_x, offset_y = zone['offset']

        x += offset_x
        y += screenshot_props.next_offset * survivor_index + offset_y

        result = self.api.get_screenshot(x, y, w, h)
        return cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)

    def read_template(self, path):
        return cv2.cvtColor(cv2.imread(path), cv2.COLOR_RGB2GRAY)

    def read_status_templates(self, statuses):
        def add_template_to_status(status):
            status['template'] = self.read_template(status['template'])
            return status

        return {status_name: add_template_to_status(status_props) for status_name, status_props in statuses.items()}
