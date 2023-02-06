import bot
import capture
import tracker


api = capture.WinAPI('DeadByDaylight')
track =  tracker.Tracker(api)
dbd = bot.DbdHudTracker(track)

while True:
    print(dbd.get_survivors_states())
    dbd.show()