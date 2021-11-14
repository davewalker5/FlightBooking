"""
This module contains the definition for the Flight class, instances of which are used to manage all the properties
of a flight (including the seating plan, passenger details and seat allocations) and to generate boarding card data
files.

Instances of a Flight can be saved to JSON-formatted data files and subsequently re-created from the data held in
those files.

BOARDING CARDS:

Plugins are used to generate boarding cards in different formats. Plugins capable of generating boarding cards should
extend the following entry point:

flight_booking.card_generator_plugins

They should provide the follow:

card_format - the format in which boarding card data is generated e.g. html, pdf, txt
card_generator - a function that generates and returns boarding card data in the format indicated by the card_format

The card_generator function receives a dictionary of properties, as follows:

gate - departure gate number
airline - name of the airline
embarkation_name - the name of the embarkation airport
embarkation - 3-letter IATA code for the destination airport
departs - departure time (local) formatted using the 12-hour clock with an am or pm suffix
destination_name - the name of the destination airport
destination- 3-letter IATA code for the destination airport
arrives - arrival time (local) formatted using the 12-hour clock with an am or pm suffix
name - the passenger name
seat_number - the seat number
"""

import json
import datetime
import pkg_resources
from .seating_plan import read_plan, \
    allocate_seat, \
    copy_seat_allocations, \
    get_allocated_seat, \
    get_unallocated_seats, \
    get_seat_allocations, \
    clear_allocation
from .utils import get_flight_file_path, get_boarding_card_path
from .airport import get_airport
from .exceptions import InsufficientCapacityError, \
    FlightIsFullError, \
    DuplicatePassportNumberError, \
    InvalidOperationError, \
    MissingBoardingCardPluginError
import pytz

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


