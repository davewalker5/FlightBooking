import unittest
from unittest.mock import patch
from src.flight_booking.data_entry import input_airport_code


class TestInputAirport(unittest.TestCase):
    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"}})
    @patch("builtins.input", side_effect=["LGW"])
    def test_input_valid_airport_code(self, _):
        airport = input_airport_code("Embarkation")
        self.assertEqual("LGW", airport["code"])

    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"}})
    @patch("builtins.input", side_effect=["LHR", "JFK", "RMU", "ALC", "ORD", "LGW"])
    def test_input_invalid_airport_code_prompts_until_correct(self, _):
        airport = input_airport_code("Embarkation")
        self.assertEqual("LGW", airport["code"])

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        airport = input_airport_code("Embarkation")
        self.assertIsNone(airport)

    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"}})
    @patch("builtins.input", side_effect=["  LGW  "])
    def test_leading_trailing_whitespace_is_ignored(self, _):
        airport = input_airport_code("Embarkation")
        self.assertEqual("LGW", airport["code"])
