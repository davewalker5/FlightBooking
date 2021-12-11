import unittest
import os
from unittest.mock import patch
from src.booking_app.option_callbacks import add_passenger_to_flight, \
    save_flight, \
    load_flight, \
    allocate_seat, \
    remove_passenger, \
    print_boarding_cards
from tests.helpers import get_flight_data_file_path, \
    delete_flight_data_file, \
    create_test_flight, \
    create_test_passenger, \
    binary_card_generator, \
    remove_files, \
    get_flight_boarding_card_file_path


class TestOptionCallbacks(unittest.TestCase):
    def setUp(self) -> None:
        self._flight = create_test_flight()
        self._passenger = create_test_passenger()

    @patch("flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"},
            "RMU": {"code": "RMU", "name": "Murcia International Airport", "tz": "Europe/Madrid"}})
    @patch("builtins.input", side_effect=["Some Passenger", "M", "01/02/1970", "England", "UK", "1234567890"])
    def test_can_add_passenger(self, _):
        add_passenger_to_flight(self._flight)
        self.assertEqual(1, len(self._flight.passengers))

    @patch("flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"},
            "RMU": {"code": "RMU", "name": "Murcia International Airport", "tz": "Europe/Madrid"}})
    @patch("builtins.input", side_effect=[""])
    def test_can_cancel_add_passenger(self, _):
        add_passenger_to_flight(self._flight)
        self.assertEqual(0, len(self._flight.passengers))

    def test_can_save_flight(self):
        delete_flight_data_file(self._flight)
        save_flight(self._flight)
        self.assertTrue(os.path.exists(get_flight_data_file_path(self._flight)))

    @patch("flight_booking.airport.airport_codes",
           {"LGW": {"code": "LGW", "name": "London Gatwick", "tz": "Europe/London"},
            "RMU": {"code": "RMU", "name": "Murcia International Airport", "tz": "Europe/Madrid"}})
    @patch("builtins.input", side_effect=["U28549", "20/11/2099"])
    def test_can_load_flight(self, _):
        delete_flight_data_file(self._flight)
        save_flight(self._flight)
        flight = load_flight()
        self.assertEqual("LGW", flight.embarkation_airport_code)
        self.assertEqual("RMU", flight.destination_airport_code)
        self.assertEqual("EasyJet", flight.airline)
        self.assertEqual("U28549", flight.number)
        self.assertEqual("20/11/2099", flight.departs_localtime.strftime("%d/%m/%Y"))
        self.assertEqual((2, 35), flight.duration)

    @patch("builtins.input", side_effect=[""])
    def test_can_cancel_load_flight_at_flight_number(self, _):
        flight = load_flight()
        self.assertIsNone(flight)

    @patch("builtins.input", side_effect=["U28549", ""])
    def test_can_cancel_load_flight_at_date(self, _):
        flight = load_flight()
        self.assertIsNone(flight)

    @patch("builtins.input", side_effect=["1", "5D"])
    def test_can_allocate_seat(self, _):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        allocate_seat(self._flight)
        self.assertTrue("5D", self._flight.get_allocated_seat(self._passenger["id"]))

    @patch("builtins.input", side_effect=[""])
    def test_can_cancel_allocate_seat_at_passenger(self, _):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        allocate_seat(self._flight)
        self.assertIsNone(self._flight.get_allocated_seat(self._passenger["id"]))

    @patch("builtins.input", side_effect=["1", ""])
    def test_can_cancel_allocate_seat_at_seat_number(self, _):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        allocate_seat(self._flight)
        self.assertIsNone(self._flight.get_allocated_seat(self._passenger["id"]))

    @patch("builtins.input", side_effect=["1"])
    def test_can_remove_passenger(self, _):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        remove_passenger(self._flight)
        self.assertEqual(0, len(self._flight.passengers))

    @patch("builtins.input", side_effect=[""])
    def test_can_cancel_remove_passenger(self, _):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        remove_passenger(self._flight)
        self.assertEqual(1, len(self._flight.passengers))

    @patch("flight_booking.flight.card_generator_map", {"pdf": binary_card_generator})
    @patch("builtins.input", side_effect=["28A"])
    def test_can_generate_boarding_cards(self, _):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        self._flight.allocate_seat("5D", self._passenger["id"])

        remove_files("boarding_cards")
        boarding_card_file = get_flight_boarding_card_file_path(self._flight, "5D", "pdf")
        self.assertFalse(os.path.exists(boarding_card_file))

        print_boarding_cards(self._flight)
        self.assertTrue(os.path.exists(boarding_card_file))
        remove_files("boarding_cards")

    @patch("builtins.input", side_effect=[""])
    def test_can_cancel_generate_boarding_cards(self, _):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        self._flight.allocate_seat("5D", self._passenger["id"])

        remove_files("boarding_cards")
        boarding_card_file = get_flight_boarding_card_file_path(self._flight, "5D", "pdf")
        self.assertFalse(os.path.exists(boarding_card_file))

        print_boarding_cards(self._flight)
        self.assertFalse(os.path.exists(boarding_card_file))
