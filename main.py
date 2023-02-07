import capture
import config
import dbdhudtracker as dht
import tracker


def main():
    api = capture.WinAPI('DeadByDaylight')
    track = tracker.Tracker(api, config.DEFAULT)
    dbd = dht.DbdHudTracker(track)

    while True:
        dbd.show(250)


if __name__ == '__main__':
    main()
