import unittest
from src.flight_booking_html_generator.boarding_card_generator import card_generator


class TestBoardingCardGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self._card_details = {
                "gate" : "28A",
                "airline": "EasyJet",
                "embarkation_name": "Alicante",
                "embarkation": "ALC",
                "departs": "09:45 pm",
                "destination_name": "London Gatwick",
                "destination": "LGW",
                "arrives": "12:00 am",
                "name": "Some Passenger",
                "seat_number": "5D"
            }

    def test_card_contains_all_placeholder_values(self):
        card_data = card_generator(self._card_details)
        for value in self._card_details.values():
            self.assertIn(value, card_data, value)
