from .option_handler import validate_all_options, display_options, input_option, call_option_function
from .data_entry import *

# The available options are represented as a dictionary in which the key is the input
# the user must provide to select the option and the value is a dictionary with a
# description of the option and a function that's called when the option is selected
options_map = {
    "1": {"description": "Create Flight", "function": input_flight},
    "2": {"description": "Load seating plan", "function": input_aircraft_seating_plan},
    "3": {"description": "Add passenger", "function": None},
    "4": {"description": "List seat allocations", "function": None},
    "5": {"description": "Move passenger", "function": None},
    "6": {"description": "Remove passenger", "function": None},
    "7": {"description": "Print boarding cards", "function": None},
    "8": {"description": "Save flight", "function": None},
    "9": {"description": "Load flight", "function": None},
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
        print(f"Current flight: {flight}")
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
