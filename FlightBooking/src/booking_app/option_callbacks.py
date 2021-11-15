"""
This module contains callback methods for handling the options selected in the console booking application
"""

from .data_entry import input_passenger, trimmed_input, input_future_date, select_passenger, list_passengers
from flight_booking import Flight


def add_passenger_to_flight(flight):
    """
    Prompt for a new passenger, add them to the specified flight and allocate the next available seat

    :param flight: Flight to add the passenger to
    """
    passenger = input_passenger()
    if passenger:
        flight.add_passenger(passenger)
        print(f"Passenger {passenger['name']} has been added to the flight")


def list_passengers_on_flight(flight):
    """
    List the passengers on a flight

    :param flight: Flight for which to list passengers
    """
    list_passengers(flight.passengers)


def save_flight(flight):
    """
    Save the specified flight to a flight data file

    :param flight: Flight to save
    """
    flight.save()
    print("The flight has been saved")


def load_flight():
    """
    Load a flight from a  flight data file

    :return: The loaded flight or None if cancelled
    """
    flight_number = trimmed_input("Flight number [ENTER to quit] ")
    if not flight_number:
        return

    departure_date = input_future_date("Departure date")
    if not departure_date:
        return

    return Flight.load_flight(flight_number, departure_date)


def list_flight_details(flight):
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


def list_seat_allocations(flight):
    """
    List all the current seat allocations for a flight

    :param flight: Flight to list allocations for
    """
    allocations = flight.get_all_seat_allocations()
    if not allocations:
        print("There are no seat allocations")
        return

    for seat_number, passenger in allocations:
        print(f"{seat_number.rjust(4)} {passenger['name']} - {passenger['passport_number']}")


def allocate_seat(flight):
    """
    Prompt for a passenger and a seat to allocate to them

    :param flight: Flight on which to perform the allocation
    """
    passenger = select_passenger(flight.passengers)
    if passenger is not None:
        seat_number = trimmed_input("Seat number [ENTER to quit] ")
        if seat_number:
            flight.allocate_seat(seat_number, passenger["id"])
            print(f"Seat {seat_number} has been allocated to {passenger['name']}")


def remove_passenger(flight):
    """
    Select a passenger and remove them from the flight

    :param flight: Flight to remove a passenger from
    """
    passenger = select_passenger(flight.passengers)
    if passenger is not None:
        flight.remove_passenger(passenger["id"])
        print(f"Passenger {passenger['name']} has been removed")


def print_boarding_cards(flight):
    """
    Prompt for a gate number and generate the boarding cards for a specified flight

    :param flight: Flight to generate boarding cards for
    """
    gate = trimmed_input("Gate number [ENTER to quit] ")
    if gate:
        flight.generate_boarding_cards("pdf", gate)
        print(f"Boarding cards have been generated for gate {gate}")
