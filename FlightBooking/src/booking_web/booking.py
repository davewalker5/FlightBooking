"""
This module implements a Flask-based web application based on the functionality provided by the "flight_booking"
package.

The site is not responsive but the Bootstrap customizer has been used to generate a cut-down version of bootstrap
to provide button and form element styling.
"""

from flask import Flask, render_template, redirect, request, session
from flight_booking import InvalidOperationError, SeatingPlanNotFoundError, AirportCodeNotFoundError
from .model import booking_model

app = Flask("Flight Booking")
app.secret_key = b'some secret key'

options_map = [
    {
        "description": "Create",
        "view": "create_new_flight",
        "requires_flight": False
    },
    {
        "description": "Seating",
        "view": "load_seating_plan",
        "requires_flight": True
    },
    {
        "description": "Add passenger",
        "view": "add_passenger_to_flight",
        "requires_flight": True
    },
    {
        "description": "List passengers",
        "view": "list_passengers",
        "requires_flight": True
    },
    {
        "description": "Boarding cards",
        "view": "print_boarding_cards",
        "requires_flight": True
    },
    {
        "description": "Save",
        "view": "save_flight",
        "requires_flight": True
    },
    {
        "description": "Load",
        "view": "load_flight",
        "requires_flight": False
    },
    {
        "description": "Close",
        "view": "close_flight",
        "requires_flight": True
    },
    {
        "description": "Home",
        "view": "home",
        "requires_flight": False,
        "is_home_link": True
    }
]


@app.route("/")
def home():
    """
    Serve the home page for the flight booking site, listing the available options

    :return: HTML for the home page
    """
    error = session.pop("error") if "error" in session else None
    message = session.pop("message") if "message" in session else None
    return render_template("home.html",
                           options_map=options_map,
                           flight=booking_model.flight,
                           error=error,
                           message=message)


@app.route("/create_new_flight", methods=["GET", "POST"])
def create_new_flight():
    """
    Serve the page to prompt for the details for a new flight and create the flight when the form is submitted

    :return: The HTML for the flight details page or a response object redirecting to /
    """
    if request.method == "POST":
        try:
            booking_model.create_flight(request.form["embarkation"],
                                        request.form["destination"],
                                        request.form["airline"],
                                        request.form["number"],
                                        request.form["departure_date"],
                                        request.form["departure_time"],
                                        request.form["duration"])
        except (AirportCodeNotFoundError, ValueError) as e:
            return render_template("create_flight.html", error=e)
        else:
            return redirect("/")
    else:
        return render_template("create_flight.html", error=None)


@app.route("/create_dummy_flight")
def create_dummy_flight():
    """
    Create a fully populated dummy flight for testing purposes

    :return: Response object redirecting to /
    """
    booking_model.create_dummy_flight(10, "A321", "neo", True)
    return redirect("/")


@app.route("/load_seating_plan", methods=["GET", "POST"])
def load_seating_plan():
    """
    Serve the page to prompt for the details for a seating plan and load the plan when the form is submitted

    :return: The HTML for the seating plan details page or a response object redirecting to /
    """
    if request.method == "POST":
        layout = request.form["layout"] if len(request.form["layout"]) > 0 else None
        try:
            booking_model.flight.load_seating(request.form["aircraft"], layout)
        except SeatingPlanNotFoundError as e:
            return render_template("load_seating_plan.html", error=e)
        else:
            return redirect("/")
    else:
        return render_template("load_seating_plan.html", error=None)


@app.route("/add_passenger_to_flight", methods=["GET", "POST"])
def add_passenger_to_flight():
    """
    Serve the page to prompt for the details for a new passenger and add the passenger to the flight when
    the form is submitted

    :return: The HTML for the passenger entry page or a response object redirecting to /
    """
    if request.method == "POST":
        try:
            booking_model.add_passenger(request.form["name"],
                                        request.form["gender"],
                                        request.form["dob"],
                                        request.form["nationality"],
                                        request.form["residency"],
                                        request.form["passport_number"])
            return redirect("/list_passengers")
        except ValueError as e:
            return render_template("add_passenger.html", error=e)
    else:
        return render_template("add_passenger.html", error=None)


