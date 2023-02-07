# DBD HUD Tracker
Python library for getting the game information by using HUD recognition.

# Code Example
```py
import dbd_icon_tracker as dit


def main():
    with dit.WinAPI('DeadByDaylight') as capture:
        while True:
            print(dit.get_survivor_statuses(capture))


if __name__ == '__main__':
    main()
```
