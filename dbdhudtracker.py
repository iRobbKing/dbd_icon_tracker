import vision
import config
from capture import WinAPI
from tracker import Tracker

class DbdHudTracker:
    def __init__(self, tracker):
        self.tracker = tracker
        self.windows = [0, 0, 0, 0]
        for i in range(4):
            self.windows[i] = vision.create_window(f's{i}')
    
    def show(self):
        survs = self.get_survivor_statuses()
        for i in range(4):
            img = self.tracker.get_survivor_screenshot(i)
            vision.set_title(f's{i}', f's{i} - {survs[i]}')
            vision.show(f's{i}', img)  

    def get_survivor_statuses(self):
        return [self.tracker.predict_survivor_status(survivor) for survivor in self.tracker.survivor_hud_tracker()]
