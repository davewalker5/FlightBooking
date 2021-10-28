import pytest
from src.flight_booking_pdf_generator.boarding_card_generator import card_generator


@pytest.fixture
def card_details():
    card_details = {
        "gate": "28A",
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

    # Using yield means the tear down actions can be placed after the yield and the
    # test will tidy up after itself
    yield card_details


@pytest.mark.slow
def test_card_is_generated(card_details):
    card_data = card_generator(card_details)
    assert card_data is not None
