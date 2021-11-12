import unittest
from src.booking_app.option_handler import validate_all_options


def dummy_function_with_no_parameters():
    pass


def dummy_function_with_flight_parameter(flight):
    pass


def dummy_function_with_non_flight_parameters(a, b, c):
    pass


class TestValidateOptionsMap(unittest.TestCase):
    def test_function_with_no_parameters_is_valid(self):
        options_map = {
            "1": {"description": "Test Option", "function": dummy_function_with_no_parameters}
        }
        validate_all_options(options_map)
        self.assertFalse(options_map["1"]["has_flight_parameter"])

    def test_function_with_flight_parameter_is_valid(self):
        options_map = {
            "1": {"description": "Test Option", "function": dummy_function_with_flight_parameter}
        }
        validate_all_options(options_map)
        self.assertTrue(options_map["1"]["has_flight_parameter"])

    def test_function_with_non_flight_parameters_is_valid(self):
        options_map = {
            "1": {"description": "Test Option", "function": dummy_function_with_non_flight_parameters}
        }
        validate_all_options(options_map)
        self.assertFalse(options_map["1"]["has_flight_parameter"])

    def test_option_with_none_function_is_valid(self):
        validate_all_options({
            "1": {"description": "Test Option", "function": None}
        })
        self.assertTrue(True)

    def test_option_with_non_callable_errors(self):
        with self.assertRaises(AssertionError):
            validate_all_options({
                "1": {"description": "Test Option", "function": 1}
            })

    def test_option_with_no_function_errors(self):
        with self.assertRaises(AssertionError):
            validate_all_options({
                "1": {"description": "Test Option"}
            })

    def test_option_with_empty_description_errors(self):
        with self.assertRaises(AssertionError):
            validate_all_options({
                "1": {"description": "", "function": None}
            })

    def test_option_with_no_description_errors(self):
        with self.assertRaises(AssertionError):
            validate_all_options({
                "1": {"function": None}
            })
