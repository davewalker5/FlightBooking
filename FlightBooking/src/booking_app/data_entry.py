"""
This module defines functions used by the console booking application package to read and validate user input
"""

import datetime
from flight_booking.airport import get_airport
from flight_booking.flight import Flight
from flight_booking.passenger import create_passenger
from .exceptions import InvalidAirportCodeError, InvalidAircraftSeatingPlanError


def trimmed_input(prompt):
    """
    Prompt for and return input, stripping leading and trailing whitespace

    :param prompt: Prompt string presented to the user
    :return: Trimmed input
    """
    return input(prompt).strip()


def input_integer(prompt, minimum=None, maximum=None):
    """
    Prompt for an integer, optionally imposing a valid range on the  value

    :param prompt: Prompt string presented to the user
    :param minimum: Optional minimum value
    :param maximum: Optional maximum value
    :return: Integer selection or None if cancelled
    """
    raw_input = trimmed_input(prompt)
    if len(raw_input) == 0:
        return None

    try:
        number = int(raw_input)
    except ValueError as e:
        raise ValueError(f"{raw_input} is not a valid integer") from e

    if minimum and number < int(minimum):
        raise ValueError(f"{raw_input} is not in the range {minimum} to {maximum}")

    if maximum and number > maximum:
        raise ValueError(f"{raw_input} is not in the range {minimum} to {maximum}")

    return number


def input_date(date_type, minimum=None, maximum=None):
    """
    Prompt for a date and optionally check it conforms to the specified minimum and maximum values

    :param date_type: Date type, used in the prompt
    :param minimum: Minimum acceptable date or None if there is no minimum
    :param maximum: Maximum acceptable date or None if there is no maximum
    :return: The date as a date() object or None if cancelled
    """
    date_string = trimmed_input(f"{date_type} DD/MM/YYYY [ENTER to quit] ")
    if len(date_string) == 0:
        return None

    try:
        d = datetime.datetime.strptime(date_string, "%d/%m/%Y").date()
    except ValueError as e:
        raise ValueError(f"{date_string} is not a valid date") from e

    if minimum and d < minimum:
        raise ValueError(f"{date_string} is before the minimum {minimum.strftime('%d/%m/%Y')}")
    elif maximum and d > maximum:
        raise ValueError(f"{date_string} is after the maximum {maximum.strftime('%d/%m/%Y')}")

    return d


def input_future_date(date_type):
    """
    Prompt for a date, that must be in the future

    :param date_type: Type of date e.g. Departure date - used in the prompt string
    :return: The date as a date() object or None if cancelled
    """
    minimum = datetime.datetime.now().date() + datetime.timedelta(days=1)
    return input_date(date_type, minimum=minimum)


def input_past_date(date_type):
    """
    Prompt for a date, that must be in the past

    :param date_type: Type of date e.g. DoB - used in the prompt string
    :return: The date as a date() object or None if cancelled
    """
    maximum = datetime.datetime.now().date() + datetime.timedelta(days=-1)
    return input_date(date_type, maximum=maximum)


def input_airport_code(airport_type):
    """
    Prompt for an airport code and return the corresponding airport object

    :param airport_type: Text used in the prompt to indicate embarkation or destination airport
    :return: A dictionary of airport properties or None if cancelled
    """
    code = trimmed_input(f"{airport_type} airport code [ENTER to quit] ")
    if len(code) == 0:
        return None

    try:
        airport = get_airport(code)
    except KeyError:
        raise InvalidAirportCodeError(f"Airport code is not recognised", code)

    return airport


def input_departure_time():
    """
    Prompt for the departure time

    :return: The departure time as a time() object or None if cancelled
    """
    departure_time_string = trimmed_input("Departure time in 24-hour format HH:MM [ENTER to quit] ")
    if len(departure_time_string) == 0:
        return None

    try:
        departure_time = datetime.datetime.strptime(departure_time_string, "%H:%M").time()
    except ValueError as e:
        raise ValueError(f"{departure_time_string} is not a valid time") from e

    return departure_time


