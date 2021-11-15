"""
This module contains methods for validating options for the console booking application package, selecting an option
and invoking the handler for the selected option
"""

import inspect
from .data_entry import trimmed_input
from flight_booking.flight import Flight


def validate_option_definition(definition):
    """
    Given an option  definition from the options dictionary, check it's properly configured using
    assertions and add required information for calling the associated callable

    :param definition: Dictionary containing the option definition
    """
    # Validate basic details
    assert isinstance(definition, dict)
    assert "description" in definition
    assert len(definition["description"]) > 0
    assert "function" in definition

    # Validate the callable associated with the definition
    function = definition["function"]
    if function is not None:
        assert callable(function)
        signature = inspect.signature(function)

        # See if it has a parameter named flight and, if so, set the flag in the
        # definition
        definition["has_flight_parameter"] = "flight" in signature.parameters


def validate_all_options(options):
    """
    Validate all the options in an options dictionary

    :param options: A dictionary of option definitions
    """
    assert isinstance(options, dict)
    for definition in options.values():
        validate_option_definition(definition)


def display_options(options_map):
    """
    Display the available booking application options
    """
    max_option_length = max([len(k) for k in options_map.keys()])
    for option in options_map:
        print(f"{option.rjust(max_option_length)} - {options_map[option]['description']}")


def input_option(options_map):
    """
    Prompt for and return an option from the options map

    :return: The option as a dictionary containing the method to call to act on the selected option
    """
    selection = trimmed_input("Option: ").upper()
    if selection not in options_map:
        raise ValueError(f"{selection} is not an available option")

    return options_map[selection]


def call_option_function(option, flight):
    """
    Call the function associated with the specified option

    :param option: Option definiton (dictionary)
    :param flight: Current flight object
    :return: Either a new flight or the current flight object
    """
    if option["has_flight_parameter"]:
        if flight:
            result = option["function"](flight=flight)
        else:
            raise ValueError(f"'{option['description']}' requires a valid flight")
    else:
        result = option["function"]()

    return result if isinstance(result, Flight) else flight
