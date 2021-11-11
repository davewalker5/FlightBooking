import unittest
from datetime import date, time, timedelta
from unittest.mock import patch
from src.flight_booking.flight import Flight
from src.flight_booking.enter_flight_details import input_airport_code, \
    input_departure_date, \
    input_departure_time, \
    input_duration, \
    input_flight


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


class TestInputDepartureDate(unittest.TestCase):
    @patch("builtins.input", side_effect=["01/02/2021"])
    def test_valid_date(self, _):
        departure_date = input_departure_date()
        self.assertTrue(isinstance(departure_date, date))
        self.assertEqual(1, departure_date.day)
        self.assertEqual(2, departure_date.month)
        self.assertEqual(2021, departure_date.year)

    @patch("builtins.input", side_effect=["01/13/2021", "Not a Date", "01/02/2021"])
    def test_invalid_date_string_prompts_until_correct(self, _):
        departure_date = input_departure_date()
        self.assertTrue(isinstance(departure_date, date))
        self.assertEqual(1, departure_date.day)
        self.assertEqual(2, departure_date.month)
        self.assertEqual(2021, departure_date.year)

    @patch("builtins.input", side_effect=["  01/02/2021  "])
    def test_leading_trailing_whitespace_is_ignored(self, _):
        departure_date = input_departure_date()
        self.assertTrue(isinstance(departure_date, date))
        self.assertEqual(1, departure_date.day)
        self.assertEqual(2, departure_date.month)
        self.assertEqual(2021, departure_date.year)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        departure_date = input_departure_date()
        self.assertIsNone(departure_date)


class TestInputDepartureTime(unittest.TestCase):
    @patch("builtins.input", side_effect=["13:45"])
    def test_valid_time(self, _):
        departure_time = input_departure_time()
        self.assertTrue(isinstance(departure_time, time))
        self.assertEqual(13, departure_time.hour)
        self.assertEqual(45, departure_time.minute)
        self.assertEqual(0, departure_time.second)

    @patch("builtins.input", side_effect=["13:67", "46:45", "Not a time", "13:45"])
    def test_invalid_time_string_prompts_until_correct(self, _):
        departure_time = input_departure_time()
        self.assertTrue(isinstance(departure_time, time))
        self.assertEqual(13, departure_time.hour)
        self.assertEqual(45, departure_time.minute)
        self.assertEqual(0, departure_time.second)

    @patch("builtins.input", side_effect=["  13:45  "])
    def test_leading_trailing_whitespace_is_ignored(self, _):
        departure_time = input_departure_time()
        self.assertTrue(isinstance(departure_time, time))
        self.assertEqual(13, departure_time.hour)
        self.assertEqual(45, departure_time.minute)
        self.assertEqual(0, departure_time.second)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        departure_time = input_departure_time()
        self.assertIsNone(departure_time)


class TestInputDuration(unittest.TestCase):
    @patch("builtins.input", side_effect=["2:45"])
    def test_valid_duration(self, _):
        duration = input_duration()
        self.assertTrue(isinstance(duration, timedelta))
        self.assertEqual(9900, duration.seconds)

    @patch("builtins.input", side_effect=["03:56:56", "This is:not valid", "2:45"])
    def test_invalid_duration_prompts_until_correct(self, _):
        duration = input_duration()
        self.assertTrue(isinstance(duration, timedelta))
        self.assertEqual(9900, duration.seconds)

    @patch("builtins.input", side_effect=[""])
    def test_empty_input_cancels(self, _):
        duration = input_duration()
        self.assertIsNone(duration)


class TestEnterFlightDetails(unittest.TestCase):
    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"},
            "RMU": {"code": "RMU", "name": "Murcia International Airport", "tz": "Europe/Madrid"}})
    @patch("builtins.input", side_effect=["LGW", "RMU", "EasyJet", "EZY8549", "20/11/2021", "10:15", "2:25"])
    def test_full_flight_details_entry(self, _):
        flight = input_flight()
        self.assertTrue(isinstance(flight, Flight))
        self.assertEqual("LGW", flight.embarkation_airport_code)
        self.assertEqual("RMU", flight.destination_airport_code)
        self.assertEqual("EasyJet", flight.airline)
        self.assertEqual("EZY8549", flight.number)
        self.assertEqual("20/11/2021", flight.departure_date.strftime("%d/%m/%Y"))
        self.assertEqual("10:15", flight.departs_localtime.strftime("%H:%M"))
        self.assertEqual((2, 25), flight.duration)

    @patch("builtins.input", side_effect=[""])
    def test_cancel_on_embarkation(self,  _):
        flight = input_flight()
        self.assertIsNone(flight)

    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"}})
    @patch("builtins.input", side_effect=["LGW", ""])
    def test_cancel_on_destination(self,  _):
        flight = input_flight()
        self.assertIsNone(flight)

    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"},
            "RMU": {"code": "RMU", "name": "Murcia International Airport", "tz": "Europe/Madrid"}})
    @patch("builtins.input", side_effect=["LGW", "RMU", ""])
    def test_cancel_on_airline(self,  _):
        flight = input_flight()
        self.assertIsNone(flight)

    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"},
            "RMU": {"code": "RMU", "name": "Murcia International Airport", "tz": "Europe/Madrid"}})
    @patch("builtins.input", side_effect=["LGW", "RMU", "EasyJet", ""])
    def test_cancel_on_number(self,  _):
        flight = input_flight()
        self.assertIsNone(flight)

    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"},
            "RMU": {"code": "RMU", "name": "Murcia International Airport", "tz": "Europe/Madrid"}})
    @patch("builtins.input", side_effect=["LGW", "RMU", "EasyJet", "EZY8549", ""])
    def test_cancel_on_departure_date(self,  _):
        flight = input_flight()
        self.assertIsNone(flight)

    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"},
            "RMU": {"code": "RMU", "name": "Murcia International Airport", "tz": "Europe/Madrid"}})
    @patch("builtins.input", side_effect=["LGW", "RMU", "EasyJet", "EZY8549", "20/11/2021", ""])
    def test_cancel_on_departure_time(self,  _):
        flight = input_flight()
        self.assertIsNone(flight)

    @patch("src.flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"},
            "RMU": {"code": "RMU", "name": "Murcia International Airport", "tz": "Europe/Madrid"}})
    @patch("builtins.input", side_effect=["LGW", "RMU", "EasyJet", "EZY8549", "20/11/2021", "10:15", ""])
    def test_cancel_on_duration(self,  _):
        flight = input_flight()
        self.assertIsNone(flight)
