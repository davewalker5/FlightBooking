"""
This module defines custom exceptions used by the console booking application package
"""


class InvalidAirportCodeError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self._code = code

    @property
    def code(self):
        return self._code

    def __str__(self):
        return f"'{self.args[0]}' for airport code {self._code}"

    def __repr__(self):
        return f"InvalidAirportCodeError({self.args[0]!r}, {self._code!r})"


class InvalidAircraftSeatingPlanError(Exception):
    def __init__(self, message, aircraft=None, layout=None):
        super().__init__(message)
        self._aircraft = aircraft
        self._layout = layout

    @property
    def aircraft(self):
        return self._aircraft

    @property
    def layout(self):
        return self._layout

    def __str__(self):
        return f"'{self.args[0]}' for aircraft {self._aircraft}, layout {self._layout}"

    def __repr__(self):
        return f"InvalidAircraftSeatingPlanError({self.args[0]!r}, {self._aircraft!r}, {self._layout!r})"
