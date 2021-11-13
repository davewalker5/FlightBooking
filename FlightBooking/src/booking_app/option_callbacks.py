from .data_entry import input_passenger


def add_passenger_to_flight(flight):
    """
    Prompt for a new passenger, add them to the specified flight and allocate the next available seat

    :param flight: Flight to add the passenger to
    """
    passenger = input_passenger()
    if passenger:
        flight.add_passenger(passenger)
        flight.allocate_next_empty_seat(passenger["id"])


def save_flight(flight):
    """
    Save the specified flight to a flight data file

    :param flight: Flight to save
    """
    flight.save()


def load_flight():
    # TODO
    pass


def list_seat_allocations(flight):
    # TODO
    pass


def move_passenger(flight):
    # TODO
    pass


def remove_passenger(flight):
    # TODO
    pass


def print_boarding_cards(flight):
    # TODO
    pass
