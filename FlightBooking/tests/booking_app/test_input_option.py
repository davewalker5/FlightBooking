import unittest
from unittest.mock import patch
from src.booking_app.option_handler import input_option, call_option_function
from tests.helpers import create_test_flight


def create_flight():
    return create_test_flight()


def dummy_function_1(flight):
    return None


def dummy_function_2(flight):
    return create_flight()


def dummy_function_3():
    return None


def dummy_function_4():
    return create_flight()


class TestInputOption(unittest.TestCase):
    @patch("builtins.input", side_effect=["1"])
    def test_valid_option(self, _):
        selected = input_option({
            "1": {"description": "Test Option", "function": None}
        })
        self.assertEqual("Test Option", selected["description"])
        self.assertIsNone(selected["function"])

    @patch("builtins.input", side_effect=["2"])
    def test_invalid_option_errors(self, _):
        with self.assertRaises(ValueError):
            _ = input_option({
                "1": {"description": "Test Option", "function": None}
            })

    def test_call_function_with_parameters_doesnt_change_flight(self):
        option = {
            "description": "Test Option",
            "has_flight_parameter": True,
            "function": dummy_function_1
        }
        result = call_option_function(option, 10)
        self.assertEqual(10, result)

    def test_call_function_with_parameters_changes_flight(self):
        option = {
            "description": "Test Option",
            "has_flight_parameter": True,
            "function": dummy_function_2
        }
        result = call_option_function(option, create_flight())
        self.assertEqual("LGW", result.embarkation_airport_code)
        self.assertEqual("RMU", result.destination_airport_code)
        self.assertEqual("EasyJet", result.airline)
        self.assertEqual("U28549", result.number)

    def test_call_function_with_parameters_requires_valid_flight(self):
        option = {
            "description": "Test Option",
            "has_flight_parameter": True,
            "function": dummy_function_2
        }
        with self.assertRaises(ValueError):
            _ = call_option_function(option, None)

    def test_call_function_with_no_parameters_doesnt_change_flight(self):
        option = {
            "description": "Test Option",
            "has_flight_parameter": False,
            "function": dummy_function_3
        }
        result = call_option_function(option, 10)
        self.assertEqual(10, result)

    def test_call_function_with_no_parameters_changes_flight(self):
        option = {
            "description": "Test Option",
            "has_flight_parameter": False,
            "function": dummy_function_4
        }
        result = call_option_function(option, None)
        self.assertEqual("LGW", result.embarkation_airport_code)
        self.assertEqual("RMU", result.destination_airport_code)
        self.assertEqual("EasyJet", result.airline)
        self.assertEqual("U28549", result.number)
