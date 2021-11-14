import os.path
import unittest
import datetime
import json
from src.flight_booking import Flight
from src.flight_booking.utils import get_flight_file_path
from .helpers import create_test_flight, create_test_passenger, remove_files


class TestFlightSaveAndLoad(unittest.TestCase):
    def setUp(self) -> None:
        self._flight = create_test_flight()
        self._passenger = create_test_passenger()

    def tearDown(self) -> None:
        # Clear down the flights data folder after the tests have run
        remove_files("flights")

    def test_can_save_flight(self):
        file_path = get_flight_file_path(self._flight.number, self._flight.departure_date)
        if os.path.exists(file_path):
            os.remove(file_path)
        self.assertFalse(os.path.exists(file_path))

        self._flight.save()
        self.assertTrue(os.path.exists(file_path))

    def test_can_reload_flight(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        self._flight.allocate_seat("5D", self._passenger["id"])
        self._flight.save()

        flight = Flight.load_flight("U28549", datetime.datetime(2021, 11, 20, 10, 45, 0))
        self.assertEqual("LGW", flight.embarkation_airport_code)
        self.assertEqual("RMU", flight.destination_airport_code)
        self.assertEqual("EasyJet", flight.airline)
        self.assertEqual("U28549", flight.number)
        self.assertEqual("A321", flight.aircraft)
        self.assertEqual("neo", flight.layout)
        self.assertEqual((2, 35), flight.duration)
        self.assertEqual(1, len(flight.passengers))
        self.assertIsNotNone(flight.seating_plan)
        self.assertEqual(235, flight.capacity)
        self.assertEqual(234, flight.available_capacity)
        self.assertEqual("5D", flight.get_allocated_seat(self._passenger["id"]))

        self.assertIsNotNone(flight.passengers)
        self.assertTrue(self._passenger["id"] in flight.passengers)
        passenger = flight.passengers[self._passenger["id"]]
        self.assertEqual(self._passenger, passenger)

    def test_can_serialize_to_and_from_json(self):
        json_data = self._flight.to_json()
        loaded = json.loads(json_data)
        self.assertEqual(loaded["details"]["number"], "U28549")

    def test_can_get_printable_flight_details(self):
        details = "\n".join(self._flight.printable_details)
        expected = ["EasyJet", "U28549", "LGW", "RMU", "2021-11-20 10:45:00", "2:35:00"]
        for value in expected:
            self.assertTrue(value in details)
