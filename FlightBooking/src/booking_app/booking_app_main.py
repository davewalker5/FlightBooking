"""
This module defines the main entry point for the console booking application package
"""

from .option_handler import validate_all_options, display_options, input_option, call_option_function
from .option_callbacks import *
from .data_entry import input_flight, input_aircraft_seating_plan
from flight_booking import InsufficientCapacityError, \
    FlightIsFullError, \
    DuplicatePassportNumberError, \
    InvalidOperationError, \
    SeatingPlanNotFoundError, \
    MissingBoardingCardPluginError, \
    AirportCodeNotFoundError

# The available options are represented as a dictionary in which the key is the input
# the user must provide to select the option and the value is a dictionary with a
# description of the option and a function that's called when the option is selected
options_map = {
    "1": {"description": "Create Flight", "function": input_flight},
    "2": {"description": "Load seating plan", "function": input_aircraft_seating_plan},
    "3": {"description": "Add passenger", "function": add_passenger_to_flight},
    "4": {"description": "List passengers", "function": list_passengers_on_flight},
    "5": {"description": "List seat allocations", "function": list_seat_allocations},
    "6": {"description": "Allocate seat", "function": allocate_seat},
    "7": {"description": "Remove passenger", "function": remove_passenger},
    "8": {"description": "Print boarding cards", "function": print_boarding_cards},
    "9": {"description": "Save flight", "function": save_flight},
    "10": {"description": "Load flight", "function": load_flight},
    "Q": {"description": "Quit", "function": None},
}


def main():
    """
    Main loop for the console-based flight booking application
    """
    validate_all_options(options_map)

    flight = None
    while True:
        print()
        if flight:
            list_flight_details(flight)
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
            else:
                try:
                    print()
                    flight = call_option_function(selected, flight)
                except (ValueError,
                        FileNotFoundError,
                        InsufficientCapacityError,
                        FlightIsFullError,
                        DuplicatePassportNumberError,
                        InvalidOperationError,
                        SeatingPlanNotFoundError,
                        MissingBoardingCardPluginError,
                        AirportCodeNotFoundError
                        ) as e:
                    print(e)
