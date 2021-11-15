import unittest
import datetime
from unittest.mock import patch
from src.booking_app.data_entry import input_date, input_past_date, input_future_date


class TestInputUtils(unittest.TestCase):
    @patch("builtins.input", side_effect=[datetime.datetime.now().strftime("%d/%m/%Y")])
    def test_now_is_a_valid_date(self, _):
        # This is potentially vulnerable to failure if the test starts at midnight and we're now in
        # the next day ... choosing to treat this as an unlikely edge case
        now = datetime.datetime.now().date()
        d = input_date("")
        self.assertTrue(isinstance(d, datetime.date))
        self.assertEqual(now.day, d.day)
        self.assertEqual(now.month, d.month)
        self.assertEqual(now.year, d.year)

    @patch("builtins.input", side_effect=["01/02/1970"])
    def test_historical_date_is_valid(self, _):
        d = input_date("")
        self.assertTrue(isinstance(d, datetime.date))
        self.assertEqual(1, d.day)
        self.assertEqual(2, d.month)
        self.assertEqual(1970, d.year)

    @patch("builtins.input", side_effect=["01/02/9999"])
    def test_future_date_is_valid(self, _):
        d = input_date("")
        self.assertTrue(isinstance(d, datetime.date))
        self.assertEqual(1, d.day)
        self.assertEqual(2, d.month)
        self.assertEqual(9999, d.year)

    @patch("builtins.input", side_effect=["  01/02/2021  "])
    def test_leading_trailing_whitespace_is_ignored(self, _):
        d = input_date("")
        self.assertTrue(isinstance(d, datetime.date))
        self.assertEqual(1, d.day)
        self.assertEqual(2, d.month)
        self.assertEqual(2021, d.year)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        d = input_date("")
        self.assertIsNone(d)

    @patch("builtins.input", side_effect=["This is not a date"])
    def test_invalid_date_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_date("")

    @patch("builtins.input", side_effect=[datetime.datetime.now().strftime("%d/%m/%Y")])
    def test_now_is_not_a_valid_past_date(self, _):
        # This is potentially vulnerable to failure if the test starts at midnight and we're now in
        # the next day ... choosing to treat this as an unlikely edge case
        with self.assertRaises(ValueError):
            _ = input_past_date("")

    @patch("builtins.input", side_effect=["01/02/9999"])
    def test_future_date_is_not_a_valid_past_date(self, _):
        with self.assertRaises(ValueError):
            _ = input_past_date("")

    @patch("builtins.input", side_effect=["01/02/1970"])
    def test_past_date_is_valid_past_date(self, _):
        d = input_past_date("")
        self.assertTrue(isinstance(d, datetime.date))
        self.assertEqual(1, d.day)
        self.assertEqual(2, d.month)
        self.assertEqual(1970, d.year)

    @patch("builtins.input", side_effect=[datetime.datetime.now().strftime("%d/%m/%Y")])
    def test_now_is_not_a_valid_future_date(self, _):
        # This is potentially vulnerable to failure if the test starts at midnight and we're now in
        # the next day ... choosing to treat this as an unlikely edge case
        with self.assertRaises(ValueError):
            _ = input_future_date("")

    @patch("builtins.input", side_effect=["01/02/1970"])
    def test_past_date_is_not_a_valid_future_date(self, _):
        with self.assertRaises(ValueError):
            _ = input_future_date("")

    @patch("builtins.input", side_effect=["01/02/9999"])
    def test_future_date_is_a_valid_future_date(self, _):
        d = input_future_date("")
        self.assertTrue(isinstance(d, datetime.date))
        self.assertEqual(1, d.day)
        self.assertEqual(2, d.month)
        self.assertEqual(9999, d.year)
