"""
This module provides supporting functions for determining and returning locations for reference and output files.
By default, those files are held in separate sub-folders under the "data" folder of the project itself. An
environment variable can be used to override the default location.
"""

import os
import re

FLIGHT_BOOKING_DATA_FOLDER_ENV = "FLIGHT_BOOKING_DATA_FOLDER"


def get_data_folder(folder_name):
    """
    Get a data folder path which is either a sub-folder of the folder specified
    in an environment variable or, if that isn't set, is a sub-folder of a
    default folder within the project structure

    :param folder_name: Name of the sub-folder
    :return: Full path to the specified sub-folder
    """
    data_folder = os.getenv(FLIGHT_BOOKING_DATA_FOLDER_ENV)
    if data_folder is None:
        # This assumes the data folder is at the top-level of the project
        project_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        data_folder = os.path.join(project_folder, "data")
    return os.path.join(data_folder, folder_name)


def get_flight_file_path(number, departure_date):
    """
    Construct the path to a flight file

    :param number: Flight number
    :param departure_date: Departure date and time
    """
    # Flights are either saved to a location pointed to by an environment variable or to
    # a defined folder within the project
    folder = get_data_folder("flights")

    # Flight files are named number_departs.dat
    file_name = "_".join([number, departure_date.strftime("%Y%m%d")])

    # Replace non-alphanumeric characters with underscores
    file_name = re.sub("\\W", "_", file_name).lower() + ".json"
    return os.path.join(folder, file_name)


def get_seating_file_path(airline, aircraft, layout=None):
    """
    Construct the path to a seating plan file

    :param airline: Name of the airline
    :param aircraft: Name of the aircraft
    :param layout: Optional layout name
    """
    # Seating plan file names are airline_aircraft_layout.csv, where the layout is optional
    plan_folder = get_data_folder("seating_plans")
    file_name = "_".join([airline, aircraft, layout]) if layout is not None else "_".join([airline, aircraft])

    # Replace non-alphanumeric characters with underscores
    file_name = re.sub("\\W", "_", file_name).lower() + ".csv"
    return os.path.join(plan_folder, file_name.lower())


def get_boarding_card_path(flight_number, seat_number, departure_date, card_format):
    """
    Construct the path to a boarding card file

    :param flight_number: Flight number
    :param seat_number: Seat number
    :param departure_date: Departure date and time
    :param card_format: Boarding card format, used as the file extension
    :return:
    """
    # Boarding card file names are flight-number_seat-number_date.csv
    card_folder = get_data_folder("boarding_cards")
    file_name = "_".join([flight_number, seat_number, departure_date.strftime("%Y%m%d")])

    # Replace non-alphanumeric characters with underscores
    file_name = re.sub("\\W", "_", file_name).lower()
    return os.path.join(card_folder, file_name.lower() + "." + card_format)


def get_lookup_file_path(file_name):
    """
    Return the full path to a file in the lookups folder

    :param file_name: File name to return the full path for
    :return: Full path to the file
    """
    lookups_folder = get_data_folder("lookups")
    return os.path.join(lookups_folder, file_name)
