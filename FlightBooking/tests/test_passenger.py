import unittest
import datetime
from src.flight_booking import *


class TestPassenger(unittest.TestCase):
    def setUp(self) -> None:
        self._passenger = create_passenger(
            "Fred Bloggs",
            "M",
            datetime.datetime(1980, 1, 1),
            "United Kingdom",
            "United Kingdom",
            "123456789")

    def test_create_passenger(self):
        self.assertIsNotNone(self._passenger["id"])
        self.assertEqual(self._passenger["name"], "Fred Bloggs")
        self.assertEqual(self._passenger["gender"], "M")
        self.assertEqual(self._passenger["dob"], datetime.datetime(1980, 1, 1).strftime("%Y%m%d"))
        self.assertEqual(self._passenger["nationality"], "United Kingdom")
        self.assertEqual(self._passenger["residency"], "United Kingdom")
        self.assertEqual(self._passenger["passport_number"], "123456789")
