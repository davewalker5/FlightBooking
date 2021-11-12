import unittest
from datetime import timedelta
from unittest.mock import patch
from src.booking_app.data_entry import input_duration


class TestInputDuration(unittest.TestCase):
    @patch("builtins.input", side_effect=["2:45"])
    def test_valid_duration(self, _):
        duration = input_duration()
        self.assertTrue(isinstance(duration, timedelta))
        self.assertEqual(9900, duration.seconds)

    @patch("builtins.input", side_effect=["0:59"])
    def test_zero_hours_passes(self, _):
        duration = input_duration()
        self.assertTrue(isinstance(duration, timedelta))
        self.assertEqual(3540, duration.seconds)

    @patch("builtins.input", side_effect=["-1:00"])
    def test_negative_hours_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=["1:60"])
    def test_more_than_59_minutes_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=["0:-1"])
    def test_negative_minutes_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=["0:0"])
    def test_zero_duration_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=["03:56:56"])
    def test_string_with_too_many_words_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=["03"])
    def test_string_with_not_enough_words_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=["1.5:30"])
    def test_string_with_non_integer_hours_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=["1:30.5"])
    def test_string_with_non_integer_minutes_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=["AB:30"])
    def test_string_with_non_numeric_hours_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=["1:AB"])
    def test_string_with_non_numeric_minutes_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_duration()

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        duration = input_duration()
        self.assertIsNone(duration)
