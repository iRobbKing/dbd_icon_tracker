import config
import cv2

class DbdHudTracker:
    def __init__(self, tracker):
        self.tracker = tracker
        self.windows = [0, 0, 0, 0]
        for i in range(4):
            self.windows[i] = cv2.namedWindow(f's{i}', cv2.WINDOW_NORMAL)
            cv2.resizeWindow(f's{i}', 450, 300)
            cv2.setWindowProperty(f's{i}', cv2.WND_PROP_TOPMOST, 1)
            
    def prepare_templates(self):
        return self.tracker.read_status_templates(config.STATUSES)
    
    def get_survivor_screenshot(self, survivor_index):
        screenshot = self.tracker.take_zone_screenshot(
                config.SCREENSHOT_PROPS,
                survivor_index,
                config.ZONES[1]
            )
        return screenshot
    
    def predict_survivor_state(self):
        return self.match_survivors_state()()
    
    def get_survivors_states(self):
        return self.predict_survivor_state()
    
    def get_states(self):
        return self.get_survivors_states(self.templates)
    
    def get_state(self, surv_index):
        return self.predict_survivor_state(self.templates, surv_index)

    def show(self):
        survs = self.get_survivors_states()
        for i in range(4):
            img = self.get_survivor_screenshot(i)
            cv2.setWindowTitle(f's{i}', f's{i} - {survs[i]}')
            cv2.imshow(f's{i}', img)
        cv2.waitKey(1)

    def match_survivors_state(self):
        hud_tracker = self.tracker.survivor_hud_tracker(config.ZONES)
        
        def clamp_survivor_status(survivor):
            return [{ config.ZONES[i].name: name } if value >= config.ZONES[i].threshold else { config.ZONES[i].name: 'unknown' }
                    for i, (name, value) in enumerate(survivor)]

        def track1():
            return [clamp_survivor_status(survivor)
                    for survivor in hud_tracker(config.SCREENSHOT_PROPS)]

        return track1
