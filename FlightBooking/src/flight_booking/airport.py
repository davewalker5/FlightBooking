"""
This module defines methods for managing airport details. A lookup of valid airports is read from a JSON-formatted
data file to give a dictionary in which the 3-letter IATA airport codes are the keys and the values are dictionaries
containing the airport properties.
"""

import json
from .utils import get_lookup_file_path

airport_codes = None


def load_airport_code_lookup():
    """
    Load the file containing airport details

    :return: A dictionary with airport codes as the keys and a dictionary of values as the values
    """
    code_file = get_lookup_file_path("airport_codes.json")
    with open(code_file, mode="rt", encoding="utf-8") as f:
        json_data = json.load(f)
    return json_data["airport_codes"]


def get_airport(airport_code):
    """
    Return a dictionary of airport properties for the airport with the specified code

    :param airport_code: Airport code e.g. LGW
    :return: Dictionary of airport properties
    """
    global airport_codes
    if airport_codes is None:
        airport_codes = load_airport_code_lookup()

    return airport_codes[airport_code]
