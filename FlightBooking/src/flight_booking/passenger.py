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
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "gender": gender,
        "dob": dob.strftime("%Y%m%d"),
        "nationality": nationality,
        "residency": residency,
        "passport_number": passport_number
    }
