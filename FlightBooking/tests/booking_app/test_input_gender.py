import unittest
from unittest.mock import patch
from src.booking_app.data_entry import input_gender


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

    @patch("builtins.input", side_effect=["a"])
    def test_invalid_gender_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_gender()

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        gender = input_gender()
        self.assertIsNone(gender)
