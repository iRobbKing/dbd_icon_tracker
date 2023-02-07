import hud_tracker
import capture


def main():
    with capture.WinAPI('DeadByDaylight') as capturer:
        while True:
            hud_tracker.show_survivor_portraits(capturer.get_screenshot)


if __name__ == '__main__':
    main()