class Flight:
    def __init__(self, embarkation, destination, airline, number, departs, duration):
        """
        Initialise an instance of the Flight class. The flight properties should contain:

        :param embarkation: Airport code for the point of embarkation
        :param destination: Airport code for the destination airport
        :param airline: Name of the airline
        :param number: Flight number
        :param departs: Departure time
        :param duration: Flight duration
        """
        self._embarkation = get_airport(embarkation)
        self._destination = get_airport(destination)
        self._airline = airline
        self._number = number

        # Store the departure date and time as UTC
        if departs.tzinfo is None:
            departs_with_tz = pytz.timezone(self._embarkation["tz"]).localize(departs)
            self._departs = departs_with_tz.astimezone(pytz.utc)
        else:
            self._departs = departs.astimezone(pytz.utc)

        self._duration = duration
        self._passengers = {}
        self._seating = None

    def __repr__(self):
        return f"{type(self).__name__}(" \
               f"embarkation={self._embarkation['code']}, " \
               f"destination={self._destination['code']}, " \
               f"airline={self._airline!r}, " \
               f"number={self._number!r}, " \
               f"departs={self._departure_time_repr()}, " \
               f"duration={self._duration!r}" \
               f")"

    def __str__(self):
        # As __format__ hasn't been overridden, it'll delegate to __str__ and produce the same output
        return f"{self._airline} {self._number} " \
               f"{self._embarkation['code']} to {self._destination['code']}, " \
               f"{self.departs_localtime.strftime('%d-%b-%Y %H:%M %p')}"

    def _departure_time_repr(self):
        """
        For dates with timezones, repr(x) doesn't return something that can be used to reconstruct a datetime using
        the Python REPL. This method does, for the departure date and time

        :return: repr() for the departure date and time
        """
        return f"datetime.datetime({self._departs.year}, " \
               f"{self._departs.month}, " \
               f"{self._departs.day}, " \
               f"{self._departs.hour}, " \
               f"{self._departs.minute}, " \
               f"tzinfo=datetime.timezone.utc)"

    @property
    def embarkation_airport_code(self):
        """
        Return the airport code for the embarkation airport

        :return: IATA 3-letter airport code for the point of embarkation
        """
        return self._embarkation["code"]

    @property
    def destination_airport_code(self):
        """
        Return the airport code for the destination airport

        :return: IATA 3-letter airport code for the destination airport

        :return:
        """
        return self._destination["code"]

    @property
    def airline(self):
        """
        Name of the airline

        :return: The name of the airline
        """
        return self._airline

    @property
    def number(self):
        """
        Flight number

        :return: The flight number
        """
        return self._number

    @property
    def aircraft(self):
        """
        The aircraft model

        :return: The aircraft model or None if a seating plan hasn't been loaded
        """
        return self._seating["aircraft"] if self._seating else None

    @property
    def layout(self):
        """
        The seating plan layout for the aircraft

        :return: The aircraft layout or None if a seating plan hasn't been loaded
        """
        return self._seating["layout"] if self._seating else None

    @property
    def seating_plan(self):
        """
        Return the seating plan for the flight or None if the seating plan
        hasn't been loaded

        :return: The seating plan
        """
        return self._seating

    @property
    def departure_date(self):
        """
        The UTC departure date

        :return: The UTC departure date with no time information
        """
        return self._departs.date()

    @property
    def departs_localtime(self):
        """
        Return the departure date and time converted to localtime for the point of embarkation

        :return: The departure time converted to localtime for the point of embarkation
        """
        embarkation_timezone = pytz.timezone(self._embarkation["tz"])
        return self._departs.astimezone(embarkation_timezone)

    @property
    def arrives_localtime(self):
        """
        The arrival date and time converted to localtime for the destination

        :return: The arrival date and time converted to localtime for the destination
        """
        arrives_utc = self._departs + self._duration
        destination_timezone = pytz.timezone(self._destination["tz"])
        return arrives_utc.astimezone(destination_timezone)

    @property
    def duration(self):
        """
        Return a tuple representing the flight duration

        :return: (hours, minutes)
        """
        return self._duration.seconds // 3600, (self._duration.seconds // 60) % 60

    @property
    def capacity(self):
        """
        Return the total number of seats on the flight

        :return: Total number of seats on the flight or 0 if a seating plan hasn't been loaded
        """
        return self._seating["capacity"] if self._seating else 0

    @property
    def available_capacity(self):
        """
        Return the number of unallocated seats available on the flight

        :return: The number of available seats or 0 if a seating plan hasn't been loaded
        """
        return self.capacity - len(self._passengers) if self._seating else 0

    @property
    def passengers(self):
        """
        Return the passenger collection

        :return: The passengers
        """
        return self._passengers

    @property
    def printable_details(self):
        """
        Return a list of printable flight details

        :return: List of details formatted for printing, one detail per entry
        """
        return [
            f"Airline        : {self._airline}",
            f"Flight Number  : {self._number}",
            f"Embarkation    : {self._embarkation['code']}",
            f"Destination    : {self._destination['code']}",
            f"Departs        : {self.departs_localtime.strftime('%Y-%m-%d %H:%M:00')}",
            f"Duration       : {self._duration}",
            f"Aircraft       : {self.aircraft}",
            f"Seating Layout : {self.layout}",
            f"Capacity       : {self.capacity}"
        ]

    def load_seating(self, aircraft, layout):
        """
        Given an aircraft name and (optional) layout, load and return the
        seating plan. If there's an existing seating plan with seat allocations,
        those allocations are migrated to the new plan

        :param aircraft: Aircraft model e.g. A320
        :param layout: Airline-specific layout name
        """
        to_plan = read_plan(self._airline, aircraft, layout)
        if to_plan["capacity"] < len(self.passengers):
            raise InsufficientCapacityError(
                f"{aircraft} layout {layout} does not have enough seats for the current passengers",
                aircraft=aircraft,
                layout=layout
            )

        if self._seating is not None:
            copy_seat_allocations(self._seating, to_plan)

        self._seating = to_plan

    def add_passenger(self, passenger):
        """
        Add a passenger to the flight

        :param passenger:
        """
        if passenger["id"] in self._passengers.keys():
            raise ValueError(f"Passenger {passenger['id']} is already on this flight")

        if self._seating and len(self._passengers) == self.capacity:
            raise FlightIsFullError("The flight is full")

        passport_numbers = [p["passport_number"] for p in self._passengers.values()]
        number = passenger["passport_number"]
        if number in passport_numbers:
            raise DuplicatePassportNumberError(
                f"Passenger with passport number {number} is already on this flight",
                number=number
            )

        self._passengers[passenger["id"]] = passenger

    def remove_passenger(self, passenger_id):
        """
        Remove the passenger with the specified ID from the flight, also removing their seat allocation

        :param passenger_id: Unique identifier for the passenger to remove
        """
        if self._seating is not None:
            seat_number = get_allocated_seat(self._seating, passenger_id)
            if seat_number is not None:
                clear_allocation(self._seating, seat_number)
        del self.passengers[passenger_id]

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

    def allocate_next_empty_seat(self, passenger_id):
        """
        Allocate the next unallocated seat to the passenger with the specified ID, filling the plane from
        row by row from front to back

        :param passenger_id: Unique passenger identifier
        """
        if not self._seating:
            # Empty sequence or None will be falsy
            raise InvalidOperationError("Cannot allocate the next seat if there is no seating plan")

        next_seat = get_unallocated_seats(self._seating)[0]
        self.allocate_seat(next_seat, passenger_id)

    def get_allocated_seat(self, passenger_id):
        """
        Return the seat allocation for the passenger with the specified ID

        :param passenger_id: Unique passenger ID
        :return: Seat number e.g. 14B
        """
        return get_allocated_seat(self._seating, passenger_id) if self._seating else None

    def get_all_seat_allocations(self):
        """
        Return a sequence representing the seat allocations for all passengers with allocations

        :return: A sequence of (seat-number, passenger) tuples for allocated seats
        """
        if self._seating is None or len(self._passengers) == 0:
            return None

        return [(seat_number, self._passengers[pid])
                for seat_number, pid
                in get_seat_allocations(self._seating)]

    def to_json(self):
        """
        Convert the core flight data, passenger list and seating plan to JSON

        :return: Pretty-printed JSON representation of the flight data
        """
        details_json = json.dumps({
            "airline": self._airline,
            "number": self._number,
            "embarkation": self._embarkation["code"],
            "destination": self._destination["code"],
            "departs": self._departs.strftime(DEPARTURE_DATE_FORMAT),
            "duration": self._duration.seconds,
            "aircraft": self.aircraft,
            "layout": self.layout,
            "capacity": self.capacity
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

    def generate_boarding_cards(self, card_format, gate):
        """
        Generate boarding cards in the specified format

        :param card_format: The format for the generated card data file
        :param gate: The gate number the flight will depart from
        """
        allocations = self.get_all_seat_allocations()
        if not allocations:
            # An empty sequence or None will be falsy
            raise InvalidOperationError("Cannot print boarding cards if the flight has no seat allocations")

        try:
            generator = card_generator_map[card_format]
        except KeyError as e:
            raise MissingBoardingCardPluginError(
                f"Boarding card plugin not registered for format {card_format}",
                card_format=card_format
            ) from e

        for seat_number, passenger in allocations:
            # Construct the card details for this passenger and generate the card
            card_data = generator({
                "gate": gate,
                "airline": self._airline,
                "embarkation_name": self._embarkation["name"],
                "embarkation": self._embarkation["code"],
                "departs": self.departs_localtime.strftime("%I:%M %p"),
                "destination_name": self._destination["name"],
                "destination": self._destination["code"],
                "arrives": self.arrives_localtime.strftime("%I:%M %p"),
                "name": passenger["name"],
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

        # Assign the passenger list and the seating plan
        flight._passengers = json_data["passengers"]
        flight._seating = json_data["seating"]

        return flight
