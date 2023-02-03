import vision

def _read_template(path):
    return vision.make_grey(vision.read_picture_from_file(path))


def _take_screenshot(x, y, w, h, hwnd=None):
    return vision.make_grey(vision.take_screenshot(x, y, w, h, hwnd))


def read_status_templates(statuses):
    def add_template_to_status(status):
        status['template'] = _read_template(status['template'])
        return status

    return {status_name: add_template_to_status(status_props) for status_name, status_props in statuses.items()}


def take_zone_screenshot(survivor_index, screenshot_props, zone):
    x, y = screenshot_props.top_left

    w, h = zone['size']
    offset_x, offset_y = zone['offset']

    x += offset_x
    y += screenshot_props.next_offset * survivor_index + offset_y

    return _take_screenshot(x, y, w, h)


def match_survivor_status(status: dict, screenshot):
    return vision.match(screenshot, status['template'], status.setdefault('threshold', .6))
