"""
This module contains methods for managing passengers. Each passenger is represented as a dictionary of properties. On
creation, each passenger is allocated a unique identifier (GUID) that is assigned to their seat in the seating plan
when the seat is allocated.
"""

import uuid


def create_passenger(name, gender, dob, nationality, residency, passport_number):
    """
    Create a dictionary representing a passenger given their details. The dictionary
    includes a unique identifier

    :param name: Full name of the passenger
    :param gender: Passenger's gender
    :param dob: Passenger's date of birth
    :param nationality: Passenger's nationality
    :param residency: Passenger's country of residency
    :param passport_number: Passenger's passport number
    :return: A dictionary representing the passenger
    """
    if not name:
        raise ValueError("Name is mandatory")

    if gender not in ["M", "F"]:
        raise ValueError(f"'{gender}' is not a valid gender")

    if not dob:
        raise ValueError("Date of birth is mandatory")

    if not nationality:
        raise ValueError("Nationality is mandatory")

    if not residency:
        raise ValueError("Country of residency is mandatory")

    if not passport_number:
        raise ValueError("Passport number is mandatory")

    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "gender": gender,
        "dob": dob.strftime("%Y%m%d"),
        "nationality": nationality,
        "residency": residency,
        "passport_number": passport_number
    }
