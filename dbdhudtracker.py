import vision


class DbdHudTracker:
    def __init__(self, tracker):
        self.tracker = tracker
        self.windows = [vision.create_window(f's{i}') for i in range(4)]
    
    def show(self, delay):
        def map_status_name(name):
            return name if name is not None else 'unknown'

        def map_survivor_statuses(statuses):
            return ', '.join((f'{map_status_name(status_name)}: {status_value}'
                    for status in statuses
                    for status_name, status_value in status.items()))

        statuses = self.get_survivor_statuses()

        print([map_survivor_statuses(status) for status in statuses])

        for i, survivor in enumerate(statuses):
            img = self.tracker.get_survivor_screenshot(i)
            vision.set_window_name(f's{i}', f's{i} - {survivor}')
            vision.show_image_in_window(f's{i}', img, delay)

    def get_survivor_statuses(self):
        return [self.tracker.predict_survivor_status(survivor) for survivor in self.tracker.survivor_hud_tracker()]
