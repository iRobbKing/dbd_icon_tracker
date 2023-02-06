import itertools
import numpy as np
import config
import tracker
import capture
import cv2

api = capture.WinAPI('DeadByDaylight')
track =  tracker.Tracker(api)

class DbdHudTracker:
    def __init__(self):
        # self.templates = self.prepare_templates()
        self.windows = [0, 0, 0, 0]
        for i in range(4):
            self.windows[i] = cv2.namedWindow(f's{i}', cv2.WINDOW_NORMAL)
            cv2.resizeWindow(f's{i}', 250, 250)
            cv2.setWindowProperty(f's{i}', cv2.WND_PROP_TOPMOST, 1)
            
    def prepare_templates(self):
        return track.read_status_templates(config.STATUSES)
    
    def get_survivor_screenshot(self, survivor_index):
        screenshot = track.take_zone_screenshot(
                survivor_index,
                config.SCREENSHOT_PROPS,
                config.SCREENSHOT_ZONES['state']
            )
        return screenshot
    
    def predict_survivor_state(self, statuses, survivor_index):
        grouped_by_zone = itertools.groupby(statuses.items(), lambda status: status[1]['zone'])
        state_names = list(statuses.keys())
        states = []

        for zone, statuses in grouped_by_zone:
            screenshot = self.get_survivor_screenshot(survivor_index)

            for status_name, status_props in statuses:
                if zone == 'state':
                    prob = track.match_survivor_state(status_props, screenshot)
                    states.append(prob)

        maxState = max(states)
        index = np.where(states == maxState)[0][0]
        threshold = 0.7
        return state_names[index] if maxState > threshold else 'healthy'
    
    def get_survivors_states(self, states):
        return [
            self.predict_survivor_state(states, 0),
            self.predict_survivor_state(states, 1),
            self.predict_survivor_state(states, 2),
            self.predict_survivor_state(states, 3)
        ]
    
    def get_states(self):
        return self.get_survivors_states(self.templates)
    
    def get_state(self, surv_index):
        return self.predict_survivor_state(self.templates, surv_index)

    def show(self):
        for i in range(4):
            img = self.get_survivor_screenshot(i)
            state = self.get_state(i)
            cv2.setWindowTitle(f's{i}', f's{i} - {state}')
            cv2.imshow(f's{i}', img)
        cv2.waitKey(1)

    def match_survivors_state(self):
        hud_tracker = track.survivor_hud_tracker(config.ZONES)

        def clamp_survivor_status(survivor):
            return [(name, value) if value >= config.ZONES[i].threshold else None
                    for i, (name, value) in enumerate(survivor)]

        def track1():
            return [clamp_survivor_status(survivor)
                    for survivor in hud_tracker(config.SCREENSHOT_PROPS)]

        return track1