def input_duration():
    """
    Prompt for the flight duration expressed as HH:MM, where the hours are >= 0
    and the minutes are between 0 and 59

    :return: The flight duration as a timedelta() object or None if cancelled
    """
    duration_string = trimmed_input("Duration HH:MM [ENTER to quit] ")
    if len(duration_string) == 0:
        return None

    words = duration_string.split(sep=":")
    if len(words) != 2:
        raise ValueError(f"{duration_string} is not a valid duration")

    hours = int(words[0])
    if hours < 0:
        raise ValueError(f"{hours} is not a valid number of hours")

    minutes = int(words[1])
    if minutes < 0 or minutes > 59:
        raise ValueError(f"{minutes} is not a valid number of minutes")

    duration = datetime.timedelta(hours=hours, minutes=minutes)
    if duration.seconds == 0:
        raise ValueError(f"{duration_string} is too short a duration")

    return duration


def input_gender():
    """
    Prompt for and return a passenger's gender

    :return: Gender, M or F or None if cancelled
    """
    gender = trimmed_input("Gender M/F [ENTER to quit] ").upper()
    if len(gender) == 0:
        return None

    if gender not in ["M", "F"]:
        raise ValueError(f"{gender} is not a valid gender")

    return gender


def input_aircraft_seating_plan(flight):
    """
    Prompt for and load an aircraft seating plan for a flight

    :param flight: The flight object for which the aircraft seating plan is to be loaded
    """
    aircraft_model_and_layout = trimmed_input("Aircraft model and (optional) layout e.g. A321:NEO [ENTER to quit] ")
    if len(aircraft_model_and_layout) == 0:
        return None

    words = aircraft_model_and_layout.split(":")
    if len(words) > 2:
        raise InvalidAircraftSeatingPlanError(f"{aircraft_model_and_layout} is  not a valid aircraft layout")

    aircraft = words[0].strip()
    layout = words[1].strip() if len(words) > 1 else None

    try:
        flight.load_seating(aircraft, layout)
    except FileNotFoundError as e:
        raise InvalidAircraftSeatingPlanError(
            f"No seating plan found for aircraft model {aircraft} with layout {layout}",
            aircraft=aircraft,
            layout=layout
        ) from e


def input_flight():
    """
    Prompts for flight details and then constructs a Flight() object from the entered data

    :return: A flight object or None if data entry is cancelled
    """
    embarkation = input_airport_code("Embarkation")
    if not embarkation:
        return

    destination = input_airport_code("Destination")
    if not destination:
        return

    airline = trimmed_input("Airline [ENTER to quit] ")
    if not airline:
        return

    flight_number = trimmed_input("Flight number [ENTER to quit] ")
    if not flight_number:
        return

    departure_date = input_future_date("Departure date")
    if not departure_date:
        return

    departure_time = input_departure_time()
    if not departure_time:
        return

    duration = input_duration()
    if not duration:
        return

    # Combine the departure date and time then construct and return a flight object
    departs = datetime.datetime.combine(departure_date, departure_time)
    return Flight(embarkation["code"], destination["code"], airline, flight_number, departs, duration)


def input_passenger():
    """
    Prompts for passenger details and then constructs a passenger object from them

    :return: Dictionary defining a passenger or None if cancelled
    """
    name = trimmed_input("Passenger name [ENTER to quit] ")
    if not name:
        return

    gender = input_gender()
    if not gender:
        return

    dob = input_past_date("Date of birth")
    if not dob:
        return

    nationality = trimmed_input("Nationality [ENTER to quit] ")
    if not nationality:
        return

    residency = trimmed_input("Residency [ENTER to quit] ")
    if not residency:
        return

    passport_number = trimmed_input("Passport number [ENTER to quit] ")
    if not passport_number:
        return

    return create_passenger(name, gender, dob, nationality, residency, passport_number)


def list_passengers(passengers):
    """
    List passenger details, associating an integer passenger number with each one

    :param passengers: Sequence of passengers to list
    """
    i = 0
    for passenger in passengers.values():
        i += 1
        print(f"{str(i).rjust(4)} - {passenger['name']} - {passenger['passport_number']}")


def select_passenger(passengers):
    """
    Prompt for a passenger number until that number is correct or the user's cancelled input

    :param passengers: Collection of passengers to list
    :return: Passenger number or None if cancelled
    """
    list_passengers(passengers)
    print()
    while True:
        try:
            number = input_integer("Passenger number [ENTER to quit] ", minimum=1, maximum=len(passengers))
            return passengers[list(passengers.keys())[number - 1]] if number else None
        except ValueError as e:
            print(e)
