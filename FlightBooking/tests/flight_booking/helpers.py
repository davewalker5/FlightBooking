import datetime
import os
import shutil
from random import randint
from src.flight_booking import *
from src.flight_booking.utils import get_data_folder

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


def remove_files(folder):
    """
    Remove all files from the specified data sub-folder

    :param folder: Sub-folder to clean
    """
    folder_to_clean = get_data_folder(folder)
    for filename in os.listdir(folder_to_clean):
        file_path = os.path.join(folder_to_clean, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting {file_path} : {e}")
