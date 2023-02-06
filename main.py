import bot
import time
dbd = bot.DbdHudTracker()


x = dbd.match_survivors_state()

while True:
    print(x())
    time.sleep(1)