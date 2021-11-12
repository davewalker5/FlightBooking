"""
https://www.timeanddate.com/time/zone/
"""
from datetime import datetime, timedelta
import pytz

# Departure time
departs_unaware = datetime(2021, 10, 15, 12, 20, 0)
departs = pytz.timezone("Europe/London").localize(departs_unaware)
departs_utc = departs.astimezone(pytz.utc)
print(departs)
print(departs_utc)

# Arrival time
duration = timedelta(hours=2, minutes=35)
arrives_utc = departs_utc + duration
arrival_timezone = pytz.timezone("Europe/Madrid")
arrives = arrives_utc.astimezone(arrival_timezone)
print(arrives)
print(arrives_utc)
