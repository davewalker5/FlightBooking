import unittest
from unittest.mock import patch
from src.booking_app.data_entry import input_passenger


class TestInputPassenger(unittest.TestCase):
    @patch("builtins.input", side_effect=["Some Passenger", "M", "01/02/1970", "England", "UK", "1234567890"])
    def test_full_passenger_details_entry(self, _):
        passenger = input_passenger()
        self.assertEqual("Some Passenger", passenger["name"])
        self.assertEqual("M", passenger["gender"])
        self.assertEqual("19700201", passenger["dob"])
        self.assertEqual("England", passenger["nationality"])
        self.assertEqual("UK", passenger["residency"])
        self.assertEqual("1234567890", passenger["passport_number"])

    @patch("builtins.input", side_effect=[""])
    def test_cancel_on_name(self, _):
        passenger = input_passenger()
        self.assertIsNone(passenger)

    @patch("builtins.input", side_effect=["Some Passenger", ""])
    def test_cancel_on_gender(self, _):
        passenger = input_passenger()
        self.assertIsNone(passenger)

    @patch("builtins.input", side_effect=["Some Passenger", "M", ""])
    def test_cancel_on_dob(self, _):
        passenger = input_passenger()
        self.assertIsNone(passenger)

    @patch("builtins.input", side_effect=["Some Passenger", "M", "01/02/1970", ""])
    def test_cancel_on_nationality(self, _):
        passenger = input_passenger()
        self.assertIsNone(passenger)

    @patch("builtins.input", side_effect=["Some Passenger", "M", "01/02/1970", "England", ""])
    def test_cancel_on_residency(self, _):
        passenger = input_passenger()
        self.assertIsNone(passenger)

    @patch("builtins.input", side_effect=["Some Passenger", "M", "01/02/1970", "England", "UK", ""])
    def test_cancel_on_passport_number(self, _):
        passenger = input_passenger()
        self.assertIsNone(passenger)
