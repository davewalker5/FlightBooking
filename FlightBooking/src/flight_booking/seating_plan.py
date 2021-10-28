import csv
from .utils import get_seating_file_path

ROW_NUMBER_COLUMN = 0
CLASS_COLUMN = 1
SEAT_LETTERS_COLUMN = 2


def read_plan(airline, aircraft, layout=None):
    """
    Read and return an empty seating plan

    :param airline: Name of the airline
    :param aircraft: Aircraft model e.g. A320
    :param layout: Optional airline-specific layout name
    :return: A dictionary of rows where the row number is the key
    """

    # Construct the path to the seating plan file
    file_path = get_seating_file_path(airline, aircraft, layout)

    # Read the rows, throwing away the (mandatory) headers
    with open(file_path, mode="rt", encoding="utf-8") as f:
        # Initialise the CSV reader and skip the headers
        reader = csv.reader(f)
        next(reader, None)

        # The seating plan is represented as a dictionary where the key is the row number
        # and the value is a dictionary containing the class and the seats. The seats are
        # a dictionary where the key is the seat number and the value is the passenger ID,
        # initialised to None here
        return {
            row[ROW_NUMBER_COLUMN]: {
                "class": row[CLASS_COLUMN],
                "seats": {f"{row[ROW_NUMBER_COLUMN]}{seat}": None for seat in row[SEAT_LETTERS_COLUMN]}
            }
            for row in reader
        }


def get_seating_row(plan, seat_number):
    """
    Given a seating plan and a seat number, locate and return the dictionary
    object for the specified row

    :param plan: Seating plan
    :param seat_number: Seat number e.g. 3A
    :return: The row as a dictionary containing seat class and seats keys
    """
    row_number = seat_number[:-1]
    if row_number not in plan.keys():
        raise ValueError(f"Row {row_number} does not exist in the seating plan")

    row = plan[row_number]
    if seat_number not in row["seats"].keys():
        raise ValueError(f"Seat {seat_number} does not exist in row {row_number}")

    return row


def allocate_seat(plan, seat_number, passenger_id):
    """
    Associate the identifying data for a passenger with a seat. If the passenger
    is already associated with a different seat, they are relocated

    :param plan: Seating plan
    :param seat_number: The seat number e.g. 3A
    :param passenger_id: The unique identifying data for a passenger
    """
    if plan is None:
        raise ValueError("Seating plan has not been loaded")

    # Check the seat isn't already allocated
    row = get_seating_row(plan, seat_number)
    current_passenger_id = row["seats"][seat_number]
    if current_passenger_id is not None and current_passenger_id != passenger_id:
        raise ValueError(f"Seat {seat_number} is already allocated")

    # See if the passenger already has a seat allocated. If so, un-allocate it
    current_seat_number = get_allocated_seat(plan, passenger_id)
    if current_seat_number is not None:
        current_seat_row = get_seating_row(plan, current_seat_number)
        current_seat_row["seats"][current_seat_number] = None

    # Allocate the seat to the passenger
    row["seats"][seat_number] = passenger_id


def get_allocated_seat(plan, passenger_id):
    """
    Return the seat number allocated to the passenger

    :param plan: Seating plan
    :param passenger_id: Unique passenger identifier
    :return: Seat number e.g. 3A if the passenger has a seat, otherwise None
    """
    matches = [
        seat_number
        for row in plan.keys()
        for seat_number in plan[row]["seats"]
        if plan[row]["seats"][seat_number] == passenger_id
    ]

    # Result of the comprehension is either an empty or single-entry list
    return matches[0] if len(matches) == 1 else None


def get_unallocated_seats(plan):
    """
    Return a collection of unallocated seats

    :param plan:
    :return:
    """
    return [
        seat_number
        for row in plan.keys()
        for seat_number in plan[row]["seats"]
        if plan[row]["seats"][seat_number] is None
    ]


def copy_seat_allocations(from_plan, to_plan):
    """
    Migrate seat allocations between two seating plans

    :param from_plan: Plan to migrate allocations from
    :param to_plan: Plan to migrate allocations to
    """

    # This returns a list of tuples containing seat numbers and passenger ids
    # for allocated seats
    matches = [
        (seat_number, from_plan[row]["seats"][seat_number])
        for row in from_plan.keys()
        for seat_number in from_plan[row]["seats"]
        if from_plan[row]["seats"][seat_number] is not None
    ]

    if len(matches) > 0:
        # First pass tries to put passengers in the same seats, on the basis that
        # any seating swap is likely to be to a roughly equivalent layout rather
        # than a totally different one (so seating class is deemed not to be an
        # issue)
        unallocated_passengers = []
        for seat_number, passenger_id in matches:
            try:
                allocate_seat(to_plan, seat_number, passenger_id)
            except ValueError:
                unallocated_passengers.append(passenger_id)

        # Second pass now uses a local function to put unallocated passengers
        # in unallocated seats and then calls it using map, passing the lists
        # of un-allocated seats and passengers
        def allocate_unallocated_passenger(seat_number, unallocated_passenger_id):
            try:
                allocate_seat(to_plan, seat_number, unallocated_passenger_id)
                return None
            except ValueError:
                # If we can't allocate a seat, return the passenger ID
                return unallocated_passenger_id

        # Note that the map() function is lazy evaluated so we need to force it to
        # be evaluated in order to process the allocations - this will happen as a
        # result of the comprehension
        unallocated_seats = get_unallocated_seats(to_plan)
        return [passenger_id
                for passenger_id in map(allocate_unallocated_passenger, unallocated_seats, unallocated_passengers)
                if passenger_id is not None]
