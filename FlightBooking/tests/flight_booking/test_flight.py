import unittest
import datetime
import pytz
from src.flight_booking import Flight
from tests.helpers import create_test_flight


class TestFlight(unittest.TestCase):
    def test_can_create_flight(self):
        flight = create_test_flight()
        self.assertEqual("LGW", flight.embarkation_airport_code)
        self.assertEqual("RMU", flight.destination_airport_code)
        self.assertEqual("EasyJet", flight.airline)
        self.assertEqual("U28549", flight.number)
        self.assertEqual("20/11/2021", flight.departs_localtime.strftime("%d/%m/%Y"))
        self.assertEqual((2, 35), flight.duration)

    def test_can_create_flight_with_timezone_aware_departure(self):
        flight = Flight(
            airline="EasyJet",
            number="U28549",
            embarkation="LGW",
            destination="RMU",
            departs=datetime.datetime(2021, 11, 20, 10, 45, 0, tzinfo=pytz.timezone("Europe/London")),
            duration=datetime.timedelta(hours=2, minutes=30)
        )

        self.assertEqual("20/11/2021", flight.departs_localtime.strftime("%d/%m/%Y"))

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
