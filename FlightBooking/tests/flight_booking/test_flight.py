import os.path
import unittest
from unittest.mock import patch
import datetime
import json
from random import randint
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
    def create_named_passenger(self):
        """
        Helper method to create a passenger
        """
        self._base_passport_number += 1
        return create_passenger("Some Passenger",
                                "M",
                                datetime.datetime(1980, 1, 1),
                                "United Kingdom",
                                "United Kingdom",
                                str(self._base_passport_number).zfill(6))

    def fill_flight(self):
        """
        Helper method to fill the flight
        """
        for _ in range(self._flight.capacity):
            passenger = self.create_named_passenger()
            self._flight.add_passenger(passenger)
            self._flight.allocate_next_empty_seat(passenger["id"])

    def setUp(self) -> None:
        # Create a flight for testing
        self._flight = Flight(
            airline="EasyJet",
            number="U28549",
            embarkation="LGW",
            destination="RMU",
            departs=datetime.datetime(2021, 11, 20, 10, 45, 0),
            duration=datetime.timedelta(hours=2, minutes=35)
        )

        # Create a passenger for testing
        self._base_passport_number = randint(1, 100000)
        self._passenger = self.create_named_passenger()

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

    def test_add_passenger(self):
        passengers = self._flight.passengers
        self.assertEqual(0, len(passengers))

        self._flight.add_passenger(self._passenger)
        passengers = self._flight.passengers
        self.assertEqual(1, len(passengers))

    def test_cannot_add_passenger_twice(self):
        with self.assertRaises(ValueError):
            self._flight.add_passenger(self._passenger)
            self._flight.add_passenger(self._passenger)

    def test_cannot_add_passenger_with_duplicate_passport(self):
        self._flight.add_passenger(self._passenger)
        passenger = self.create_named_passenger()
        passenger["passport_number"] = self._passenger["passport_number"]
        with self.assertRaises(ValueError):
            self._flight.add_passenger(passenger)

    def test_flight_with_no_plan_has_0_capacity(self):
        self.assertIsNone(self._flight.seating_plan)
        self.assertEqual(0, self._flight.capacity)

    def test_load_seating(self):
        self._flight.load_seating("A321", "neo")
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual(235, self._flight.capacity)

    def test_allocate_seat(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        pid = self._passenger["id"]
        self.assertIsNone(self._flight.get_allocated_seat(pid))

        self._flight.allocate_seat("5D", pid)
        self.assertEqual("5D", self._flight.get_allocated_seat(pid))

    def test_allocate_next_seat(self):
        self._flight.load_seating("A321", "neo")
        expected = ["1A", "1B", "1C", "2A", "2B"]
        for i in range(5):
            passenger = self.create_named_passenger()
            self._flight.add_passenger(passenger)
            self._flight.allocate_next_empty_seat(passenger["id"])
            self.assertEqual(expected[i], self._flight.get_allocated_seat(passenger["id"]))

    def test_can_fill_the_flight(self):
        self._flight.load_seating("A321", "neo")
        self.fill_flight()
        self.assertEqual(self._flight.capacity, len(self._flight.passengers))

    def test_cannot_add_passenger_to_a_full_flight(self):
        self._flight.load_seating("A321", "neo")
        self.fill_flight()
        with self.assertRaises(ValueError):
            passenger = self.create_named_passenger()
            self._flight.add_passenger(passenger)

    def test_cannot_allocate_seat_to_missing_passenger(self):
        with self.assertRaises(ValueError):
            self._flight.allocate_seat("1A", "not_on_the_flight")

    def test_move_passenger(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)

        pid = self._passenger["id"]
        self._flight.allocate_seat("5D", pid)
        self.assertEqual("5D", self._flight.get_allocated_seat(pid))

        pid = self._passenger["id"]
        self._flight.allocate_seat("7F", pid)
        self.assertEqual("7F", self._flight.get_allocated_seat(pid))

    def test_reload_seating_plan(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)

        pid = self._passenger["id"]
        self._flight.allocate_seat("5D", pid)

        self._flight.load_seating("A320", "1")
        self.assertEqual("5D", self._flight.get_allocated_seat(pid))

    def test_reload_seating_plan_with_no_allocations(self):
        self._flight.load_seating("A320", "1")
        self.assertEqual(186, self._flight.capacity)
        self._flight.load_seating("A321", "neo")
        self.assertEqual(235, self._flight.capacity)

    def test_cannot_load_plan_with_insufficient_seats(self):
        self._flight.load_seating("A321", "neo")
        self.fill_flight()
        with self.assertRaises(ValueError):
            self._flight.load_seating("A320", "1")

    def test_get_passengers(self):
        self._flight.add_passenger(self._passenger)
        passengers = self._flight.passengers
        self.assertEqual(len(passengers), 1)

        first = list(passengers.values())[0]
        self.assertEqual(first["name"], "Some Passenger")

    def test_get_seating_plan(self):
        self._flight.load_seating("A321", "neo")
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual(235, self._flight.capacity)

    def test_to_json(self):
        json_data = self._flight.to_json()
        loaded = json.loads(json_data)
        self.assertEqual(loaded["details"]["number"], "U28549")

    def test_save(self):
        file_path = get_flight_file_path(self._flight.number, self._flight.departure_date)
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
        self.assertEqual("5D", flight.get_allocated_seat(self._passenger["id"]))

        self.assertIsNotNone(flight.passengers)
        self.assertTrue(self._passenger["id"] in flight.passengers)
        passenger = flight.passengers[self._passenger["id"]]
        self.assertEqual(self._passenger, passenger)

    def test_get_details(self):
        details = "\n".join(self._flight.printable_details)
        expected = ["EasyJet", "U28549", "LGW", "RMU", "2021-11-20 10:45:00", "2:35:00"]
        for value in expected:
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
        self.assertIn("02:20 PM", contents)
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
        self.assertIn("02:20 PM", contents)
        self.assertIn("Some Passenger", contents)
