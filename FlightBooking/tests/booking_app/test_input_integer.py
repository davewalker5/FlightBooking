import unittest
from unittest.mock import patch
from src.booking_app.data_entry import input_integer


class TestInputInteger(unittest.TestCase):
    @patch("builtins.input", side_effect=["2871765"])
    def test_can_enter_valid_integer(self, _):
        i = input_integer("")
        self.assertEqual(2871765, i)

    @patch("builtins.input", side_effect=["2871765"])
    def test_can_enter_integer_equal_to_minimum(self, _):
        i = input_integer("", minimum=2871765)
        self.assertEqual(2871765, i)

    @patch("builtins.input", side_effect=["2871766"])
    def test_can_enter_integer_greater_than_minimum(self, _):
        i = input_integer("", minimum=2871765)
        self.assertEqual(2871766, i)

    @patch("builtins.input", side_effect=["2871764"])
    def test_cannot_enter_integer_less_than_minimum(self, _):
        with self.assertRaises(ValueError):
            _ = input_integer("", minimum=2871765)

    @patch("builtins.input", side_effect=["2871765"])
    def test_can_enter_integer_equal_to_maximum(self, _):
        i = input_integer("", maximum=2871765)
        self.assertEqual(2871765, i)

    @patch("builtins.input", side_effect=["2871764"])
    def test_can_enter_integer_less_than_maximum(self, _):
        i = input_integer("", maximum=2871765)
        self.assertEqual(2871764, i)

    @patch("builtins.input", side_effect=["2871766"])
    def test_cannot_enter_integer_greater_than_maximum(self, _):
        with self.assertRaises(ValueError):
            _ = input_integer("", maximum=2871765)

    @patch("builtins.input", side_effect=["2871765"])
    def test_can_enter_integer_in_range(self, _):
        i = input_integer("", minimum=2871764, maximum=2871766)
        self.assertEqual(2871765, i)

    @patch("builtins.input", side_effect=["2871765"])
    def test_can_enter_integer_in_range_of_one(self, _):
        i = input_integer("", minimum=2871765, maximum=2871765)
        self.assertEqual(2871765, i)