@app.route("/list_passengers")
def list_passengers():
    """
    Serve the page showing passenger details and their seat allocations. From this page, seat allocations can
    be added and changed and passengers can be removed from the flight.

    :return: The HTML for the passenger details page
    """
    passengers = booking_model.get_passengers_including_seat_allocations()
    if len(passengers) > 0:
        home_option = [o for o in options_map if "is_home_link" in o and o["is_home_link"]]
        return render_template("list_passengers.html", passengers=passengers, options_map=home_option)
    else:
        session["message"] = "There are no passengers on the flight"
        return redirect("/")


@app.route("/allocate_seat/<passenger_id>", methods=["GET", "POST"])
def allocate_seat(passenger_id):
    """
    Serve the page prompting for a seat allocation for a single passenger

    :param passenger_id: Unique identifier for the passenger to allocate to a seat
    :return: The HTML for the seat allocation page or a response object redirecting to the passenger details page
    """
    if request.method == "POST":
        try:
            booking_model.flight.allocate_seat(request.form["seat_number"], passenger_id)
            return redirect("/list_passengers")
        except (ValueError, KeyError) as e:
            return render_template("allocate_seat.html",
                                   passenger=booking_model.flight.passengers[passenger_id],
                                   error=e)
    else:
        return render_template("allocate_seat.html",
                               passenger=booking_model.flight.passengers[passenger_id],
                               error=None)


@app.route("/remove_passenger/<passenger_id>", methods=["GET", "POST"])
def remove_passenger(passenger_id):
    """
    Serve the page to confirm removal of a passenger from the current flight and to remove them if confirmed

    :param passenger_id: Unique identifier for the passenger to remove
    :return: The HTML for the confirmation page or a response object redirecting to the passenger details page
    """
    if request.method == "POST":
        booking_model.flight.remove_passenger(passenger_id)
        return redirect("/list_passengers")
    else:
        return render_template("remove_passenger.html", passenger=booking_model.flight.passengers[passenger_id])


@app.route("/print_boarding_cards", methods=["GET", "POST"])
def print_boarding_cards():
    """
    Serve the page to prompt for a gate number and generate boarding cards when the form is submitted

    :return: The HTML for the boarding card generation page or a response object redirecting to /
    """
    if request.method == "POST":
        try:
            booking_model.flight.generate_boarding_cards("pdf", request.form["gate_number"])
            session["message"] = "Boarding cards have been generated"
        except (ValueError, InvalidOperationError) as e:
            return render_template("print_boarding_cards.html", error=e)
        else:
            return redirect("/")
    else:
        return render_template("print_boarding_cards.html", error=None)


@app.route("/save_flight")
def save_flight():
    """
    Save the current flight

    :return: Response object redirecting to /
    """
    booking_model.save()
    session["message"] = "The flight has been saved"
    return redirect("/")


@app.route("/load_flight", methods=["GET", "POST"])
def load_flight():
    """
    Serve the page to prompt for flight details allowing the current flight to be loaded from a flight data file.
    Load the flight when the form is submitted

    :return: The HTML for the load flight page or a response object redirecting to /
    """
    if request.method == "POST":
        try:
            booking_model.load(request.form["flight_number"],
                               request.form["departure_date"])
        except (ValueError, FileNotFoundError) as e:
            return render_template("load_flight.html", error=e)
        else:
            return redirect("/")
    else:
        return render_template("load_flight.html", error=None)


@app.route("/close")
def close_flight():
    """
    Close the current flight

    :return: Response object redirecting to /
    """
    booking_model.close_flight()
    return redirect("/")
