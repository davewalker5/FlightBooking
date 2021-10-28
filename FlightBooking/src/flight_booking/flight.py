import re
import json
import datetime
import pkg_resources
from .seating_plan import read_plan, allocate_seat, copy_seat_allocations, get_unallocated_seats, get_allocated_seat
from .utils import get_flight_file_path, get_boarding_card_path, get_lookup_file_path

DEPARTURE_DATE_FORMAT = "%Y%m%d%H%M"

# Set comprehension that uses pkg_resources to identify entry point objects
# for the boarding card printer. The load() method on these returns the module
card_printer_plugins = {
    entry_point.load()
    for entry_point
    in pkg_resources.iter_entry_points("flight_booking.card_generator_plugins")
}

# Build a dictionary of plugins that maps their format string to their callable
# card printer
card_generator_map = {
    module.card_format: module.card_generator
    for module in card_printer_plugins
}


def load_airport_code_lookup():
    """
    Load the file containing the lookups between airport codes and airport names

    :return: A dictionary with airport codes as the keys and names as the values
    """
    code_file = get_lookup_file_path("airport_codes.json")
    with open(code_file, mode="rt", encoding="utf-8") as f:
        json_data = json.load(f)
    return json_data["airport_codes"]


def validate_airport_code(airport_code):
    """
    Validate the format of the specified airport code

    :param airport_code: Airport code to validate
    """
    if airport_code is not None and re.match("[A-Z]{3}$", airport_code) is None:
        raise ValueError(f"{airport_code} is not a valid airport code")


