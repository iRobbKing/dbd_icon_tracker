import config
import tracker


def match_survivors_state():
    hud_tracker = tracker.survivor_hud_tracker(config.ZONES)
    return lambda: hud_tracker(config.SCREENSHOT_PROPS)


def match_zone_statuses(zone):
    statuses = [(status.name, tracker._read_template(status.path)) for status in zone.statuses]

    def take_screenshot():
        for i in range(4):
            screenshot = tracker._take_zone_screenshot(config.SCREENSHOT_PROPS, i, zone)
            yield [tracker._match_statuses(screenshot, statuses)]

    return lambda: list(take_screenshot())

