import unittest
from datetime import timedelta
from unittest.mock import patch
from src.flight_booking.data_entry import input_duration


class TestInputDuration(unittest.TestCase):
    @patch("builtins.input", side_effect=["2:45"])
    def test_valid_duration(self, _):
        duration = input_duration()
        self.assertTrue(isinstance(duration, timedelta))
        self.assertEqual(9900, duration.seconds)

    @patch("builtins.input", side_effect=["03:56:56", "This is:not valid", "2:45"])
    def test_invalid_duration_prompts_until_correct(self, _):
        duration = input_duration()
        self.assertTrue(isinstance(duration, timedelta))
        self.assertEqual(9900, duration.seconds)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        duration = input_duration()
        self.assertIsNone(duration)
