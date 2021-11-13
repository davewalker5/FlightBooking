from .option_handler import validate_all_options, display_options, input_option, call_option_function
from .option_callbacks import *
from .data_entry import input_flight, \
    input_aircraft_seating_plan, \
    InvalidAircraftSeatingPlanError, \
    InvalidAirportCodeError

# The available options are represented as a dictionary in which the key is the input
# the user must provide to select the option and the value is a dictionary with a
# description of the option and a function that's called when the option is selected
options_map = {
    "1": {"description": "Create Flight", "function": input_flight},
    "2": {"description": "Load seating plan", "function": input_aircraft_seating_plan},
    "3": {"description": "Add passenger", "function": add_passenger_to_flight},
    "4": {"description": "List seat allocations", "function": list_seat_allocations},
    "5": {"description": "Move passenger", "function": move_passenger},
    "6": {"description": "Remove passenger", "function": remove_passenger},
    "7": {"description": "Print boarding cards", "function": print_boarding_cards},
    "8": {"description": "Save flight", "function": save_flight},
    "9": {"description": "Load flight", "function": load_flight},
    "Q": {"description": "Quit", "function": None},
}


def print_header(flight):
    """
    Print the header containing the flight details

    :param flight: Flight to display details for
    """
    flight_details = f"Current flight  : {flight}"
    border = "=" * len(flight_details)

    print(border)
    print(flight_details)
    print(f"Passenger count : {len(flight.passengers)}")

    if flight.aircraft:
        print(f"Aircraft        : {flight.aircraft}")
        if flight.layout:
            print(f"Layout          : {flight.layout}")
        print(f"Capacity        : {flight.capacity}")
        print(f"Available seats : {flight.available_capacity}")

    print(border)


def main():
    """
    Main loop for the console-based flight booking application
    """
    validate_all_options(options_map)

    flight = None
    while True:
        if flight:
            print_header(flight)
            print()

        display_options(options_map)
        print()

        try:
            selected = input_option(options_map)
        except ValueError as e:
            print(e)
        else:
            if selected["function"] is None:
                break
            try:
                flight = call_option_function(selected, flight)
            except InvalidAircraftSeatingPlanError as e:
                print(e)
            except InvalidAirportCodeError as e:
                print(e)
            except ValueError as e:
                print(e)
