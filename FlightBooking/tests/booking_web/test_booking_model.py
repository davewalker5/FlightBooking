import unittest
import datetime
import os
from flight_booking.utils import get_flight_file_path
from src.booking_web.model import FlightBookingModel


class TestFlightBookingModel(unittest.TestCase):
    def setUp(self) -> None:
        self._model = FlightBookingModel()

    def test_create_flight(self):
        self._model.create_flight(
            airline="EasyJet",
            number="U28549",
            embarkation="LGW",
            destination="RMU",
            departure_date="20/11/2021",
            departure_time="10:45",
            duration="2:25")

        self.assertIsNotNone(self._model.flight)
        self.assertEqual("EasyJet", self._model.flight.airline)
        self.assertEqual("U28549", self._model.flight.number)
        self.assertEqual("LGW", self._model.flight.embarkation_airport_code)
        self.assertEqual("RMU", self._model.flight.destination_airport_code)
        self.assertEqual(datetime.date(2021, 11, 20), self._model.flight.departure_date)
        self.assertEqual((2, 25), self._model.flight.duration)
        self.assertEqual(0, len(self._model.flight.passengers))
        self.assertEqual(None, self._model.flight.aircraft)
        self.assertEqual(None, self._model.flight.layout)
        self.assertEqual(0, self._model.flight.capacity)
        self.assertEqual(0, self._model.flight.available_capacity)
        self.assertIsNone(None, self._model.flight.aircraft)
        self.assertIsNone(self._model.flight.get_all_seat_allocations())

    def test_create_dummy_flight(self):
        self._model.create_dummy_flight(number_of_passengers=0,
                                        aircraft=None,
                                        layout=None,
                                        perform_seat_allocations=False)

        self.assertIsNotNone(self._model.flight)
        self.assertEqual("EasyJet", self._model.flight.airline)
        self.assertEqual("U28549", self._model.flight.number)
        self.assertEqual("LGW", self._model.flight.embarkation_airport_code)
        self.assertEqual("RMU", self._model.flight.destination_airport_code)
        self.assertEqual(datetime.date(2021, 11, 20), self._model.flight.departure_date)
        self.assertEqual((2, 25), self._model.flight.duration)
        self.assertEqual(0, len(self._model.flight.passengers))
        self.assertEqual(None, self._model.flight.aircraft)
        self.assertEqual(None, self._model.flight.layout)
        self.assertEqual(0, self._model.flight.capacity)
        self.assertEqual(0, self._model.flight.available_capacity)
        self.assertIsNone(None, self._model.flight.aircraft)
        self.assertIsNone(self._model.flight.get_all_seat_allocations())

    def test_create_dummy_flight_with_passengers(self):
        self._model.create_dummy_flight(number_of_passengers=10,
                                        aircraft=None,
                                        layout=None,
                                        perform_seat_allocations=False)

        self.assertIsNotNone(self._model.flight)
        self.assertEqual("EasyJet", self._model.flight.airline)
        self.assertEqual("U28549", self._model.flight.number)
        self.assertEqual("LGW", self._model.flight.embarkation_airport_code)
        self.assertEqual("RMU", self._model.flight.destination_airport_code)
        self.assertEqual(datetime.date(2021, 11, 20), self._model.flight.departure_date)
        self.assertEqual((2, 25), self._model.flight.duration)
        self.assertEqual(10, len(self._model.flight.passengers))
        self.assertEqual(None, self._model.flight.aircraft)
        self.assertEqual(None, self._model.flight.layout)
        self.assertEqual(0, self._model.flight.capacity)
        self.assertEqual(0, self._model.flight.available_capacity)
        self.assertIsNone(None, self._model.flight.aircraft)
        self.assertIsNone(self._model.flight.get_all_seat_allocations())

    def test_create_dummy_flight_with_passengers_and_layout(self):
        self._model.create_dummy_flight(number_of_passengers=10,
                                        aircraft="A321",
                                        layout="neo",
                                        perform_seat_allocations=False)

        self.assertIsNotNone(self._model.flight)
        self.assertEqual("EasyJet", self._model.flight.airline)
        self.assertEqual("U28549", self._model.flight.number)
        self.assertEqual("LGW", self._model.flight.embarkation_airport_code)
        self.assertEqual("RMU", self._model.flight.destination_airport_code)
        self.assertEqual(datetime.date(2021, 11, 20), self._model.flight.departure_date)
        self.assertEqual((2, 25), self._model.flight.duration)
        self.assertEqual(10, len(self._model.flight.passengers))
        self.assertEqual("A321", self._model.flight.aircraft)
        self.assertEqual("neo", self._model.flight.layout)
        self.assertEqual(235, self._model.flight.capacity)
        self.assertEqual(225, self._model.flight.available_capacity)
        self.assertEqual(0, len(self._model.flight.get_all_seat_allocations()))

    def test_create_dummy_flight_with_passengers_layout_and_allocations(self):
        self._model.create_dummy_flight(number_of_passengers=10,
                                        aircraft="A321",
                                        layout="neo",
                                        perform_seat_allocations=True)

        self.assertIsNotNone(self._model.flight)
        self.assertEqual("EasyJet", self._model.flight.airline)
        self.assertEqual("U28549", self._model.flight.number)
        self.assertEqual("LGW", self._model.flight.embarkation_airport_code)
        self.assertEqual("RMU", self._model.flight.destination_airport_code)
        self.assertEqual(datetime.date(2021, 11, 20), self._model.flight.departure_date)
        self.assertEqual((2, 25), self._model.flight.duration)
        self.assertEqual(10, len(self._model.flight.passengers))
        self.assertEqual("A321", self._model.flight.aircraft)
        self.assertEqual("neo", self._model.flight.layout)
        self.assertEqual(235, self._model.flight.capacity)
        self.assertEqual(225, self._model.flight.available_capacity)
        self.assertEqual(10, len(self._model.flight.get_all_seat_allocations()))

    def test_can_add_passenger(self):
        self._model.create_dummy_flight(number_of_passengers=0,
                                        aircraft=None,
                                        layout=None,
                                        perform_seat_allocations=False)

        self._model.add_passenger("Some One",
                                  "M",
                                  "01/02/1980",
                                  "UK",
                                  "UK",
                                  "1234567890")

        self.assertEqual(1, len(self._model.flight.passengers))
        self.assertEqual(1, len(self._model.flight.passengers))

        passenger_id = list(self._model.flight.passengers.keys())[0]
        passenger = self._model.flight.passengers[passenger_id]
        self.assertEqual("Some One", passenger["name"])
        self.assertEqual("M", passenger["gender"])
        self.assertEqual("19800201", passenger["dob"])
        self.assertEqual("UK", passenger["nationality"])
        self.assertEqual("UK", passenger["residency"])
        self.assertEqual("1234567890", passenger["passport_number"])

    def test_can_get_passenger_with_no_seat_allocation(self):
        self._model.create_dummy_flight(number_of_passengers=1,
                                        aircraft="A321",
                                        layout="neo",
                                        perform_seat_allocations=False)

        passenger_details = self._model.get_passengers_including_seat_allocations()
        passenger_id = list(passenger_details.keys())[0]
        passenger = passenger_details[passenger_id]
        self.assertIsNone(passenger["seat_number"])

    def test_can_get_passenger_with_seat_allocation(self):
        self._model.create_dummy_flight(number_of_passengers=1,
                                        aircraft="A321",
                                        layout="neo",
                                        perform_seat_allocations=True)

        passenger_details = self._model.get_passengers_including_seat_allocations()
        passenger_id = list(passenger_details.keys())[0]
        passenger = passenger_details[passenger_id]
        self.assertEqual("1A", passenger["seat_number"])

    def test_can_save_flight(self):
        self._model.create_dummy_flight(number_of_passengers=0,
                                        aircraft=None,
                                        layout=None,
                                        perform_seat_allocations=False)

        file_path = get_flight_file_path(self._model.flight.number, self._model.flight.departure_date)
        if os.path.exists(file_path):
            os.remove(file_path)
        self.assertFalse(os.path.exists(file_path))

        self._model.save()
        self.assertTrue(os.path.exists(file_path))

    def test_can_close_flight(self):
        self._model.create_dummy_flight(number_of_passengers=0,
                                        aircraft=None,
                                        layout=None,
                                        perform_seat_allocations=False)

        self.assertIsNotNone(self._model.flight)
        self._model.close_flight()
        self.assertIsNone(self._model.flight)
