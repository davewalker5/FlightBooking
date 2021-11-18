"""
This module defines custom exceptions used by the console booking application package
"""

from flight_booking import SeatingPlanNotFoundError


class InvalidAircraftSeatingPlanError(SeatingPlanNotFoundError):
    pass
