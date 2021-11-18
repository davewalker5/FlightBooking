import os.path
import unittest
from unittest.mock import patch
from src.flight_booking import InvalidOperationError, MissingBoardingCardPluginError
from tests.helpers import create_test_flight, \
    create_test_passenger, \
    text_card_generator, \
    binary_card_generator, \
    get_flight_boarding_card_file_path


class TestFlightBoardingCards(unittest.TestCase):
    def setUp(self) -> None:
        self._flight = create_test_flight()
        self._passenger = create_test_passenger()

    @patch("src.flight_booking.flight.card_generator_map", {"txt": text_card_generator})
    def test_can_generate_boarding_cards(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        self._flight.allocate_seat("5D", self._passenger["id"])
        self._flight.generate_boarding_cards("txt", "28A")

        # Boarding card text file should exist
        boarding_card_file = get_flight_boarding_card_file_path(self._flight, "5D", "txt")
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
    def test_can_generate_binary_boarding_cards(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        self._flight.allocate_seat("5D", self._passenger["id"])
        self._flight.generate_boarding_cards("dat", "28A")

        # Boarding card data file should exist
        boarding_card_file = get_flight_boarding_card_file_path(self._flight, "5D", "dat")
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

    def test_cannot_generate_boarding_cards_with_missing_gate(self):
        with self.assertRaises(ValueError):
            self._flight.generate_boarding_cards("txt", None)

    def test_cannot_generate_boarding_cards_with_blank_gate(self):
        with self.assertRaises(ValueError):
            self._flight.generate_boarding_cards("txt", "")

    @patch("src.flight_booking.flight.card_generator_map", {"txt": text_card_generator})
    def test_cannot_generate_boarding_cards_with_no_seating_plan(self):
        with self.assertRaises(InvalidOperationError):
            self._flight.generate_boarding_cards("txt", "2A")

    @patch("src.flight_booking.flight.card_generator_map", {"txt": text_card_generator})
    def test_cannot_generate_boarding_cards_with_no_passengers(self):
        self._flight.load_seating("A321", "neo")
        with self.assertRaises(InvalidOperationError):
            self._flight.generate_boarding_cards("txt", "2A")

    @patch("src.flight_booking.flight.card_generator_map", {"txt": text_card_generator})
    def test_cannot_generate_boarding_cards_with_no_seat_allocations(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        with self.assertRaises(InvalidOperationError):
            self._flight.generate_boarding_cards("txt", "2A")

    def test_cannot_generate_boarding_cards_when_plugin_is_missing(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        self._flight.allocate_seat("5D", self._passenger["id"])
        with self.assertRaises(MissingBoardingCardPluginError):
            self._flight.generate_boarding_cards("missing-format", "28A")
