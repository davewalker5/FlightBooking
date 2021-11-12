import unittest
from unittest.mock import patch
from src.flight_booking.data_entry import input_gender


class TestInputGender(unittest.TestCase):
    @patch("builtins.input", side_effect=["M"])
    def test_input_male(self, _):
        gender = input_gender()
        self.assertEqual("M", gender)

    @patch("builtins.input", side_effect=["F"])
    def test_input_female(self, _):
        gender = input_gender()
        self.assertEqual("F", gender)

    @patch("builtins.input", side_effect=["m"])
    def test_gender_is_uppercase(self, _):
        gender = input_gender()
        self.assertEqual("M", gender)

    @patch("builtins.input", side_effect=["    m    "])
    def test_whitespace_is_trimmed(self, _):
        gender = input_gender()
        self.assertEqual("M", gender)

    @patch("builtins.input", side_effect=["a", "b", "c", "d", "m"])
    def test_invalid_prompts_until_correct(self, _):
        gender = input_gender()
        self.assertEqual("M", gender)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        gender = input_gender()
        self.assertIsNone(gender)
