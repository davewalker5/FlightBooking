import datetime
from .airport import get_airport
from .flight import Flight
from .passenger import create_passenger


def trimmed_input(prompt):
    """
    Prompt for and return input, stripping leading and trailing whitespace

    :return: Trimmed input
    """
    return input(prompt).strip()


def input_date(date_type, minimum=None, maximum=None):
    """
    Prompt for a date and optionally check it conforms to the specified minimum and maximum values

    :param date_type: Date type, used in the prompt
    :param minimum: Minimum acceptable date or None if there is no minimum
    :param maximum: Maximum acceptable date or None if there is no maximum
    :return: The date as a date() object or None if cancelled
    """
    while True:
        date_string = trimmed_input(f"{date_type} DD/MM/YYYY [ENTER to quit] ")
        if len(date_string) > 0:
            try:
                d = datetime.datetime.strptime(date_string, "%d/%m/%Y").date()
                if minimum and d < minimum:
                    print(f"{date_string} is before the minimum {minimum.strftime('%d/%m/%Y')}")
                elif maximum and d > maximum:
                    print(f"{date_string} is after the maximum {maximum.strftime('%d/%m/%Y')}")
                else:
                    return d
            except ValueError:
                print(f"{date_string} is not a valid date")
        else:
            return


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
    while True:
        code = trimmed_input(f"{airport_type} airport code [ENTER to quit] ")
        if len(code) > 0:
            try:
                airport = get_airport(code)
                return airport
            except KeyError:
                print(f"Airport code {code} is not recognised")
        else:
            return


def input_departure_date():
    """
    Prompt for and return a passenger's date of birth

    :return: The DoB as a date() object or None if cancelled
    """
    while True:
        dob = input_date("Date of birth")
        if not dob or dob < datetime.datetime.now().date():
            return dob
        print(f"{dob.strftime('%d/%m/%Y')} is a future date and not a valid DoB")


def input_departure_time():
    """
    Prompt for the departure time

    :return: The departure time as a time() object or None if cancelled
    """
    while True:
        departure_time_string = trimmed_input("Departure time in 24-hour format HH:MM [ENTER to quit] ")
        if len(departure_time_string) > 0:
            try:
                departure_time = datetime.datetime.strptime(departure_time_string, "%H:%M").time()
                return departure_time
            except ValueError:
                print(f"{departure_time_string} is not a valid time")
        else:
            return


def input_duration():
    """
    Prompt for the flight duration

    :return: The flight duration as a timedelta() object or None if cancelled
    """
    while True:
        duration_string = trimmed_input("Duration HH:MM [ENTER to quit] ")
        if not duration_string:
            return

        words = duration_string.split(sep=":")
        if len(words) == 2:
            try:
                hours = int(words[0])
                minutes = int(words[1])
                return datetime.timedelta(hours=hours, minutes=minutes)
            except ValueError:
                pass  # Error is printed, below, so we can sink value exceptions here

        print(f"{duration_string} is not a valid duration")


def input_gender():
    """
    Prompt for and return a passenger's gender

    :return: Gender, M or F or None if cancelled
    """
    while True:
        gender = trimmed_input("Gender M/F [ENTER to quit] ").upper()
        if len(gender) > 0:
            if gender in ["M", "F"]:
                return gender
            print(f"{gender} is not a valid gender")
        else:
            return


def input_aircraft_seating_plan(flight):
    """
    Prompt for and load an aircraft seating plan for a flight

    :param flight: The flight object for which the aircraft seating plan is to be loaded
    """
    while True:
        aircraft_model_and_layout = trimmed_input("Aircraft model and layout e.g. A321:NEO [ENTER to quit] ")
        if len(aircraft_model_and_layout) == 0:
            break

        words = aircraft_model_and_layout.split(":")
        model = words[0].strip()
        layout = words[1].strip() if len(words) > 1 else None

        try:
            flight.load_seating(model, layout)
            break
        except FileNotFoundError:
            print(f"No seating plan found for aircraft model {model} with layout {layout}")


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
