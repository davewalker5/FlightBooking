import unittest
from datetime import date
from unittest.mock import patch
from src.flight_booking.data_entry import input_departure_date


class TestInputDepartureDate(unittest.TestCase):
    @patch("builtins.input", side_effect=["01/02/2021"])
    def test_valid_date(self, _):
        departure_date = input_departure_date()
        self.assertTrue(isinstance(departure_date, date))
        self.assertEqual(1, departure_date.day)
        self.assertEqual(2, departure_date.month)
        self.assertEqual(2021, departure_date.year)

    @patch("builtins.input", side_effect=["01/13/2021", "Not a Date", "01/02/2021"])
    def test_invalid_date_string_prompts_until_correct(self, _):
        departure_date = input_departure_date()
        self.assertTrue(isinstance(departure_date, date))
        self.assertEqual(1, departure_date.day)
        self.assertEqual(2, departure_date.month)
        self.assertEqual(2021, departure_date.year)

    @patch("builtins.input", side_effect=["  01/02/2021  "])
    def test_leading_trailing_whitespace_is_ignored(self, _):
        departure_date = input_departure_date()
        self.assertTrue(isinstance(departure_date, date))
        self.assertEqual(1, departure_date.day)
        self.assertEqual(2, departure_date.month)
        self.assertEqual(2021, departure_date.year)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        departure_date = input_departure_date()
        self.assertIsNone(departure_date)
