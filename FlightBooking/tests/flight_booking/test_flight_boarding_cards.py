import os.path
import unittest
from unittest.mock import patch
import datetime
from src.flight_booking.utils import get_boarding_card_path
from .helpers import create_test_flight, create_test_passenger


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


class TestFlightBoardingCards(unittest.TestCase):
    def setUp(self) -> None:
        self._flight = create_test_flight()
        self._passenger = create_test_passenger()

    @patch("src.flight_booking.flight.card_generator_map", {"txt": card_generator})
    def test_can_generate_boarding_cards(self):
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
    def test_can_generate_binary_boarding_cards(self):
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
