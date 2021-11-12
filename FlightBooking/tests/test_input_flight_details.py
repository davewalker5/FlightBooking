import unittest
from unittest.mock import patch
from src.flight_booking.flight import Flight
from src.flight_booking.data_entry import input_flight


class TestInputFlightDetails(unittest.TestCase):
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
