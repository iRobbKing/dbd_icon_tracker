import os

from vision import take_screenshot_grey, read_template, match


def _get_status_templates(folder, template_paths):
    for status, template_path in template_paths.items():
        full_path = os.path.join(folder, template_path)
        yield status, read_template(full_path)


def get_status_templates(folder, template_paths):
    return dict(_get_status_templates(folder, template_paths))


def _take_survivor_portrait_screenshot(survivor_index, survivor_portrait, next_survivor_offset):
    x, y, w, h = survivor_portrait
    y += next_survivor_offset * survivor_index
    return take_screenshot_grey(x, y, w, h)


def _take_survivor_action_screenshot(survivor_index, survivor_portrait, next_survivor_offset, action_offset, action_size):
    x, y, _, _ = survivor_portrait
    y += next_survivor_offset * survivor_index

    x_offset, y_offset = action_offset
    x += x_offset
    y += y_offset

    w, h = action_size

    return take_screenshot_grey(x, y, w, h)


def _read_survivor_status(templates, screenshot):
    for state, template in templates.items():
        if match(screenshot, template, .6):
            return state


def read_survivor_state(coordinates, templates, survivor_index):
    screenshot = _take_survivor_portrait_screenshot(survivor_index, **coordinates)
    return _read_survivor_status(templates, screenshot)


def read_survivor_action(coordinates, templates, survivor_index):
    screenshot = _take_survivor_action_screenshot(survivor_index, **coordinates)
    return _read_survivor_status(templates, screenshot)
