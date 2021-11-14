import datetime
from random import randint
from src.flight_booking import *

base_passport_number = randint(1, 100000)


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
