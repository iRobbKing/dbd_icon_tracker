import vision


def debug_show(tracker, delay):
    def map_status_name(name):
        return name if name is not None else 'unknown'

    def map_survivor_statuses(statuses):
        return ', '.join((f'{map_status_name(status_name)}: {status_value}'
                          for status in statuses
                          for status_name, status_value in status.items()))

    statuses = tracker.get_survivor_statuses()

    print([map_survivor_statuses(status) for status in statuses])

    for i, survivor in enumerate(statuses):
        img = tracker.get_survivor_screenshot(i)
        vision.set_window_name(f's{i}', f's{i} - {survivor}')
        vision.show_image_in_window(f's{i}', img)

    vision.wait(delay)

