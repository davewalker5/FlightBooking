import unittest
from tests.helpers import create_test_flight, create_test_passenger
from src.flight_booking import DuplicatePassportNumberError


class TestFlightPassengers(unittest.TestCase):
    def setUp(self) -> None:
        self._flight = create_test_flight()
        self._passenger = create_test_passenger()

    def test_can_add_passenger(self):
        passengers = self._flight.passengers
        self.assertEqual(0, len(passengers))

        self._flight.add_passenger(self._passenger)
        passengers = self._flight.passengers
        self.assertEqual(1, len(passengers))

    def test_can_get_passengers(self):
        self._flight.add_passenger(self._passenger)
        passengers = self._flight.passengers
        self.assertEqual(len(passengers), 1)

        first = list(passengers.values())[0]
        self.assertEqual(first["name"], "Some Passenger")

    def test_cannot_add_passenger_twice(self):
        with self.assertRaises(ValueError):
            self._flight.add_passenger(self._passenger)
            self._flight.add_passenger(self._passenger)

    def test_cannot_add_passenger_with_duplicate_passport(self):
        self._flight.add_passenger(self._passenger)
        passenger = create_test_passenger()
        passenger["passport_number"] = self._passenger["passport_number"]
        with self.assertRaises(DuplicatePassportNumberError):
            self._flight.add_passenger(passenger)

    def test_can_remove_existing_passenger(self):
        self._flight.add_passenger(self._passenger)
        self._flight.remove_passenger(self._passenger["id"])
        self.assertEqual(0, len(self._flight.passengers))
