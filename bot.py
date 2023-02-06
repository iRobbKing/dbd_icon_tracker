import config
import vision

class DbdHudTracker:
    def __init__(self, tracker):
        self.tracker = tracker
        self.windows = [0, 0, 0, 0]
        for i in range(4):
            self.windows[i] = vision.create_window(f's{i}')
    
    def get_survivor_screenshot(self, survivor_index):
        screenshot = self.tracker.take_zone_screenshot(
                config.SCREENSHOT_PROPS,
                survivor_index,
                config.ZONES[1]
            )
        return screenshot

    def get_survivors_states(self):
        return self.match_survivors_state()()
    
    def show(self):
        survs = self.get_survivors_states()
        for i in range(4):
            img = self.get_survivor_screenshot(i)
            vision.set_title(f's{i}', f's{i} - {survs[i]}')
            vision.show(f's{i}', img)  

    def match_survivors_state(self):
        hud_tracker = self.tracker.survivor_hud_tracker(config.ZONES)
        
        def clamp_survivor_status(survivor):
            return [{ config.ZONES[i].name: name } if value >= config.ZONES[i].threshold else { config.ZONES[i].name: 'unknown' }
                    for i, (name, value) in enumerate(survivor)]

        def track():
            return [clamp_survivor_status(survivor)
                    for survivor in hud_tracker(config.SCREENSHOT_PROPS)]

        return track
