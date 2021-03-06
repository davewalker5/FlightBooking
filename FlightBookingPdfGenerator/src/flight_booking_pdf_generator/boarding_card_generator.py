"""
This module implements a boarding card generator plugin that can generates and returns boarding card contents in
PDF format.

The "templates" data folder contains a boarding card template in HTML format. Boarding card data is first generated
in HTML format and then converted to PDF format to be returned to the caller
"""
import os
import pdfkit

card_format = "pdf"


def card_generator(card_details):
    """
    Generate and return boarding card content in PDF format

    :param card_details: Dictionary of the details for the boarding card
    :return: Boarding card content as PDF
    """
    # Construct the path to the template file and read its contents
    template_path = os.path.join(os.path.dirname(__file__), "templates", "boarding_card.html")
    with open(template_path, mode="rt", encoding="utf-8") as f:
        card = f.read()

    # Perform substitutions for placeholders in the content
    for key in card_details.keys():
        card = card.replace(f"${key}", card_details[key])

    return pdfkit.from_string(card, None)
