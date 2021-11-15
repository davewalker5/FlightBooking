"""
This module implements a boarding card generator plugin that can generates and returns boarding card contents in
HTML format using the boarding card template in the “templates” data folder.
"""

import os

card_format = "html"


def card_generator(card_details):
    """
    Generate and return boarding card content in HTML format

    :param card_details: Dictionary of the details for the boarding card
    :return: Boarding card content as HTML
    """
    # Construct the path to the template file and read its contents
    template_path = os.path.join(os.path.dirname(__file__), "templates", "boarding_card.html")
    with open(template_path, mode="rt", encoding="utf-8") as f:
        card = f.read()

    # Perform substitutions for placeholders in the content
    for key in card_details.keys():
        card = card.replace(f"${key}", card_details[key])

    return card



