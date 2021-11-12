import unittest
import datetime
from src.flight_booking import *


class TestPassenger(unittest.TestCase):
    def setUp(self) -> None:
        self._passenger = create_passenger(
            "Fred Bloggs",
            "M",
            datetime.datetime(1980, 1, 1),
            "England",
            "United Kingdom",
            "123456789")

    def test_create_passenger(self):
        self.assertIsNotNone(self._passenger["id"])
        self.assertEqual("Fred Bloggs", self._passenger["name"])
        self.assertEqual(self._passenger["gender"], "M")
        self.assertEqual(datetime.datetime(1980, 1, 1).strftime("%Y%m%d"), self._passenger["dob"])
        self.assertEqual("England", self._passenger["nationality"])
        self.assertEqual("United Kingdom", self._passenger["residency"])
        self.assertEqual("123456789", self._passenger["passport_number"])
