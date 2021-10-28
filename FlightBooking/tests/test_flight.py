import os.path
import unittest
from unittest.mock import patch
import datetime
import json
from src.flight_booking import *
from src.flight_booking.utils import get_flight_file_path, get_boarding_card_path


def card_generator(card_details):
    """
    Stub card generator monkeypatched into the flight module for testing
    boarding card printing

    :param card_details: Boarding card details
    """
    return "\n".join(card_details.values())


def binary_card_generator(card_details):
    """
    Stub card generator monkeypatched into the flight module for testing
    boarding card printing

    :param card_details: Boarding card details
    """
    return "\n".join(card_details.values()).encode("utf-8")


class TestFlight(unittest.TestCase):
    def setUp(self) -> None:
        # Create a flight for testing
        self._flight = Flight(
            airline="EasyJet",
            number="U28549",
            embarkation="LGW",
            destination="RMU",
            departs=datetime.datetime(2021, 11, 20, 10, 45, 0),
            duration=datetime.timedelta(hours=2, minutes=0)
        )

        # Create a passenger for testing
        self._passenger = create_passenger(
            "Some Passenger",
            "M",
            datetime.datetime(1980, 1, 1),
            "United Kingdom",
            "United Kingdom",
            "123456789")

    def test_create_flight_with_invalid_airport_code(self):
        with self.assertRaises(ValueError):
            Flight(embarkation="DODGY")

    def test_load_seating(self):
        self.assertIsNone(self._flight.seating_plan)
        self.assertEqual(self._flight.capacity, 0)
        self._flight.load_seating("A321", "neo")
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual(self._flight.capacity, 235)

    def test_add_passenger(self):
        passengers = self._flight.passengers
        self.assertEqual(len(passengers), 0)

        self._flight.add_passenger(self._passenger)
        passengers = self._flight.passengers
        self.assertEqual(len(passengers), 1)

    def test_add_passenger_twice(self):
        with self.assertRaises(ValueError):
            self._flight.add_passenger(self._passenger)
            self._flight.add_passenger(self._passenger)

    def test_allocate_seat(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        pid = self._passenger["id"]
        self.assertIsNone(self._flight.get_allocated_seat(pid))

        self._flight.allocate_seat("5D", pid)
        self.assertEqual(self._flight.get_allocated_seat(pid), "5D")

    def test_allocate_seat_to_missing_passenger(self):
        with self.assertRaises(ValueError):
            self._flight.allocate_seat("1A", "not_on_the_flight")

    def test_move_passenger(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)

        pid = self._passenger["id"]
        self._flight.allocate_seat("5D", pid)
        self.assertEqual(self._flight.get_allocated_seat(pid), "5D")

        pid = self._passenger["id"]
        self._flight.allocate_seat("7F", pid)
        self.assertEqual(self._flight.get_allocated_seat(pid), "7F")

    def test_reload_seating_plan(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)

        pid = self._passenger["id"]
        self._flight.allocate_seat("5D", pid)

        self._flight.load_seating("A320", "1")
        self.assertEqual(self._flight.get_allocated_seat(pid), "5D")

    def test_reload_seating_plan_with_no_allocations(self):
        self._flight.load_seating("A320", "1")
        self.assertEqual(self._flight.capacity, 186)
        self._flight.load_seating("A321", "neo")
        self.assertEqual(self._flight.capacity, 235)

    def test_get_passengers(self):
        self._flight.add_passenger(self._passenger)
        passengers = self._flight.passengers
        self.assertEqual(len(passengers), 1)

        first = list(passengers.values())[0]
        self.assertEqual(first["name"], "Some Passenger")

    def test_get_seating_plan(self):
        self._flight.load_seating("A321", "neo")
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual(self._flight.capacity, 235)

    def test_to_json(self):
        json_data = self._flight.to_json()
        loaded = json.loads(json_data)
        self.assertEqual(loaded["details"]["number"], "U28549")

    def test_save(self):
        file_path = get_flight_file_path(self._flight._number, self._flight._departs)
        if os.path.exists(file_path):
            os.remove(file_path)
        self.assertFalse(os.path.exists(file_path))

        self._flight.save()
        self.assertTrue(os.path.exists(file_path))

    def test_load_flight(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        self._flight.allocate_seat("5D", self._passenger["id"])
        self._flight.save()

        flight = Flight.load_flight("U28549", datetime.datetime(2021, 11, 20, 10, 45, 0))
        self.assertEqual(flight._number, "U28549")
        self.assertEqual(len(flight.passengers), 1)
        self.assertIsNotNone(flight.seating_plan)
        self.assertEqual(flight.capacity, 235)
        self.assertEqual(flight.get_allocated_seat(self._passenger["id"]), "5D")

    def test_get_details(self):
        details = "\n".join(self._flight.printable_details)
        expected = ["EasyJet", "U28549", "LGW", "RMU", "2021-11-20 10:45:00", "2:00:00"]
        for value in  expected:
            self.assertTrue(value in details)

    @patch("src.flight_booking.flight.card_generator_map", {"txt": card_generator})
    def test_generate_boarding_cards(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        self._flight.allocate_seat("5D", self._passenger["id"])
        self._flight.generate_boarding_cards("txt", "28A")

        # Boarding card text file should exist
        boarding_card_file = get_boarding_card_path("U28549", "5D", datetime.datetime(2021, 11, 20, 10, 45, 0), "txt")
        self.assertTrue(os.path.exists(boarding_card_file))

        # Boarding card text file should contain each of the flight details
        with open(boarding_card_file, mode="rt", encoding="utf-8") as f:
            contents = f.read()
        os.unlink(boarding_card_file)

        self.assertIn("EasyJet", contents)
        self.assertIn("LGW", contents)
        self.assertIn("10:45 AM", contents)
        self.assertIn("RMU", contents)
        self.assertIn("12:45 PM", contents)
        self.assertIn("Some Passenger", contents)

    @patch("src.flight_booking.flight.card_generator_map", {"dat": binary_card_generator})
    def test_generate_binary_boarding_cards(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        self._flight.allocate_seat("5D", self._passenger["id"])
        self._flight.generate_boarding_cards("dat", "28A")

        # Boarding card data file should exist
        boarding_card_file = get_boarding_card_path("U28549", "5D", datetime.datetime(2021, 11, 20, 10, 45, 0), "dat")
        self.assertTrue(os.path.exists(boarding_card_file))

        # Boarding card text file should contain each of the flight details
        with open(boarding_card_file, mode="rb") as f:
            contents = f.read().decode("utf-8")
        os.unlink(boarding_card_file)

        self.assertIn("EasyJet", contents)
        self.assertIn("LGW", contents)
        self.assertIn("10:45 AM", contents)
        self.assertIn("RMU", contents)
        self.assertIn("12:45 PM", contents)
        self.assertIn("Some Passenger", contents)