class Flight:
    def __init__(self, **kwargs):
        """
        Initialise an instance of the Flight class. The flight properties should contain:

        airline: Name of the airline
        number: Flight number
        embarkation: Airport code for the point of embarkation
        destination: Airport code for the destination
        departs: Departure time
        duration: Flight duration

        :param kwargs: Flight properties
        """
        self._embarkation = kwargs.get("embarkation", None)
        self._destination = kwargs.get("destination", None)
        validate_airport_code(self._embarkation)
        validate_airport_code(self._destination)
        self._airline = kwargs.get("airline", None)
        self._number = kwargs.get("number", None)
        self._departs = kwargs.get("departs", None)
        self._duration = kwargs.get("duration", None)
        self._passengers = {}
        self._seating = None
        self._aircraft = None
        self._layout = None
        self._capacity = 0

    def load_seating(self, aircraft, layout):
        """
        Given an aircraft name and (optional) layout, load and return the
        seating plan. If there's an existing seating plan with seat allocations,
        those allocations are migrated to the new plan

        :param aircraft: Aircraft model e.g. A320
        :param layout: Airline-specific layout name
        """

        # Read the plan and calculate the capacity as the unallocated seat
        # count after initially loading
        to_plan = read_plan(self._airline, aircraft, layout)
        self._capacity = len(get_unallocated_seats(to_plan))
        self._aircraft = aircraft
        self._layout = layout

        # Migrate existing seat allocations
        if self._seating is not None:
            copy_seat_allocations(self._seating, to_plan)

        self._seating = to_plan

    @property
    def seating_plan(self):
        """
        Return the seating plan for the flight or None if the seating plan
        hasn't been loaded

        :return: The seating plan
        """
        return self._seating

    @property
    def capacity(self):
        """
        Return the total number of seats on the flight

        :return: Total number of seats on the flight
        """
        return self._capacity

    def add_passenger(self, passenger):
        """
        Add a passenger to the flight

        :param passenger:
        """
        if passenger["id"] in self._passengers.keys():
            raise ValueError(f"Passenger {passenger['id']} is already on this flight")
        self._passengers[passenger["id"]] = passenger

    def allocate_seat(self, seat_number, passenger_id):
        """
        Allocate a seat to a passenger. If they already have a seat allocation, they
        are moved

        :param seat_number: Seat number e.g. 3A
        :param passenger_id: Unique passenger identifier
        """
        if passenger_id not in self._passengers.keys():
            raise ValueError(f"Passenger {passenger_id} is not on this flight")
        allocate_seat(self._seating, seat_number, passenger_id)

    def get_allocated_seat(self, passenger_id):
        """
        Return the seat allocation for the passenger with the specified ID

        :param passenger_id: Unique passenger ID
        :return: Seat number e.g. 14B
        """
        return get_allocated_seat(self._seating, passenger_id)

    @property
    def passengers(self):
        """
        Return the passenger collection

        :return: The passengers
        """
        return self._passengers

    def to_json(self):
        """
        Convert the core flight data, passenger list and seating plan to JSON

        :return: Pretty-printed JSON representation of the flight data
        """
        details_json = json.dumps({
            "airline": self._airline,
            "number": self._number,
            "embarkation": self._embarkation,
            "destination": self._destination,
            "departs": self._departs.strftime(DEPARTURE_DATE_FORMAT),
            "duration": self._duration.seconds,
            "aircraft": self._aircraft,
            "layout": self._layout,
            "capacity": self._capacity
        })

        # Construct the JSON, reload it and pretty-print it
        json_data = '{' + f'"details": {details_json}, ' \
                          f'"passengers": {json.dumps(self._passengers)}, ' \
                          f'"seating": {json.dumps(self._seating)} ' + '} '
        loaded = json.loads(json_data)
        return json.dumps(loaded, indent=3, sort_keys=False)

    def save(self):
        """
        Write the flight data to a data file in JSON format
        """
        file_path = get_flight_file_path(self._number, self._departs)
        with open(file_path, mode="wt", encoding="utf-8") as f:
            f.write(self.to_json())

    @property
    def printable_details(self):
        """
        Return a list of printable flight details

        :return: List of details formatted for printing, one detail per entry
        """
        return [
            f"Airline        : {self._airline}",
            f"Flight Number  : {self._number}",
            f"Embarkation    : {self._embarkation}",
            f"Destination    : {self._destination}",
            f"Departs        : {self._departs}",
            f"Duration       : {self._duration}",
            f"Aircraft       : {self._aircraft}",
            f"Seating Layout : {self._layout}",
            f"Capacity       : {self._capacity}"
        ]

    def generate_boarding_cards(self, card_format, gate):
        airport_codes = load_airport_code_lookup()
        generator = card_generator_map[card_format]
        arrival_time = self._departs + self._duration

        for passenger_id in self._passengers:
            # Construct the card details for this passenger and generate the card
            seat_number = get_allocated_seat(self._seating, passenger_id)
            card_data = generator({
                "gate": gate,
                "airline": self._airline,
                "embarkation_name": airport_codes[self._embarkation],
                "embarkation": self._embarkation,
                "departs": self._departs.strftime("%I:%M %p"),
                "destination_name": airport_codes[self._destination],
                "destination": self._destination,
                "arrives": arrival_time.strftime("%I:%M %p"),
                "name": self._passengers[passenger_id]["name"],
                "seat_number": seat_number
            })

            # Write the card to a file
            card_file_path = get_boarding_card_path(self._number, seat_number, self._departs, card_format)
            if isinstance(card_data, str):
                with open(card_file_path, mode="wt", encoding="utf-8") as f:
                    f.write(card_data)
            else:
                with open(card_file_path, mode="wb") as f:
                    f.write(card_data)

    @staticmethod
    def load_flight(number, departs):
        """
        Load a previously saved flight data file

        :param number: The flight number
        :param departs: The departure date and time for the flight
        :return: A new Flight instance initialised from the data in the flight data file
        """
        # Read the JSON file
        file_path = get_flight_file_path(number, departs)
        with open(file_path, mode="rt", encoding="utf-8") as f:
            json_data = json.load(f)

        # Create a new flight
        flight = Flight(
            airline=json_data["details"]["airline"],
            number=json_data["details"]["number"],
            embarkation=json_data["details"]["embarkation"],
            destination=json_data["details"]["destination"],
            departs=datetime.datetime.strptime(json_data["details"]["departs"], DEPARTURE_DATE_FORMAT),
            duration=datetime.timedelta(seconds=int(json_data["details"]["duration"]))
        )

        # Assign the seating layout properties, the passenger list and the seating plan
        flight._aircraft = json_data["details"]["aircraft"]
        flight._layout = json_data["details"]["layout"]
        flight._capacity = json_data["details"]["capacity"]
        flight._passengers = json_data["passengers"]
        flight._seating = json_data["seating"]

        return flight
