"""
This module contains helper methods to perform common operations required by the unit tests
"""

import datetime
import os
import shutil
from random import randint
from src.flight_booking import *
from src.flight_booking.utils import get_data_folder, get_flight_file_path, get_boarding_card_path

base_passport_number = randint(1, 100000)


def create_test_flight():
    """
    Helper method to create a flight

    :return: An instance of the Flight class
    """
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

    :return: A passenger, represented as a dictionary of properties
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


def get_flight_data_file_path(flight):
    """
    Return the full path to a flight data file

    :param flight: Flight for which to get the data file path
    :return: Data file path
    """
    return get_flight_file_path(flight.number, flight.departure_date)


def get_flight_boarding_card_file_path(flight, seat_number, card_format):
    return get_boarding_card_path(flight.number, seat_number, flight.departure_date, card_format)


def delete_flight_data_file(flight):
    """
    Delete the flight data file for the specified flight

    :param flight: Flight for which to delete the data file
    """
    file_path = get_flight_data_file_path(flight)
    if os.path.exists(file_path):
        os.remove(file_path)


def text_card_generator(card_details):
    """
    Stub card generator monkeypatched into the flight module for testing
    boarding card printing

    :param card_details: Boarding card details
    """
    return "\n".join(card_details.values())


def binary_card_generator(card_details):
    """
    Stub card generator monkeypatched into the flight module for testing
    boarding card printing

    :param card_details: Boarding card details
    """
    return "\n".join(card_details.values()).encode("utf-8")
