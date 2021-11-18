"""
This module implements a simple Model layer for use in the demonstration Flight Booking Web Application.

The FlightBookingModel class implements a thin wrapper around an instance of the Flight class, with the latter
supplying the bulk of the business logic. The wrapper consists of a small number of helper methods that provide
an interface between data input in the web application and the Flight business logic.

A module level variable exposes an instance of the model class for use in the Flask view functions in the booking.py
module.
"""

from flight_booking import Flight, create_passenger
import datetime
from copy import deepcopy
from random import randint


class FlightBookingModel:
    def __init__(self):
        self._flight = None

    @property
    def flight(self) -> Flight | None:
        """
        Return the current flight

        :return: Instance of the Flight class or None
        """
        return self._flight

    def create_flight(self, embarkation, destination, airline, number, departure_date, departure_time, duration):
        """
        Create a flight given the flight properties

        :param embarkation: 3-letter IATA code for the embarkation airport
        :param destination: 3-letter IATA code for the destination airport
        :param airline: Airline name
        :param number: Flight number
        :param departure_date: Departure date in the format DD/MM/YYYY
        :param departure_time: Departure time in the format HH:MM
        :param duration: Flight duration in the format HH:MM
        """
        departs = self._construct_date_and_time(departure_date, departure_time)
        flight_duration = self._construct_duration(duration)
        self._flight = Flight(
            airline=airline,
            number=number,
            embarkation=embarkation,
            destination=destination,
            departs=departs,
            duration=flight_duration
        )

    def create_dummy_flight(self, number_of_passengers=0, aircraft=None, layout=None, perform_seat_allocations=False):
        """
        Create and populate a dummy flight for development testing

        :param number_of_passengers: Number of passengers to add to the flight
        :param aircraft: Aircraft model
        :param layout: Aircraft seating layout
        :param perform_seat_allocations: If true, seat allocations will be created
        """
        self._create_dummy_flight()

        if number_of_passengers > 0:
            self._create_dummy_passengers(number_of_passengers=number_of_passengers)

        if aircraft:
            self._flight.load_seating(aircraft=aircraft, layout=layout)

        if number_of_passengers > 0 and aircraft and perform_seat_allocations:
            self._create_dummy_seat_allocations()

    def close_flight(self):
        """
        Close the current flight (i.e. set it back to None)
        """
        self._flight = None

    def add_passenger(self, name, gender, dob, nationality, residency, passport_number):
        """
        Create a passenger and allocate the next empty seat to them, if a seating plan's been loaded

        :param name: Passenger name
        :param gender: Passenger gender, M/F
        :param dob: Date of birth in the format DD/MM/YYYY
        :param nationality: Nationality of the  passenger
        :param residency: Country of residence of the passenger
        :param passport_number: Passenger's passport number
        """
        date_of_birth = datetime.datetime.strptime(dob, "%d/%m/%Y").date()
        passenger = create_passenger(name, gender, date_of_birth, nationality, residency, passport_number)

        self._flight.add_passenger(passenger)
        if self._flight.seating_plan:
            self._flight.allocate_next_empty_seat(passenger["id"])

    def get_passengers_including_seat_allocations(self):
        """
        Return a dictionary of passengers with the allocated seat number included in each passenger's details

        :return: Dictionary of passengers
        """
        passengers = {}
        for passenger_id in self._flight.passengers:
            passengers[passenger_id] = self._get_passenger_including_seat_allocation(passenger_id)
        return passengers

    def save(self):
        """
        Save the current flight details to a flight data file
        """
        self._flight.save()

    def load(self, number, departure_date):
        """
        Load the current flight from a flight data file

        :param number: Flight number
        :param departure_date: Departure date in the format DD/MM/YYYY
        """
        departs = datetime.datetime.strptime(departure_date, "%d/%m/%Y").date()
        self._flight = Flight.load_flight(number, departs)

    def _create_dummy_flight(self):
        """
        Create a flight with dummy airline, route and timing details
        """
        self.create_flight(
            airline="EasyJet",
            number="U28549",
            embarkation="LGW",
            destination="RMU",
            departure_date="20/11/2021",
            departure_time="10:45",
            duration="2:25"
        )

    def _create_dummy_passengers(self, number_of_passengers):
        """
        Create dummy passengers on a flight

        ":param number_of_passengers: The number of passengers to add
        """
        for i in range(number_of_passengers):
            passport_number = next(FlightBookingModel._next_passport_number())
            year = randint(1970, 1990)
            month = randint(1, 12)
            day = randint(1, 28)
            passenger = create_passenger(f"Passenger {i}",
                                         "M" if randint(1, 10) > 5 else "F",
                                         datetime.datetime(year, month, day),
                                         "United Kingdom",
                                         "United Kingdom",
                                         str(passport_number).zfill(6))
            self._flight.add_passenger(passenger)

    def _create_dummy_seat_allocations(self):
        """
        Allocate the next seat on the flight to each passenger in turn
        """
        for passenger_id in self._flight.passengers:
            self._flight.allocate_next_empty_seat(passenger_id)

    def _get_passenger_including_seat_allocation(self, passenger_id):
        """
        For a given flight and passenger ID, return the passenger details with the seat allocation added

        :param passenger_id: Passenger unique ID
        :return: Passenger dictionary for the specified passenger with the seat number added
        """
        passenger = deepcopy(self._flight.passengers[passenger_id])
        passenger["seat_number"] = self._flight.get_allocated_seat(passenger_id)
        return passenger

    @staticmethod
    def _next_passport_number():
        """
        Generator method to return a sequence of dummy passport numbers
        """
        passport_number = randint(1, 100000)
        while True:
            yield passport_number
            passport_number += 1

    @staticmethod
    def _construct_date_and_time(date_string, time_string):
        """
        Given strings representing the date and time parts of the departure date, combine them to generate a full date
        and time object

        :param date_string: Date part in the format DD/MM/YYYY
        :param time_string: Time part in the format HH:MM
        :return: A datetime object representing the date and time
        """
        departs_date = datetime.datetime.strptime(date_string, "%d/%m/%Y").date()
        departs_time = datetime.datetime.strptime(time_string, "%H:%M").time()
        return datetime.datetime.combine(departs_date, departs_time)

    @staticmethod
    def _construct_duration(duration_string):
        """
        Given a string representing the flight duration, parse it to generate a timedelta object

        :param duration_string: Duration in the format HH:MM
        :return: A timedelta object representing the flight duration
        """
        words = duration_string.split(sep=":")
        hours = int(words[0])
        minutes = int(words[1])
        return datetime.timedelta(hours=hours, minutes=minutes)


booking_model = FlightBookingModel()
