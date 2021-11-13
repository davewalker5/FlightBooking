import datetime
from random import randint
from src.flight_booking import *

base_passport_number = randint(1, 100000)


def create_test_flight():
    return Flight(
        airline="EasyJet",
        number="U28549",
        embarkation="LGW",
        destination="RMU",
        departs=datetime.datetime(2021, 11, 20, 10, 45, 0),
        duration=datetime.timedelta(hours=2, minutes=35)
    )


def create_test_passenger():
    """
    Helper method to create a passenger
    """
    global base_passport_number
    base_passport_number += 1
    return create_passenger("Some Passenger",
                            "M",
                            datetime.datetime(1980, 1, 1),
                            "United Kingdom",
                            "United Kingdom",
                            str(base_passport_number).zfill(6))


def fill_test_flight(flight):
    """
    Helper method to fill the flight
    """
    for _ in range(flight.capacity):
        passenger = create_test_passenger()
        flight.add_passenger(passenger)
        flight.allocate_next_empty_seat(passenger["id"])
