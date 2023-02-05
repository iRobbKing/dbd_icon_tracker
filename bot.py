import config
import tracker


def match_survivors_state():
    hud_tracker = tracker.survivor_hud_tracker(config.ZONES)

    def clamp_survivor_status(survivor):
        return [(name, value) if value >= config.ZONES[i].threshold else None
                for i, (name, value) in enumerate(survivor)]

    def track():
        return [clamp_survivor_status(survivor)
                for survivor in hud_tracker(config.SCREENSHOT_PROPS)]

    return track
