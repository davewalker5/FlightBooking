"""
This package contains a tutorial/demonstration project implementing a simplified system for creating and managing
airline flight bookings and passengers.

It was inspired by an example in the "Core Python : Getting Started" PluralSight course by Austin Bingham and Robert
Smallshire and is intended as a practice project for the techniques contained in the PluralSight "Core Python" path.

Flights should be created and managed using instances of the Flight class. Passengers should be created using the
create_passenger() function and added to instances of the Flight class using the methods provided by that class. The
Flight class and the create_passenger function are the only intended entry points for consumers of the package.

Under appropriate circumstances, the package may intentionally raise a small number of custom exceptions along with
the ValueError and FileNotFoundError exceptions.
"""

from .flight import Flight
from .passenger import create_passenger
from .exceptions import InsufficientCapacityError, \
    DuplicatePassportNumberError, \
    FlightIsFullError, \
    InvalidOperationError, \
    MissingBoardingCardPluginError

__all__ = ["Flight",
           "create_passenger",
           "InsufficientCapacityError",
           "DuplicatePassportNumberError",
           "FlightIsFullError",
           "InvalidOperationError",
           "MissingBoardingCardPluginError"]
