"""
This module defines custom exceptions used by the flight booking package
"""


class InsufficientCapacityError(Exception):
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
        return f"InsufficientCapacityError({self.args[0]!r}, {self._aircraft!r}, {self._layout!r})"


class DuplicatePassportNumberError(Exception):
    def __init__(self, message, number=None):
        super().__init__(message)
        self._number = number

    @property
    def number(self):
        return self._number

    def __str__(self):
        return f"'{self.args[0]}' for passport number {self._number}"

    def __repr__(self):
        return f"DuplicatePassportNumberError({self.args[0]!r}, {self._number!r})"


class MissingBoardingCardPluginError(Exception):
    def __init__(self, message, card_format=None):
        super().__init__(message)
        self._card_format = card_format

    @property
    def card_format(self):
        return self._card_format

    def __str__(self):
        return f"'{self.args[0]}' for card format '{self._card_format}'"

    def __repr__(self):
        return f"MissingBoardingCardPluginError({self.args[0]!r}, {self._card_format!r})"


class FlightIsFullError(Exception):
    pass


class InvalidOperationError(Exception):
    pass
