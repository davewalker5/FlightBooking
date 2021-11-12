import datetime
from .airport import get_airport
from .flight import Flight


def input_airport_code(airport_type):
    """
    Prompt for an airport code and return the corresponding airport object

    :param airport_type: Text used in the prompt to indicate embarkation or destination airport
    :return: A dictionary of airport properties or None if cancelled
    """
    while True:
        code = input(f"{airport_type} airport code [ENTER to quit] ").strip()
        if len(code) > 0:
            try:
                airport = get_airport(code)
                return airport
            except KeyError:
                print(f"Airport code {code} is not recognised")
        else:
            return


def input_airline():
    """
    Prompt for and return an airline name

    :return: Airline name or an empty string to cancel
    """
    return input("Airline [ENTER to quit] ").strip()


def input_flight_number():
    """
    Prompt for and return a flight number

    :return: Flight number or an empty string to cancel
    """
    return input("Flight number [ENTER to quit] ").strip()


def input_departure_date():
    """
    Prompt for the departure date

    :return: The departure date as a date() object or None if cancelled
    """
    while True:
        departure_date_string = input("Departure date DD/MM/YYYY [ENTER to quit] ").strip()
        if len(departure_date_string) > 0:
            try:
                departure_date = datetime.datetime.strptime(departure_date_string, "%d/%m/%Y").date()
                return departure_date
            except ValueError:
                print(f"{departure_date_string} is not a valid date")
        else:
            return


def input_departure_time():
    """
    Prompt for the departure time

    :return: The departure time as a time() object or None if cancelled
    """
    while True:
        departure_time_string = input("Departure time in 24-hour format HH:MM [ENTER to quit] ").strip()
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
        duration_string = input("Duration HH:MM [ENTER to quit] ")
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


def input_aircraft_seating_plan(flight):
    """
    Prompt for and load an aircraft seating plan for a flight

    :param flight: The flight object for which the aircraft seating plan is to be loaded
    """
    while True:
        aircraft_model_and_layout = input("Aircraft model and layout e.g. A321:NEO [ENTER to quit] ")
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

    airline = input_airline()
    if not airline:
        return

    flight_number = input_flight_number()
    if not flight_number:
        return

    departure_date = input_departure_date()
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
