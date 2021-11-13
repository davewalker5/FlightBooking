import unittest
import datetime
from src.flight_booking import Flight


class TestFlight(unittest.TestCase):
    def test_cannot_create_flight_with_invalid_airport_code(self):
        with self.assertRaises(KeyError):
            Flight(
                airline="EasyJet",
                number="U28549",
                embarkation="DODGY",
                destination="RMU",
                departs=datetime.datetime(2021, 11, 20, 10, 45, 0),
                duration=datetime.timedelta(hours=2, minutes=30)
            )
