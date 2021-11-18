import unittest
import datetime
from src.flight_booking import create_passenger


class TestPassenger(unittest.TestCase):
    def test_can_create_passenger(self):
        passenger = create_passenger(
                        "Some One",
                        "M",
                        datetime.datetime(1980, 1, 1),
                        "England",
                        "United Kingdom",
                        "123456789")

        self.assertIsNotNone(passenger["id"])
        self.assertEqual("Some One", passenger["name"])
        self.assertEqual(passenger["gender"], "M")
        self.assertEqual(datetime.datetime(1980, 1, 1).strftime("%Y%m%d"), passenger["dob"])
        self.assertEqual("England", passenger["nationality"])
        self.assertEqual("United Kingdom", passenger["residency"])
        self.assertEqual("123456789", passenger["passport_number"])

    def test_name_cannot_be_none(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    None,
                    "M",
                    datetime.datetime(1980, 1, 1),
                    "England",
                    "United Kingdom",
                    "123456789")

    def test_name_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    "",
                    "M",
                    datetime.datetime(1980, 1, 1),
                    "England",
                    "United Kingdom",
                    "123456789")

    def test_dob_cannot_be_none(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    "Some One",
                    "M",
                    None,
                    "England",
                    "United Kingdom",
                    "123456789")

    def test_dob_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    "Some One",
                    "M",
                    "",
                    "England",
                    "United Kingdom",
                    "123456789")

    def test_nationality_cannot_be_none(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    "Some One",
                    "M",
                    datetime.datetime(1980, 1, 1),
                    None,
                    "United Kingdom",
                    "123456789")

    def test_passenger_dob_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    "Some One",
                    "M",
                    datetime.datetime(1980, 1, 1),
                    "",
                    "United Kingdom",
                    "123456789")

    def test_residency_cannot_be_none(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    "Some One",
                    "M",
                    datetime.datetime(1980, 1, 1),
                    "England",
                    None,
                    "123456789")

    def test_residency_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    "Some One",
                    "M",
                    datetime.datetime(1980, 1, 1),
                    "England",
                    "",
                    "123456789")

    def test_passport_number_cannot_be_none(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    "Some One",
                    "M",
                    datetime.datetime(1980, 1, 1),
                    "England",
                    "United Kingdom",
                    None)

    def test_passport_number_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            _ = create_passenger(
                    "Some One",
                    "M",
                    datetime.datetime(1980, 1, 1),
                    "England",
                    "United Kingdom",
                    "")
