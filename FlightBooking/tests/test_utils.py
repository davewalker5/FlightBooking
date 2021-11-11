import unittest
import datetime
from src.flight_booking.utils import *


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        os.environ[FLIGHT_BOOKING_DATA_FOLDER_ENV] = "tmp"

    def test_get_data_folder_with_env_var(self):
        expected = os.path.join("tmp", "flights")
        self.assertEqual(expected, get_data_folder("flights"))

    def test_get_data_folder_without_env_var(self):
        # With the environment not set, the data folder reverts to the "data" folder in the project
        del os.environ[FLIGHT_BOOKING_DATA_FOLDER_ENV]
        expected = os.path.join("data", "flights")
        self.assertTrue(expected in get_data_folder("flights"))

    def test_get_flight_file_path(self):
        file_path = get_flight_file_path("U28549", datetime.datetime(2021, 11, 20, 10, 45, 0))
        expected = os.path.join("tmp", "flights", "u28549_20211120.json")
        self.assertEqual(expected, file_path)

    def test_get_boarding_card_path(self):
        file_path = get_boarding_card_path("U28549", "5B", datetime.datetime(2021, 11, 20, 10, 45, 0), "pdf")
        expected = os.path.join("tmp", "boarding_cards", "u28549_5b_20211120.pdf")
        self.assertEqual(expected, file_path)

    def test_get_lookup_file_path(self):
        file_path = get_lookup_file_path("lookup_file.dat")
        expected = os.path.join("tmp", "lookups", "lookup_file.dat")
        self.assertEqual(expected, file_path)
