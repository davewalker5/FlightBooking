import os
import shutil
import datetime
from pprint import pprint as pp
from flight_booking import *
from flight_booking.utils import get_data_folder


def create_flight():
    """
    Create a flight with a seating plan and one passenger

    :return: Instance of Flight()
    """
    # Create a flight
    flight = Flight(
        airline="EasyJet",
        number="U25142",
        embarkation="ALC",
        destination="LGW",
        departs=datetime.datetime(2021, 10, 18, 21, 45, 0),
        duration=datetime.timedelta(hours=2, minutes=15)
    )

    # Load the seating plan for the aircraft
    flight.load_seating("A320", "1")

    # Create a passenger and add them to the flight
    passenger = create_passenger(
        "Some Passenger",
        "M",
        datetime.datetime(1980, 1, 1),
        "United Kingdom",
        "United Kingdom",
        "123456789")
    flight.add_passenger(passenger)
    return flight


def allocate_seat(flight, passenger_id, seats):
    """
    Allocate each seat in the seats iterable to the specified passenger, in turn. This
    simulates an initial seat allocation followed by requests to move the passenger around

    :param flight: Instance of Flight()
    :param passenger_id: Unique passenger ID
    :param seats: Iterable of seat numbers
    """
    for seat_number in seats:
        flight.allocate_seat(seat_number, passenger_id)
        print(f"Passenger {passenger_id} is in seat {flight.get_allocated_seat(passenger_id)}")


def reload_flight(flight, passenger_id):
    """
    Move the passenger to a seat that doesn't exist on a new seating plan then
    load that plan and show that the passenger's been automatically relocated

    :param flight: Instance of Flight()
    :param passenger_id: Unique passenger ID
    """
    allocate_seat(flight, passenger_id, ["1D"])
    flight.load_seating("A321", "neo")
    print(f"Passenger {passenger_id} is in seat {flight.get_allocated_seat(passenger_id)}")


def remove_files(folder):
    """
    Remove all files from the specified data sub-folder

    :param folder: Sub-folder to clean
    """
    folder_to_clean = get_data_folder(folder)
    for filename in os.listdir(folder_to_clean):
        file_path = os.path.join(folder_to_clean, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting {file_path} : {e}")


def run_example():
    """
    Run an example that exercises the flight booking application
    """
    # Remove boarding card and saved flight files from previous runs
    remove_files("boarding_cards")
    remove_files("flights")

    # Create a flight, get the unique ID for the  first (and only) passenger on the flight and allocate
    # a seat to the passenger (moving them around a bit) before saving the flight
    original = create_flight()
    pid = next(iter(original.passengers.values()))["id"]
    allocate_seat(original, pid, ["2A", "2F", "5B"])
    original.save()

    # Reload the flight into a new instance and dump the flight details
    loaded = Flight.load_flight("U25142", datetime.datetime(2021, 10, 18, 21, 45, 0))
    print("\n".join(loaded.printable_details))

    # Dump the passenger list
    print("\nPassengers:\n")
    passengers = loaded.passengers
    pp(passengers)

    # Dump the seating plan
    print("\nSeating Plan:\n")
    pp(loaded.seating_plan)

    # Move a passenger to a new seat, to confirm the reloaded dictionaries are constructed
    # as expected
    passenger_id = list(passengers)[0]
    loaded.allocate_seat("5B", passenger_id)
    pp(loaded.seating_plan)

    try:
        # If the boarding card plugin hasn't been installed in the project's venv
        # then these calls will throw an exception, which we sink
        loaded.generate_boarding_cards("html", "28A")
        loaded.generate_boarding_cards("pdf", "28A")
    except KeyError:
        print("Boarding card plugins not installed")


if __name__ == "__main__":
    run_example()
