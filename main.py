import dbdhudtracker as dht

api = dht.WinAPI('DeadByDaylight')
track = dht.Tracker(api, dht.config.DEFAULT)
dbd = dht.DbdHudTracker(track)

while True:
    print(dbd.get_survivor_statuses())
    dbd.show()
