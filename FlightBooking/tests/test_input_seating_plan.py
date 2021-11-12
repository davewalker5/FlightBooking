import unittest
import datetime
from unittest.mock import patch
from src.flight_booking.flight import Flight
from src.flight_booking.data_entry import input_aircraft


class TestInputSeatingPlan(unittest.TestCase):
    """
    Seating plans are read from files and can't be monkeypatched, so the tests in this class
    rely on the seating plan files being present in the appropriate data subfolder
    """
    def setUp(self) -> None:
        self._flight = Flight("LGW",
                              "RMU",
                              "EasyJet",
                              "EZY8549",
                              datetime.datetime(2021, 11, 20, 10, 15),
                              datetime.timedelta(hours=2, minutes=25))

    @patch("builtins.input", side_effect=["A320:1"])
    def test_valid_seating_plan_with_layout(self, _):
        input_aircraft(self._flight)
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual("A320", self._flight.aircraft)
        self.assertEqual("1", self._flight.layout)
        self.assertEqual(186, self._flight.capacity)

    @patch("builtins.input", side_effect=["A320"])
    def test_valid_seating_plan_with_no_layout(self, _):
        input_aircraft(self._flight)
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual("A320", self._flight.aircraft)
        self.assertEqual(None, self._flight.layout)
        self.assertEqual(186, self._flight.capacity)

    @patch("builtins.input", side_effect=["  A320  :  1  "])
    def test_leading_trailing_whitespace_is_ignored(self, _):
        input_aircraft(self._flight)
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual("A320", self._flight.aircraft)
        self.assertEqual("1", self._flight.layout)
        self.assertEqual(186, self._flight.capacity)

    @patch("builtins.input", side_effect=["A380", "747", "787-10", "737", "A320:1"])
    def test_invalid_plan_prompts_until_correct(self, _):
        input_aircraft(self._flight)
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual("A320", self._flight.aircraft)
        self.assertEqual("1", self._flight.layout)
        self.assertEqual(186, self._flight.capacity)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        input_aircraft(self._flight)
