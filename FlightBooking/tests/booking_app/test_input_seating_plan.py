import unittest
from unittest.mock import patch
from src.flight_booking import SeatingPlanNotFoundError
from tests.helpers import create_test_flight
from src.booking_app.data_entry import input_aircraft_seating_plan
from src.booking_app.exceptions import InvalidAircraftSeatingPlanError


class TestInputSeatingPlan(unittest.TestCase):
    """
    Seating plans are read from files and can't be monkeypatched, so the tests in this class
    rely on the seating plan files being present in the appropriate data subfolder
    """
    def setUp(self) -> None:
        self._flight = create_test_flight()

    @patch("builtins.input", side_effect=["A320:1"])
    def test_valid_seating_plan_with_layout(self, _):
        input_aircraft_seating_plan(self._flight)
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual("A320", self._flight.aircraft)
        self.assertEqual("1", self._flight.layout)
        self.assertEqual(186, self._flight.capacity)

    @patch("builtins.input", side_effect=["A320"])
    def test_valid_seating_plan_with_no_layout(self, _):
        input_aircraft_seating_plan(self._flight)
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual("A320", self._flight.aircraft)
        self.assertEqual(None, self._flight.layout)
        self.assertEqual(186, self._flight.capacity)

    @patch("builtins.input", side_effect=["  A320  :  1  "])
    def test_leading_trailing_whitespace_is_ignored(self, _):
        input_aircraft_seating_plan(self._flight)
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual("A320", self._flight.aircraft)
        self.assertEqual("1", self._flight.layout)
        self.assertEqual(186, self._flight.capacity)

    @patch("builtins.input", side_effect=["A380"])
    def test_invalid_aircraft_errors(self, _):
        with self.assertRaises(SeatingPlanNotFoundError):
            input_aircraft_seating_plan(self._flight)

    @patch("builtins.input", side_effect=["A320:2"])
    def test_invalid_layout_for_valid_aircraft_errors(self, _):
        with self.assertRaises(SeatingPlanNotFoundError):
            input_aircraft_seating_plan(self._flight)

    @patch("builtins.input", side_effect=["A320:1:2"])
    def test_badly_formatted_seating_plan_errors(self, _):
        with self.assertRaises(InvalidAircraftSeatingPlanError):
            input_aircraft_seating_plan(self._flight)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        input_aircraft_seating_plan(self._flight)
        self.assertIsNone(self._flight.seating_plan)
