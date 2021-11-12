import unittest
from datetime import time
from unittest.mock import patch
from src.flight_booking.data_entry import input_departure_time


class TestInputDepartureTime(unittest.TestCase):
    @patch("builtins.input", side_effect=["13:45"])
    def test_valid_time(self, _):
        departure_time = input_departure_time()
        self.assertTrue(isinstance(departure_time, time))
        self.assertEqual(13, departure_time.hour)
        self.assertEqual(45, departure_time.minute)
        self.assertEqual(0, departure_time.second)

    @patch("builtins.input", side_effect=["13:67", "46:45", "Not a time", "13:45"])
    def test_invalid_time_string_prompts_until_correct(self, _):
        departure_time = input_departure_time()
        self.assertTrue(isinstance(departure_time, time))
        self.assertEqual(13, departure_time.hour)
        self.assertEqual(45, departure_time.minute)
        self.assertEqual(0, departure_time.second)

    @patch("builtins.input", side_effect=["  13:45  "])
    def test_leading_trailing_whitespace_is_ignored(self, _):
        departure_time = input_departure_time()
        self.assertTrue(isinstance(departure_time, time))
        self.assertEqual(13, departure_time.hour)
        self.assertEqual(45, departure_time.minute)
        self.assertEqual(0, departure_time.second)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        departure_time = input_departure_time()
        self.assertIsNone(departure_time)
