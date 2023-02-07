# DBD HUD Tracker
Python library for getting the game information by using HUD recognition.

# Code Example
```py
import dbd_icon_tracker as dit


def main():
    with dit.WinAPI('DeadByDaylight') as capturer:
        while True:
            print(capturer.get_screenshot)


if __name__ == '__main__':
    main()
```
