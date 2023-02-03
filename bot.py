import itertools

import config
import tracker


def prepare_templates():
    return tracker.read_status_templates(config.STATUSES)


def _match_survivor_status(statuses, survivor_index):
    grouped_by_zone = itertools.groupby(statuses.items(), lambda status: status[1]['zone'])

    for zone, statuses in grouped_by_zone:
        screenshot = tracker.take_zone_screenshot(
            survivor_index,
            config.SCREENSHOT_PROPS,
            config.SCREENSHOT_ZONES[zone]
        )

        for status_name, status_props in statuses:
            if tracker.match_survivor_status(status_props, screenshot):
                yield zone, status_name
                break
        else:
            yield zone, None


def get_survivors_statuses(statuses):
    for i in range(4):
        yield dict(_match_survivor_status(statuses, i))
