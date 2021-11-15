import unittest
from unittest.mock import patch
from src.booking_app.data_entry import input_airport_code
from src.booking_app.exceptions import InvalidAirportCodeError


class TestInputAirport(unittest.TestCase):
    @patch("flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"}})
    @patch("builtins.input", side_effect=["LGW"])
    def test_input_valid_airport_code(self, _):
        airport = input_airport_code("Embarkation")
        self.assertEqual("LGW", airport["code"])

    @patch("flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"}})
    @patch("builtins.input", side_effect=["LHR"])
    def test_input_invalid_airport_code_errors(self, _):
        with self.assertRaises(InvalidAirportCodeError):
            _ = input_airport_code("Embarkation")

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        airport = input_airport_code("Embarkation")
        self.assertIsNone(airport)

    @patch("flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"}})
    @patch("builtins.input", side_effect=["  LGW  "])
    def test_leading_trailing_whitespace_is_ignored(self, _):
        airport = input_airport_code("Embarkation")
        self.assertEqual("LGW", airport["code"])
